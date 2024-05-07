from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_postgres.vectorstores import PGVector


try:  
    loader = TextLoader('transcript.txt', encoding='utf-8')
    documents = loader.load()
    # print("Document Contents: ", documents)
    print("Document Length: ", len(documents))
except Exception as e:
    print("Error: ", e)


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
texts = text_splitter.split_documents(documents)
print(len(texts))

embeddings = OllamaEmbeddings()
vector = embeddings.embed_query("Testing the embedding model")
print(len(vector))

doc_vectors = embeddings.embed_documents([t.page_content for t in texts[:5]])
print(len(doc_vectors))
print(doc_vectors[0])

# Connect to the database and store the vectors
CONNECTION_STRING = "postgresql+psycopg://postgres:password@localhost:5432/test_vector_db"
COLLECTION_NAME = "Transcript_Vectors" # Set this to the video ID -- it is stored in langchain_pg_collection

db = PGVector.from_documents(embedding=embeddings, documents=texts, collection_name=COLLECTION_NAME, connection=CONNECTION_STRING, use_jsonb=True)
print(db.collection_metadata)

query = "What did they say about the lost 116 pages?"
similar = db.similarity_search_with_score(query, k=5)
for doc in similar:
    print(doc)

# query = "What did they say about the lost 116 pages?"
# db2 = PGVector.similarity_search_with_score(query, k=5)
# for doc in db2:
#     print(doc)



