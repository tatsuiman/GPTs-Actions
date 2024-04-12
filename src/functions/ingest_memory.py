import os
import time
import hashlib
import boto3
from openai import OpenAI
from pinecone import Pinecone, PodSpec

# クライアントの初期化
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
VECTOR_TABLE = os.getenv("VECTOR_TABLE")

embedding_model = "text-embedding-3-small"
index_name = "semantic-search-openai"

def run(text):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(VECTOR_TABLE)
    # Pineconeのインデックスを確認する
    if index_name not in pc.list_indexes().names():
        # インデックスがなければ作成する
        pc.create_index(
            index_name,
            dimension=1536,  # dimensionality of text-embed-3-small
            metric="dotproduct",
            spec=PodSpec(environment="gcp-starter"),
        )
        # インデックスが初期化されるまで待つ
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    # インデックスに接続
    index = pc.Index(index_name)

    # OpenAI API
    client = OpenAI(timeout=20.0, max_retries=3)

    embed = (
        client.embeddings.create(input=text, model=embedding_model).data[0].embedding
    )

    text_id = hashlib.md5(text.encode()).hexdigest()
    created_at = int(time.time())
    # ベクトルデータのみをPineconeに保存する。
    res = index.upsert(
        vectors=[
            {
                "id": text_id,
                "values": embed,
                "metadata": {"created_at": created_at},
            }
        ],
    )
    table.put_item(Item={"id": text_id, "text": text, "created_at": created_at})
    return "OK"
