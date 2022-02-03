import pika


def get_channel_connection(
    queue_name,
    host='localhost',
    port='5672',
    vhost='/',
    user='guest',
    pswrd='guest',
):
    '''
    Setting up connection and creating a channel
    Configuring prefetch count = 1 to make consumer consume only 1 msg at a time
    '''
    url = f'amqp://{user}:{pswrd}@{host}:{port}/%2F{vhost}?heartbeat=3600'
    parameters = pika.URLParameters(url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue_name, durable=True)  # creates if not exists

    return channel




