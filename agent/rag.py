from agent.vectorstore import create_vectorstore

vectorstore = create_vectorstore()

def retrieve_context(query: str):
    docs = vectorstore.similarity_search(query, k=2)
    return "\n".join([doc.page_content for doc in docs])