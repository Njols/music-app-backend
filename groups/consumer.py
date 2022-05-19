import json, os, django
import queue
import pika

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "groups.settings")
django.setup()

from groupsapp.models import User
from groupsapp.serializers import UserSerializer

params = pika.URLParameters(
    "amqps://whkhfpzi:g79RzaI3ilrdvbKmipN5ZvByHVfFtp2k@whale.rmq.cloudamqp.com/whkhfpzi"
)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue="user")


def callback(channel, method, properties, body):
    data = json.loads(body)
    if properties.content_type == "user_created":
        new_user = data
        serializer = UserSerializer(data=new_user)
        if serializer.is_valid():
            serializer.save()

    if properties.content_type == "user_deleted":
        id = data
        user = User.objects.get(id=id)
        user.delete()

    if properties.content_type == "user_changed":
        changed_user = data
        user = User.objects.get(id=changed_user.user_id)
        serializer = UserSerializer(user, data=changed_user)
        if serializer.is_valid():
            serializer.save()


channel.basic_consume(queue="user", on_message_callback=callback)

channel.start_consuming()
connection.close()
