import asyncio
import os
import streamlit as st

from dotenv import load_dotenv
from ollama import AsyncClient as AsyncOllamaClient, ChatResponse, Message


# Load environment variables.
load_dotenv()

# Assign variables from the environment.
llm_model = os.getenv("LLM_MODEL", "deepseek-r1:7b")
ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Create a new client instance.
ollama_client = AsyncOllamaClient(
    host=ollama_host,
)


async def stream_chat_response(message: Message):
    """Stream chat response from the model."""
    messages = st.session_state.messages + [message]
    chat_response: ChatResponse = await ollama_client.chat(
        model=llm_model,
        messages=messages,
        stream=True,
    )

    text = ""
    placeholder = st.empty()

    async for part in chat_response:
        text += part.message.content
        placeholder.markdown(text)

    final_message = Message(role="assistant", content=text)
    st.session_state.messages.append(final_message)


async def main():
    st.title(f"{llm_model} local chatbot")

    # Initialize message history in session state.
    if "messages" not in st.session_state:
        print(f"initialize messages in session state")
        st.session_state.messages = []

    # Display all messages so far.
    for message in st.session_state.messages:
        with st.chat_message(message.role):
            st.markdown(message.content)

    # User input
    user_input = st.chat_input("Type something...")

    if user_input:
        message = Message(role="user", content=user_input)
        st.session_state.messages.append(message)

        # Show the question from the user.
        with st.chat_message("user"):
            st.markdown(message.content)

        # Show the response from the model.
        with st.chat_message("assistant"):
            await stream_chat_response(message)


if __name__ == "__main__":
    asyncio.run(main())
