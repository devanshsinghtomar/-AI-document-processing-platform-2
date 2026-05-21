from langchain_community.vectorstores import Chroma

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def chat_with_document(text, question):

    vectordb = Chroma.from_texts(
        [text],
        embeddings
    )

    docs = vectordb.similarity_search(question)

    answer = docs[0].page_content

    return answer[:1000]