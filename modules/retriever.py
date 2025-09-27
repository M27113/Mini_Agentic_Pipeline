import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader

class Retriever:
    def __init__(self, docs_path):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vectorstore = self._load_docs(docs_path)

    def _load_docs(self, docs_path):
        if not os.path.exists(docs_path):
            raise FileNotFoundError(f"KB folder {docs_path} does not exist!")
        loader = DirectoryLoader(docs_path, glob="*.txt", loader_cls=TextLoader)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs_chunks = splitter.split_documents(documents)
        return FAISS.from_documents(docs_chunks, self.embeddings)

    def get_relevant_docs(self, query, top_k=3):
        results = self.vectorstore.similarity_search(query, k=top_k)
        summary = " ".join([doc.page_content for doc in results])
        return {"summary": summary, "docs": results}
