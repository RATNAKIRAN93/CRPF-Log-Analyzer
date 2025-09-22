from elasticsearch import Elasticsearch
import pandas as pd

def get_es(elastic_url, user, pwd):
    return Elasticsearch(elastic_url, http_auth=(user, pwd), verify_certs=True)

def fetch_counts(es, index="syslog-*", minutes=10):
    q = {
      "query": {"range": {"@timestamp": {"gte": f"now-{minutes}m"}}},
      "size": 0,
      "aggs": {"by_minute": {"date_histogram": {"field": "@timestamp", "fixed_interval": "1m"}}}
    }
    res = es.search(index=index, body=q)
    buckets = res['aggregations']['by_minute']['buckets']
    df = pd.DataFrame([{"t": b['key_as_string'], "count": b['doc_count']} for b in buckets])
    return df

if __name__ == "__main__":
    import os
    ES_URL = os.environ.get("ELASTIC_URL")
    ES_USER = os.environ.get("ELASTIC_USER")
    ES_PWD = os.environ.get("ELASTIC_PASSWORD")
    es = get_es(ES_URL, ES_USER, ES_PWD)
    print(fetch_counts(es, minutes=30).tail())
