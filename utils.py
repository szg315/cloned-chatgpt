from langchain.chains import ConversationChain


def get_chat_response(prompt, memory,model):
    chain = ConversationChain(llm=model, memory=memory)
    response = chain.invoke({"input": prompt})
    return response["response"]