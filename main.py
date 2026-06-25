import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

from utils import get_chat_response

st.title("💬 朋友聊天室")

with st.sidebar:
    st.write("请输入一种api_key")
    openai_api_key = st.text_input("请输入OpenAI API Key：", type="password")
    st.markdown("[获取OpenAI API key](https://platform.openai.com/account/api-keys)")

    deepseek_api_key = st.text_input("请输入deepseek API Key：", type="password")
    st.markdown("[获取deepseek API key](https://platform.deepseek.com/usage)")

    qwen_api_key = st.text_input("请输入Qwen API Key：", type="password")
    st.markdown("[获取Qwen API key](https://bailian.console.aliyun.com/cn-beijing?tab=model#/api-key)")

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(return_messages=True)
    st.session_state["messages"] = [{"role": "ai",
                                     "content": "你好，我是你的AI助手，有什么可以帮你的吗？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()
if prompt:
    if openai_api_key:
        model=ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=openai_api_key,
            temperature=0.7
        )
    elif deepseek_api_key:
         model=ChatOpenAI(
            model="deepseek-v4-flash",
            openai_api_key=deepseek_api_key,
            base_url="https://api.deepseek.com",
            temperature=0.7
        )
    elif qwen_api_key:
        model=ChatOpenAI(
            model="qwen3-turbo",
            openai_api_key=qwen_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            temperature=0.7
        )
    else:
        st.info("请输入一个 API Key")
        st.stop()
    
    st.session_state["messages"].append({"role": "human", "content": prompt})
    st.chat_message("human").write(prompt)

    with st.spinner("AI正在思考中，请稍等..."):
        response = get_chat_response(prompt, st.session_state["memory"],model)
    msg = {"role": "ai", "content": response}
    st.session_state["messages"].append(msg)
    st.chat_message("ai").write(response)