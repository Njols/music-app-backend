import json
import pika

params = pika.URLParameters(
    "amqps://whkhfpzi:g79RzaI3ilrdvbKmipN5ZvByHVfFtp2k@whale.rmq.cloudamqp.com/whkhfpzi"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="group", body=json.dumps(body), properties=properties
    )
