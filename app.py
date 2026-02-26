import streamlit as st
import requests

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Local LLM Chat (Ollama)",
    page_icon="🧠"
)

st.title("🧠 Local LLM Chatbot")
st.caption("Using Ollama + Streamlit in Python's Virtual Environment")

# ----------------------------
# Initialize Session State
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# Reset Conversation Button
# ----------------------------
if st.button("🔄 Reset Chat"):
    st.session_state.chat_history = []
    st.rerun()

# ----------------------------
# Display Chat History
# ----------------------------
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# ----------------------------
# User Input Box
# ----------------------------
user_prompt = st.chat_input("Ask something from local LLM...")

# ----------------------------
# Function to call Ollama API
# ----------------------------
def query_ollama(prompt):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "No response from model")
    except requests.exceptions.ConnectionError:
        return "❌ Ollama server is not running. Start it using: ollama serve"
    except requests.exceptions.Timeout:
        return "❌ Model is taking too long to respond"
    except Exception as e:
        return f"❌ Error: {e}"

# ----------------------------
# Handle User Input
# ----------------------------
if user_prompt:
    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_prompt
    })

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Get LLM Response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            answer = query_ollama(user_prompt)
            st.markdown(answer)

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": answer
    })
