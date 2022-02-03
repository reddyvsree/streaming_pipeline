import os
import json
import time
import pika
import requests
import config as cfg
from utils.log_utils import get_logger
from twitter_rules import (
    delete_all_rules,
    get_rules,
    create_rules,
    get_bearer_token,
)
from utils.simple_queue import get_channel_connection


logger = get_logger('stream_driver')
channel = get_channel_connection('tweets_stream', host='rabbitmq')


def push_to_queue(message):
    '''
    Publish message to queue
    '''
    properties = pika.BasicProperties(delivery_mode=2)
    channel.basic_publish(
        exchange='',
        routing_key='tweets_stream',
        body=message,
        properties=properties
    )


def connect_stream():
    '''
    Connects to Twitter API and streams tweets continuously
    '''
    url = f'{cfg.BASE_URL}?{cfg.TWEET_FIELDS}{cfg.USER_FIELDS}'
    url = url + 'expansions=author_id'
    token = get_bearer_token()
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(
        url,
        headers=headers,
        stream=True,
    )
    print(response.status_code)

    if response.status_code != 200:
        code = response.status_code
        text = response.text
        raise Exception(
            f"Cannot get tweets (HTTP {code}): {text}"
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            push_to_queue(json.dumps(json_response))


def main():
    '''
    Recreates rules - from config.yaml - and initiates the stream with exponential backoff when we encounter http error
    '''
    rules = get_rules()
    delete_all_rules(rules)
    create_rules()
    timeout = 0
    max_timeout = 5
    while True:  # retry on failure
        try:
            connect_stream()
        except Exception:
            time.sleep(2**timeout)  # exponential wait time
            timeout += 1
            if timeout == max_timeout:
                timeout = 0


if __name__ == "__main__":

    main()
