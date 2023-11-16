import csv
import requests
import pinecone
import pickle

# Constants
OPENAI_API_KEY = ""
CSV_FILE_PATH = input( "The CSV File: " )
PINECONE_API_KEY = ""
ENVIRONMENT_PINE = ""
PINE_INDEX = ""
EMBEDDING_DIMENSION = 1536
pinecone.init(api_key=PINECONE_API_KEY, environment=ENVIRONMENT_PINE) 
index = pinecone.Index(PINE_INDEX) 

# OpenAI endpoint details
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
url = "https://api.openai.com/v1/embeddings"

# Read the CSV data
with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    posts = [row for row in reader]

vectors = {}
n = 0
for post in posts:
    title, content, link, post_id = post

    # Fetch embedding for the content
    payload = {
        "input": content,
        "model": "text-embedding-ada-002",
        "encoding_format": "float"
    }
    response = requests.post(url, headers=headers, json=payload)
    embedding = response.json()["data"][0]["embedding"]
    print( f"generated embeddding, moving on to post #{n}")
    n += 1
    # Using the link (or title) as the key for Pinecone might be a good idea if they're unique
    # This ensures you can directly retrieve the post URL when querying Pinecone later.
    vectors[link] = {'embedding': embedding, 'title': title, 'post_id': post_id}

with open("embeddings.pkl", "wb") as f:
    pickle.dump(vectors, f)

with open("embeddings.pkl", "rb") as f:
    vectors = pickle.load(f)
# Upsert vectors to Pinecone
print("upserting to Pinecone")

formatted_vectors = []
for link, data in vectors.items():
    embedding = data['embedding']
    title = data['title']
    post_id = data['post_id']
    vector_data = {
        "id": link,
        "values": embedding,
        "metadata": {
            "title": title,
            "post_id": post_id
        }  # if you want to store the title as metadata
    }
    formatted_vectors.append(vector_data)

# Upsert to Pinecone
upsert_response = index.upsert(vectors=formatted_vectors)
