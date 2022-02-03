import time
import json
import xxhash
from elasticsearch import Elasticsearch
from utils.simple_queue import get_channel_connection
from utils.log_utils import get_logger

# Setting up logging and service envs
logger = get_logger('ingester')
channel = get_channel_connection('tweets_stream', host='rabbitmq')
esclient = Elasticsearch(f"http://elasticsearch:9200/")


def get_hash(data):
    '''
    Generates unique hash of a tweet
    that will used as id in elasticsearch document
    '''
    data = data.decode('utf-8')
    _hash = xxhash.xxh64(data).hexdigest()
    return _hash


def ingest_to_elasticsearch(doc):
    '''
    Indexes tweets to elasticsearch using index api
    '''
    id_ = get_hash(doc)
    try:
        res = esclient.index(index="testindex", id=id_, document=doc)
        logger.info('ingested doc of hash %s', id_)
        logger.debug(res['result'])
        logger.debug(doc)
        return True
    except Exception as err:
        logger.error('exception occured: %s', str(err))
        return False


def consume():
    '''
    Listens to rabbitmq for new tweets
    Ingests into elasticsearch upon a receving the tweet from a queue
    '''
    for method, prop, body in channel.consume('tweets_stream'):
        result = ingest_to_elasticsearch(body)
        if result:
            channel.basic_ack(method.delivery_tag)
            logger.info('task sucessful, sending ack')
            logger.debug('delivery tag: %s', method.delivery_tag)
        else:
            # Nack will redeliver
            channel.basic_nack(method.delivery_tag)


if __name__ == "__main__":
    consume()
