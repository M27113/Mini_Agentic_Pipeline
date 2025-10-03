import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader

class Retriever:
    def __init__(self, docs_path):
        # added try except for better error handling
        try:
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            self.vectorstore = self._load_docs(docs_path)
        except FileNotFoundError as fnf_error:
            print(f"[Error] KB folder not found: {fnf_error}")
            raise
        except Exception as e:
            print(f"[Error] Failed to initialize Retriever: {e}")
            raise
        self.cache = {}  # In-memory cache for document retrievals

    def _load_docs(self, docs_path):
        # added check for docs_path existence
        if not os.path.exists(docs_path):
            raise FileNotFoundError(f"KB folder {docs_path} does not exist!")
        try:
            loader = DirectoryLoader(docs_path, glob="*.txt", loader_cls=TextLoader)
            documents = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs_chunks = splitter.split_documents(documents)
            return FAISS.from_documents(docs_chunks, self.embeddings)
        except Exception as e:
            print(f"[Error] Failed to load documents: {e}")
            raise

    def get_relevant_docs(self, query, top_k=3):
        # added simple in-memory cache for retrieval results
        if query in self.cache:  # Check cache first
            return self.cache[query]
        try: 
            results = self.vectorstore.similarity_search(query, k=top_k)
            summary = " ".join([doc.page_content for doc in results])
            output = {"summary": summary, "docs": results}
        except Exception as e:
            print(f"[Error] Failed to retrieve relevant docs: {e}")
            output = {"summary": "", "docs": []}    

        self.cache[query] = output  # Cache the result
        return output
