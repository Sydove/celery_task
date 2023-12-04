from pika import BlockingConnection, ConnectionParameters
from queue import Queue
from threading import Lock

class RabbitMQPool:
    def __init__(self, pool_size=5, **connection_params):
        self.pool = Queue(maxsize=pool_size)
        self.connection_params = connection_params
        self.lock = Lock()

    def create_connection(self):
        return BlockingConnection(ConnectionParameters(**self.connection_params))

    def get_connection(self):
        with self.lock:
            if self.pool.qsize() < 1:
                return self.create_connection()
            return self.pool.get()

    def release_connection(self, connection):
        self.pool.put(connection)

    def close_pool(self):
        with self.lock:
            while not self.pool.empty():
                connection = self.pool.get()
                connection.close()

# 示例用法
if __name__ == '__main__':
    rabbitmq_params = {
        'host': 'localhost',
        'port': 5672,
        'username': 'guest',
        'password': 'guest',
    }

    rabbitmq_pool = RabbitMQPool(pool_size=5, **rabbitmq_params)

    try:
        # 使用连接池获取连接
        connection = rabbitmq_pool.get_connection()

        # 在连接上执行一些操作，例如声明队列、发布消息等
        channel = connection.channel()
        channel.queue_declare(queue='hello_queue')
        channel.basic_publish(exchange='', routing_key='hello_queue', body='Hello, RabbitMQ!')

        # 释放连接
        rabbitmq_pool.release_connection(connection)

    finally:
        # 关闭连接池
        rabbitmq_pool.close_pool()


# 连接 RabbitMQ 服务器
connection_params = pika.ConnectionParameters(
    host='47.108.164.71',  # RabbitMQ 服务器的主机名或 IP 地址
    port=5672,  # RabbitMQ 服务器的端口，默认是 5672
    virtual_host='admin',
    credentials=pika.PlainCredentials(
        username='admin',  # RabbitMQ 的用户名
        password='admin'  # RabbitMQ 的密码
    )
)

# 建立到 RabbitMQ 服务器的连接
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 定义队列
channel.queue_declare(queue='hello')

# 发布消息
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")


# 定义回调函数来处理接收到的消息
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


# 消费消息
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
