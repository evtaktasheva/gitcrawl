import pika
import os
import sys
from utils import Downloader
from conf import SERVER_LOGIN, SERVER_PASSWORD


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    down = Downloader(body.decode())
    down.download()
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # connect to RabbitMq queue
    credentials = pika.PlainCredentials(SERVER_LOGIN, SERVER_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='18.133.183.10', port=5672,
                                  virtual_host='gitcrawl',
                                  credentials=credentials)
    )
    channel = connection.channel()

    # (re)declare queue if non-existent
    channel.queue_declare(queue='queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    # begin consuming messages
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='queue', on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)