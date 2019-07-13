import pika

# Established connection with RabbitMQ Server
"""
    ConnectionParameters take the host or IP addr of the RabbitMQ Server
    The container name in a specified environment
"""
connection = pika.BlockingConnection(pika.ConnectionParameters(host='t_rabbit')) 
channel = connection.channel()

# Need to create a queue before sending a message, however the message will be dropped by RabbitMQ
#channel.queue_declare(queue='hello')

result = channel.queue_declare(queue='', exclusive=True)

# Give the queue to callback_queue, setted in result 
callback_queue = result.method.queue

# A message need to go through an exchange and can't be send directly to the queue

"""
    when exchange is an empty string
    routing_key args define the queue which will be used to send the message
# """
# Basic exemple
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World!')

# Setting RPC mode
channel.basic_publish(  exchange='',
                        routing_key='rpc_queue',
                        properties=pika.BasicProperties(
                            # Describe the MIME-type of the encoding, often is application/json
                            content_type='application/json',

                            # Used to name the callback queue
                            reply_to=callback_queue,

                            # ID that identified the response with this request
                            correlation_id='test'
                        ),
                        body='Hello World!')
print(" [x] Sent 'Hello World!'")

# We need to close the connection to flush buffers to do is gently
connection.close()