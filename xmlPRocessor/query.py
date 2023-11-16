import pinecone
import requests
# Initialize Pinecone
PINECONE_API_KEY = ""
ENVIRONMENT_PINE = ""
PINE_INDEX = ""
OPENAI_API_KEY = ""
pinecone.init(api_key=PINECONE_API_KEY, environment=ENVIRONMENT_PINE)
index = pinecone.Index(PINE_INDEX)

query_text = input( "Your topic or query here: " )
# OpenAI endpoint details
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}
url = "https://api.openai.com/v1/embeddings"

payload = {
    "input": query_text,
    "model": "text-embedding-ada-002",
    "encoding_format": "float"
}
response = requests.post(url, headers=headers, json=payload)
embedding = response.json()["data"][0]["embedding"]

# Query Pinecone for similar posts
top_k_results = 4  # or however many you want
query_response = index.query(
    top_k=top_k_results,
    include_values=True,
    include_metadata=True,
    vector=embedding
)

# Extract and display results
for match in query_response.matches:
    print(f"URL: {match.id}")  # Assuming IDs are the URLs
    print(f"Title: {match.metadata['title']}")
    print(f"Post ID: {match.metadata['post_id']}")
    print(f"Similarity Score: {match.score}")
    print("----------------------")
