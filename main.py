from database import SQLDatabase, SQLDatabaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings

# Example usage
db = SQLDatabase("postgresql://postgres:password@localhost:5432/podcast-app")
query = "SELECT * FROM episodeinfo WHERE yt_channel_id = 'UCG0yyZlH_HYWmKegHoC96ig'"
loader = SQLDatabaseLoader(query, db)

# Load data
data = loader.load_data()
print(len(data))
print(data)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
texts = text_splitter.split_documents(data)
print(texts[0][4])