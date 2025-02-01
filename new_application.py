import os
import streamlit as st
from groq import Groq

# Initialize Groq API client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Page Configuration
st.set_page_config(page_title="Super Chat", layout="wide", page_icon="⚡")

# Custom CSS for a clean chat UI
st.markdown("""
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #f9f9f9;
        }
        .main-container {
            max-width: 900px;
            margin: auto;
            padding: 20px;
        }
        .chat-box {
            background: white;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
        }
        .user-message {
            text-align: right;
            color: white;
            background-color: #0084ff;
            padding: 12px;
            border-radius: 15px;
            max-width: 70%;
            display: inline-block;
        }
        .bot-message {
            text-align: left;
            color: black;
            background-color: #e0e0e0;
            padding: 12px;
            border-radius: 15px;
            max-width: 70%;
            display: inline-block;
        }
        .chat-history {
            height: 450px;
            overflow-y: auto;
            border-radius: 15px;
            padding: 15px;
            background: #f4f4f4;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        }
        .stTextInput > div > div > input {
            font-size: 16px;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #ddd;
            width: 100%;
        }
        .stButton button {
            background-color: #0084ff;
            color: white;
            font-size: 16px;
            padding: 12px 20px;
            border-radius: 10px;
            margin-top: 10px;
            width: 100%;
        }
        .action-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
        }
        .action-buttons .stButton button {
            width: 48%;
            background: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Load logo (Optional: Change the file path accordingly)
st.image("langchain+chatglm.png", width=120)  # Replace with your actual logo path

st.markdown("<h1 style='text-align: center;'>⚡ Super Chat</h1>", unsafe_allow_html=True)
st.write("💬 **Ask anything about global real estate, and I'll remember our conversation!**")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant and only respond to global real estate queries."}
    ]

# Display chat history only if there are messages
if len(st.session_state.messages) > 1:
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    for message in st.session_state.messages[1:]:  # Skip system prompt
        if message["role"] == "user":
            st.markdown(f'<div class="chat-box"><div class="user-message">{message["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-box"><div class="bot-message">{message["content"]}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# User input for chat
user_query = st.text_input("Ask a question:", placeholder="Type your message here...")

# Generate response if the user submits a query
if st.button("Search") and user_query.strip():
    with st.spinner("Oora Thinking..."):
        try:
            # Append user query to session
            st.session_state.messages.append({"role": "user", "content": user_query})

            # Get response from Groq API
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,  # Send conversation history
                model="llama-3.3-70b-versatile",
            )

            response = chat_completion.choices[0].message.content

            # Append assistant response to memory
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Refresh chat history
            st.experimental_rerun()

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Floating Action Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant and only respond to global real estate queries."}
        ]
        st.experimental_rerun()

with col2:
    if st.button("🔄 Regenerate Response"):
        with st.spinner("Generating new response..."):
            try:
                # Get last user message
                last_user_message = [msg for msg in st.session_state.messages if msg["role"] == "user"][-1]["content"]

                # Get new response from Groq API
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,  # Send conversation history
                    model="llama-3.3-70b-versatile",
                )

                response = chat_completion.choices[0].message.content

                # Replace last bot response with the new response
                if st.session_state.messages[-1]["role"] == "assistant":
                    st.session_state.messages[-1] = {"role": "assistant", "content": response}
                else:
                    st.session_state.messages.append({"role": "assistant", "content": response})

                # Refresh chat history
                st.experimental_rerun()

            except Exception as e:
                st.error(f"An error occurred: {e}")
