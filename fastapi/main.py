import os
from fastapi import FastAPI, Query
from opensearchpy import OpenSearch

app = FastAPI()
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "http://opensearch:9200")
INDEX = os.getenv("OPENSEARCH_INDEX", "system-logs")
client = OpenSearch([OPENSEARCH_HOST])

@app.get("/search")
def search(q: str = Query(..., description="Query string")):
    body = {
        "query": {
            "query_string": {
                "query": q
            }
        },
        "size": 100
    }
    res = client.search(index=INDEX, body=body)
    hits = [h["_source"] for h in res["hits"]["hits"]]
    return {"count": res["hits"]["total"]["value"], "results": hits}
