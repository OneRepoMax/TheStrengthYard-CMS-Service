from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key='question',
    output_key='answer'
)

# Creating a custom prompt
template = """Use the following pieces of context to answer the question at the end.
{context}
Question: {question}
Helpful Answer:"""
custom_prompt = PromptTemplate.from_template(template)

from langchain.chat_models import ChatOpenAI
llm_name = "gpt-3.5-turbo"
llm = ChatOpenAI(model_name=llm_name, temperature=0)

# Using the Conversational Retrieval Chain
retriever=vectordb.as_retriever()

qa = ConversationalRetrievalChain.from_llm(
    llm,
    combine_docs_chain_kwargs={"prompt": custom_prompt},
    retriever=retriever,
    return_source_documents=True,
    return_generated_question=True,
    memory=memory
)

# Use this code cell to specify a question and display LLM's response
while True:
    question = input("Enter your question: ")
    result = qa({"question": question})
    print("Response: \n",result["answer"])