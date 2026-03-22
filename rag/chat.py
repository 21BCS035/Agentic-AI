from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

# take user input
user_query = input("Ask something ...")

# relevant chunks from the vector_db
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
])

SYSTEM_PROMPT = f"""
 You are an expert helpful AI Assistant who answers user query based on the available context retrieved from PDF file along with page_contents and page number.
 You should only answer based on the following context and navigate the user to open the right page number to know more.
 
Context:
{context} 
"""

response = openai_client.chat.completions.create(
    model="gpt-5",
    messages=[
        { "role":"system", "content":SYSTEM_PROMPT },
        { "role":"user", "content":user_query }
    ]
)

print(f"🧠 : {response.choices[0].message.content}")
