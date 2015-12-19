#!/Users/alex/coding/tassl/mailer/venv/bin/python
"""This script connects to a RabbitMQ server and sends a 'welcome-to-tassl' email for each message in the queue"""
import pika, send_template, json, config


def connect_to_rabbitmq(username, password, rabbit_server, rabbit_queue):
	creds = pika.credentials.PlainCredentials(username, password)
	parameters = pika.ConnectionParameters(rabbit_server,5672,'/',creds)
	global connection
	connection = pika.BlockingConnection(parameters)
	global channel
	channel = connection.channel()
	channel.queue_declare(queue=rabbit_queue)
	print('[*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    j = json.loads(str(body.decode("utf-8"))) #json sent as stream of bytes, so utf-8 decoding is needed to make a string
    name = j['name']
    email = j['email']
    school = j['alma_mater']
    print("Message received. Sending email to %s (%s), from %s." % (name, email, school))
    send_template.dispatch(template_identifier='welcome-to-tassl', recipient_name=name, recipient_email=email, recipient_alma_mater=school)
    print("[x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

connect_to_rabbitmq(config.RABBITMQ_USERNAME, config.RABBITMQ_PASSWORD,config.RABBITMQ_SERVER, config.RABBITMQ_QUEUE)
#channel.basic_qos(prefetch_count=1) #why didn't this work?
channel.basic_consume(callback, queue='signups')
channel.start_consuming()

