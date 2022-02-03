import yaml


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


configs = read_yaml('config.yaml')
CONSUMER_KEY = configs['TWITTER']['consumer_key']
CONSUMER_SECRET = configs['TWITTER']['consumer_secret']
ADD_RULES = configs['FILTER_RULES']['rules']
BASE_URL = 'https://api.twitter.com/2/tweets/search/stream'
AUTH_URL = 'https://api.twitter.com/oauth2/token'
TWEET_FIELDS = "tweet.fields=id,text,author_id,conversation_id,created_at,entities,geo,lang,public_metrics,possibly_sensitive,referenced_tweets,source,withheld&"
USER_FIELDS = "user.fields=entities,id,location,name,username,verified&"
NETLOC = 'localhost' 
