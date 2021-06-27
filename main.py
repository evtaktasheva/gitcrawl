import pika
import psycopg2
from conf import DB_LOGIN, DB_PASSWORD, SERVER_LOGIN, SERVER_PASSWORD


# connect to database
conn = psycopg2.connect(dbname="qnkabsei",
                        user=DB_LOGIN,
                        password=DB_PASSWORD,
                        host="hattie.db.elephantsql.com")
cur = conn.cursor()

# select all not downloaded files
cur.execute("""SELECT file_id, file_link
               FROM gitcrawl 
               WHERE seen != True""")
messages = cur.fetchall()
conn.close()

# connect to RabbitMQ queue
credentials = pika.PlainCredentials(SERVER_LOGIN, SERVER_PASSWORD)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='18.133.183.10', port=5672,
                              virtual_host='gitcrawl', credentials=credentials)
)
channel = connection.channel()

# send objects to queue
channel.queue_declare(queue='queue', durable=True)
for message in messages:
    message = ' '.join(map(str, message))
    channel.basic_publish(
        exchange='',
        routing_key='queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        ))
    print(" [x] Sent %r" % message)

connection.close()

