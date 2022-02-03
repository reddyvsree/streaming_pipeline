'''
This reads in the tweets, does an aggregate over the field __version, to count duplicates as well for total count

-- __version field gets update when a document of same id (id is the hash of whole tweet object) is inserted
'''

from elasticsearch import Elasticsearch
es = Elasticsearch()

data = es.search(index="testindex", body={"query":{"match_all":{}}})

query_body ={
  "aggs": {
    "total_consumed_count": {
      "sum": {
        "field": "_version"
      }
    }
  }
}

result = es.search(index="testindex", body=query_body)

print("Total Unique tweets {}".format(int(result['hits']['total']['value'])))
print("Total Consumed tweets {}".format(int(result['aggregations']['total_consumed_count']['value'])))