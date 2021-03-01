import pika
import logging
import encoding

logging.getLogger().setLevel(logging.INFO)

class Consumer(object):
    def __init__(self):

        # Setting connection, try every 10 seconds until 5 times if fail
        self.connection = pika.BlockingConnection(
                            pika.ConnectionParameters(
                                host='t_rabbit',
                                connection_attempts=5, 
                                retry_delay=10))

        # Get the channel from the connexion
        self.channel = self.connection.channel()

        # Declaring the queue which will be used to communicate with the receiver
        result = self.channel.queue_declare(queue='rpc_queue')

        # Contain the queue
        self.callback_queue = result.method.queue

        self.channel.basic_qos(prefetch_count=1)

        # Consume client queue, means that the question get an answer by the RPC
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.replying,
            )

    def start(self):
        self.channel.start_consuming()

    # To send a reply, need to set a publishing request in the fonction
    def replying(self, ch, method, props, body):
        print(" [x] Receive :: {}".format(body))

        response = "is ok"

        # setting the publishing message
        ch.basic_publish(   exchange='',

                            # Got the value in reply_to on the other side (here, the callback_queue name)
                            routing_key=props.reply_to,

                            # Setting properties to match sender's (by the correlation_id)
                            properties=pika.BasicProperties(
                                correlation_id = props.correlation_id),

                            # Give the response in the body
                            body=str(response))

        # Need more informations
        ch.basic_ack(delivery_tag=method.delivery_tag)

        # body is type bytes, need to decode to get the string
        file_path = body.decode('utf-8')

        # Launching the encoding
        encoder = encoding.Encoding()
        encoder.post(file_path)

    def responseQueue(self, file_path):
        self.encoding_queue = self.channel.queue_declare(queue='response_encoding')

        self.response = None
        #self.corr_id = str(uuid.uuid4())

        # publish the first message which will wait for a response
        # self.channel.basic_publish(
        #     exchange='',
        #     routing_key='response_encoding',
        #     properties=pika.BasicProperties(
        #         reply_to=self.encoding_queue,
        #         correlation_id=self.corr_id,
        #     ),
        #     body=str(n))

        logging.info("\n\nTYPE OF FILE_PATH :: {}\n\n".format(type(file_path)))

        self.channel.basic_publish(
                exchange='',
                routing_key=self.encoding_queue,
                body=file_path)



    
# Established connection with RabbitMQ Server
"""
    ConnectionParameters take the host or IP addr of the RabbitMQ Server
    The container name in a specified environment
""
connection = pika.BlockingConnection(pika.ConnectionParameters(host='t_rabbit')) 
channel = connection.channel()

# Need to create a queue before sending a message, however the message will be dropped by RabbitMQ
""
    It's a bets practice to avoid an inexistant queue, however we can't be sure which script will be run as first
    We can say that this line do : declare queue if not exist
""
#channel.queue_declare(queue='hello')
#channel.queue_declare(queue='rpc_queue')

# Function callback which is needed to receive the message from the Queue
def callback(ch, method, properties, body):
    print(" [x] Receive :: {}".format(body))

# To send a reply, need to set a publishing request in the fonction
def replying(ch, method, props, body):
    print(" [x] Receive :: {}".format(body))

    response = "is ok"

    # setting the publishing message
    ch.basic_publish(   exchange='',

                        # Got the value in reply_to on the other side (here, the callback_queue name)
                        routing_key=props.reply_to,

                        # Setting properties to match sender's (by the correlation_id)
                        properties=pika.BasicProperties(
                            correlation_id = props.correlation_id),

                        # Give the response in the body
                        body=str(response))

    # Need more informations
    ch.basic_ack(delivery_tag=method.delivery_tag)

""
# Setting the order of the process, here, define as first
channel.basic_qos(prefetch_count=1)

# Consuming the queue, on_message_callback represent the function which receive the message consumed in the queue
# channel.basic_consume(  queue='hello',
#                         auto_ack = True,
#                         on_message_callback = callback)

# Consume the rpc_queue's message and answer with the replying function, which send a message on the sender's queue
channel.basic_consume(queue='rpc_queue', on_message_callback=replying)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
"""