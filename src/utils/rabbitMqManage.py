import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建扇出交换机
channel.exchange_declare(exchange='fanout_exchange', exchange_type='fanout')

# 创建队列，队列名为随机生成的，exclusive 表示当连接断开时，队列会被删除
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# 将队列绑定到扇出交换机
channel.queue_bind(exchange='fanout_exchange', queue=queue_name)
