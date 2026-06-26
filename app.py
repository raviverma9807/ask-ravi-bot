import streamlit as st

from services.openai_service import OpenAIService
from services.search_service import SearchService

from utils.ui import (
    render_header,
    render_sidebar,
    render_sources
)

from utils.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_DEPLOYMENT,
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_KEY,
    AZURE_SEARCH_INDEX
)

# --- Page setup ---
st.set_page_config(
    page_title="Ravi Verma | Career Portfolio",
    page_icon="r2.png"
)

search_service = SearchService(
    endpoint=AZURE_SEARCH_ENDPOINT,
    api_key=AZURE_SEARCH_KEY,
    index_name=AZURE_SEARCH_INDEX
)

openai_service = OpenAIService(
    endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    deployment=AZURE_DEPLOYMENT
)

render_header()
render_sidebar()

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I'm Ravi Verma's AI Career Assistant. Ask me about my experience, projects, Azure expertise, .NET skills, certifications, or education."
        }
    ]

# --- Render chat messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Preset Question ---
if "preset_question" not in st.session_state:
    st.session_state["preset_question"] = ""

# --- Chat Input ---
user_input = st.chat_input(
    "Ask about my Azure experience, .NET projects, certifications, or AI solutions..."
)

if not user_input and st.session_state["preset_question"]:
    user_input = st.session_state["preset_question"]
    st.session_state["preset_question"] = ""

# --- Process User Input ---
if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        with st.spinner("Getting response..."):

            context, sources = search_service.search_documents(user_input)

            answer = openai_service.generate_answer(
                question=user_input,
                context=context,
                history=st.session_state.messages
            )

    except Exception as ex:
        answer = f"⚠️ Error: {ex}"
        sources = []

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)
        render_sources(sources)
    