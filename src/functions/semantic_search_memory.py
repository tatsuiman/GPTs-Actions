import os
import boto3
import json
from openai import OpenAI
from pinecone import Pinecone

VECTOR_TABLE = os.getenv("VECTOR_TABLE")

embedding_model = "text-embedding-3-small"
index_name = "semantic-search-openai"


def run(query, pinecone_api_key, openai_api_key):
    result = []
    # クライアントの初期化
    pc = Pinecone(api_key=pinecone_api_key)
    client = OpenAI(api_key=openai_api_key)
    # dynamodb client
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(VECTOR_TABLE)
    # 質問内容をベクトル化
    xq = client.embeddings.create(input=query, model=embedding_model).data[0].embedding
    index = pc.Index(index_name)
    res = index.query(vector=[xq], top_k=3, include_metadata=True)
    matches = res["matches"]
    for match in matches:
        res = table.get_item(Key={"id": match["id"]})
        result.append({"text": res["Item"]["text"], "score": match["score"]})

    return json.dumps({"match": result}, ensure_ascii=False)
