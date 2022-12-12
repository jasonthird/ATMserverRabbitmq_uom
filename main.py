#!/usr/bin/env python
import pika
from SqlConnection import Sql
from decimal import Decimal

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    sql = Sql()
    msg = str(body.decode('UTF-8'))
    # message type is OPERATION data
    # message: auth username pin
    # message: withdraw auth amount
    # message: deposit auth amount
    # example message: auth bob 1234
    msg = msg.split(' ')
    try:
        if msg[0] == 'auth':
            if msg[1] is not None and msg[2] is not None:
                response = sql.AuthUser(msg[1], msg[2])
            else:
                response = "Invalid message"
        elif msg[0] == 'withdraw':
            if msg[1] is not None and msg[2] is not None:
                before, after = sql.Withdraw(msg[1], msg[2])
                response = before - after
            else:
                response = "Invalid message"
        elif msg[0] == 'deposit':
            if msg[1] is not None and msg[2] is not None:
                before, after = sql.Deposit(msg[1], msg[2])
                response = after - before
            else:
                response = "Invalid message"
        elif msg[0] == 'balance':
            if msg[1] is not None:
                response = sql.getBalance(msg[1])
            else:
                response = "Invalid message"
        else:
            response = "Invalid message"
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(e)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         body=str("Invalid message"))
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
