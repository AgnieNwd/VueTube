import pika
import uuid
import logging

logging.getLogger().setLevel(logging.INFO)

class SenderClient(object):

    # Setting to join the broker
    def __init__(self):

        logging.info("\n\nTEST CONNEXION\n\n")

        # Get the connexion
        self.connection = pika.BlockingConnection(
                            pika.ConnectionParameters(
                                host='t_rabbit',
                                connection_attempts=5, 
                                retry_delay=10))
        
        logging.info("\n\nConnexion OK")

        # Get the channel from the connexion
        self.channel = self.connection.channel()

        # Declaring the queue which will be used to communicate with the receiver
        result = self.channel.queue_declare(queue='', exclusive=True)

        # Contain the queue
        self.callback_queue = result.method.queue

        # Consume client queue, means that the question get an answer by the RPC
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    # Check if the correlation_id match with the question, send the body if ok
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # publish the first message which will wait for a response
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))

        # while no response was received by the broker, continue to scan
        while self.response is None:
            self.connection.process_data_events()

        # when the response was given, return the response message
        return self.response

    def reception_callback(self, ch, method, properties, body):
        logging,info("\n\n ON RETOUR CALLBACK :: {}\n\n".format(body))


    def start(self):
        self.channel.start_consuming()

    def get_response_encoded(self):

        logging.info("\n\nI NEED TO GET THE RABBIT RESPONSE \n\n")
        # Declaring the queue
        receive_queue = self.channel.queue_declare(queue='response_encoding')

        logging.info("\n\nI NEED TO GET THE RABBIT RESPONSE 2\n\n")
        # Setting the order of the process, here, define as first
        self.channel.basic_qos(prefetch_count=2)

        logging.info("\n\nI NEED TO GET THE RABBIT RESPONSE 3\n\n")
        # Consuming the queue, on_message_callback represent the function which receive the message consumed in the queue
        self.channel.basic_consume(queue=receive_queue.method.queue, auto_ack=True, on_message_callback=self.reception_callback)
        logging.info("\n\nI NEED TO GET THE RABBIT RESPONSE 4\n\n")
# sender = SenderClient()

# print(" [x] Requesting fib(30)")
# response = sender.call("toto is ok ?")
# print(" [.] Got %r" % response)