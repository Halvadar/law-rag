
# %%
from dotenv import load_dotenv

load_dotenv()


# %%
from langchain_community.document_loaders import PyPDFLoader


loader = PyPDFLoader("kanoni.pdf")
pages = loader.load()
text = ""
for page in pages:
    text += page.page_content

# print first 1000 characters



# %%
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0,
    separators=["თავი [IVXLCDM]+", "მუხლი \d+"],
    is_separator_regex=True,
)
chunks = text_splitter.split_text(text)



# %%
# embed chunks
from langchain_cohere import CohereEmbeddings
import os
# store chunks in chroma
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="kanoni",
    embedding_function=CohereEmbeddings(cohere_api_key=os.getenv("COHERE_API_KEY"), model="embed-multilingual-v3.0"),
    persist_directory="./chroma_langchain_db",
    create_collection_if_not_exists=True
)



# %%
import os
import time
from tenacity import retry, wait_exponential, stop_after_attempt
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def get_embeddings(texts):
    embeddings = CohereEmbeddings(cohere_api_key=os.environ["COHERE_API_KEY"], model="embed-multilingual-v3.0", )
    return embeddings.embed(texts=texts,input_type="search_document")



# Add texts in smaller batches with delay
batch_size = 5  # Reduced batch size
total_batches = len(chunks) // batch_size + (1 if len(chunks) % batch_size > 0 else 0)

for i in range(0, len(chunks), batch_size):
    try:
        print(f"Processing batch {i//batch_size + 1} of {total_batches}")
        batch = chunks[i:i+batch_size]
        print("embedding batch")
        # Get embeddings for the batch
        embeddings = get_embeddings(batch)
        print("adding to vector store")
        # Add texts and embeddings to the vector store
        vector_store.add_texts(texts=batch, embeddings=embeddings)
        
        print(f"Successfully added batch {i//batch_size + 1}")
        time.sleep(1)  # Increased delay between batches
    except Exception as e:
        print(f"Error processing batch {i//batch_size + 1}: {str(e)}")
        time.sleep(2)  # Longer delay if an error occurs

print("Finished processing all batches")


# %%
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 6})

# %%
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import hub
from langchain_openai import ChatOpenAI
prompt = hub.pull("rlm/rag-prompt")

llm = ChatOpenAI(model="gpt-4o-mini")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

for chunk in rag_chain.stream("რამდენ წლიანი სასჯელია ქურდობაზე?"):
    print(chunk, end="", flush=True)

