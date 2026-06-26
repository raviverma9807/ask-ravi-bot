import os
import base64
import streamlit as st
from openai import AzureOpenAI
from streamlit.components.v1 import html as st_html  # <-- add this
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType


# --- Page setup ---
st.set_page_config(
    page_title="Ravi Verma | Career Portfolio",
    page_icon="r2.png"
)

def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_of_image("ravi-profile.jpg")

col1, col2, col3, col4 = st.columns(4)

with st.sidebar:
    st.header("Quick Questions")

    if st.button("☁️ Azure Experience"):
        st.session_state["preset_question"] = "What Azure services has Ravi worked with?"

    if st.button("🏗️ Microservices"):
        st.session_state["preset_question"] = "Tell me about Ravi's microservices experience."

    if st.button("🏆 Certifications"):
        st.session_state["preset_question"] = "What certifications does Ravi hold?"

    if st.button("🤖 Projects"):
        st.session_state["preset_question"] = "Tell me about Ravi's major projects."

st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 10px;">
        <h1 style="margin: 0;">AI-Powered Career Assistant</h1>
        <img src="data:image/png;base64,{img_base64}" style="width:55px; height:55px; 
        border-radius:50%; object-fit:cover; border:2px solid #ccc;">
    </div>
    """,
    unsafe_allow_html=True
)

st.caption("Built using Azure OpenAI and Streamlit")




#link to download resume

with st.sidebar:
    st.header("Connect")

    st.link_button(
        "LinkedIn",
        "https://www.linkedin.com/in/ravi-verma-2b757817b/"
    )

    st.link_button(
        "GitHub",
        "https://github.com/raviverma9807/"
    )

    with open("Ravi_Verma_Resume.pdf", "rb") as pdf_file:
        st.download_button(
            label="📄 Download Resume",
            data=pdf_file,
            file_name="Ravi_Verma_Resume.pdf",
            mime="application/pdf"
        )


# --- Load Azure OpenAI credentials ---
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") or st.secrets.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY") or st.secrets.get("AZURE_OPENAI_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT") or st.secrets.get("AZURE_DEPLOYMENT")

if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_KEY or not AZURE_DEPLOYMENT:
    st.error("❌ Azure OpenAI credentials not found. Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_DEPLOYMENT.")
    st.stop()

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01",
    azure_endpoint=AZURE_OPENAI_ENDPOINT)

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT") or st.secrets.get("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY") or st.secrets.get("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX") or st.secrets.get("AZURE_SEARCH_INDEX")

if not AZURE_SEARCH_ENDPOINT or not AZURE_SEARCH_KEY or not AZURE_SEARCH_INDEX:
    st.error("❌ Azure Search credentials not found. Please set AZURE_SEARCH_ENDPOINT, AZURE_SEARCH_KEY, and AZURE_SEARCH_INDEX.")
    st.stop()

search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)

)

def search_documents(query):
    try:
        results = search_client.search(
            search_text=query,
            top=3
        )

        chunks = []

        for result in results:
            chunks.append(result["chunk"])

        return "\n\n".join(chunks)

    except Exception as ex:
        return f"Search Error: {ex}"


if st.button("Test Azure Search"):
    result = search_documents("Royal Mail")
    st.text_area("Search Result", result, height=400)


# --- Resume & Personal Knowledge Base ---
facts_text = """
My name is Ravi Verma.  
I am a human, not the AI 😄 — this AI bot represents me.  

General info:
- Full Name: Ravi Verma  
- Current Location: Noida, India  
- Home Town : Lucknow
- Languages: English (Professional), Hindi (Native)  
- Hobbies: Coding, exploring AI tools, learning new technologies, and solving problems.  
- Personality: Friendly, curious, and helpful.  

Career:
- Current Role: Consultant at Capgemini India (2025–present).  
- Past Role: System Engineer at TCS (2023–2025).
- Past Role: Senior System Engineer at Infosys (2020–2023).  
- Key Skills: .NET Core, ASP.NET, C#, Minimal APIs, SQL, Microsoft Azure (Functions, Logic Apps, APIM, Blob Storage, Service Bus), Kafka, OpenTelemetry, microservices.  
- Career Goals / Future Plans : Looking to grow as a Cloud Solutions Architect and contribute to large-scale distributed systems.

Strengths:
- Strong analytical thinking, quick learner, and effective communicator.
- Experience in mentoring juniors and leading small project teams.

Projects:
- Health - US based CVS Pharmacy 
- Retail - Walmart ASDA  
- Logistics - UK based Royal Mail account
- Enery and Utilities - welsh water

AI Project:
- Developed and deployed an AI-Powered Career Assistant using Azure OpenAI and Streamlit.
- Integrated prompt engineering techniques to provide context-aware responses.
- Live Demo: https://raviverma.streamlit.app

Education:
- High School-2013 (88%) and Intermediate-2015 (88%) from Brightland Inter College Lucknow, UP and B.Tech in Computer Science from Ajay Kumar Garg Engineering College, Ghaziabad, UP (2016–2020, CGPA 8.41). 

Certifications:
-Microsoft Certified: Azure Developer Associate (AZ-204)
-Microsoft Certified: Azure Administrator Associate (AZ-104)
-Microsoft Certified: Azure Fundamentals (AZ-900) 
-Microsoft Certified: Azure AI Fundamentals (AI-900) 
 

Achievements or honors:
- Infosys Insta Award for outstanding performance.  

Social:
- LinkedIn: https://www.linkedin.com/in/ravi-verma-2b757817b/  

Github:
- https://github.com/raviverma9807/

Fun facts:
- If someone asks "Who are you?" → the answer is I’m Ravi’s digital assistant — here to share his career journey, skills, and experiences. 
- If someone asks "What's your name?" → the answer is Ravi Verma.  
- If someone asks something casual (like "ok","okk", "thanks", "bye"), respond politely in a friendly way. 
- If someone says "How are you?" → respond politely (e.g., "I’m doing well, thanks for asking!").  
- If someone asks something unrelated, reply: "I don't have that information."
"""

# --- System Prompt ---
system_prompt = f"""
You are Ravi Verma's personal AI assistant.

Rules:
1. Always answer using Ravi's information from the facts below but do not mention resumes, documents, files, or datasets. 
2. Keep answers concise, professional, and natural. Do not add closing phrases like 
   "If you have any other questions, feel free to ask."
3. If asked casual questions like "How are you?", respond politely 
   (e.g., "I’m doing well, thanks for asking!").
4. If asked "What’s your name?", answer: "My name is Ravi Verma."
5. If asked about hobbies, mention he enjoys coding, exploring AI tools, learning new technologies, 
   and solving problems.
6. If the answer is NOT in Ravi’s facts, reply: 
   "I don’t have that information. Could you rephrase or ask something else?"
7. Never repeat the same phrase in multiple answers.
8. Always answer using he or his.
9. If the user says "tell me everything" or "give me full details", 
   respond with a **comprehensive overview** including general info, 
   career, education, skills, projects, certifications, achievements, 
   social links, and hobbies all together in one answer.

📖 Ravi's Personal Facts:
{facts_text}
"""

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Explore my professional experience, Azure expertise, .NET development skills, certifications, projects, and career achievements through an AI-powered assistant built with Azure OpenAI."}
    ]

# --- Render chat messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Input & response ---

if "preset_question" not in st.session_state:
    st.session_state["preset_question"] = ""

user_input = st.chat_input(
    "Ask about my Azure experience, .NET projects, certifications, or AI solutions..."
)

if not user_input and st.session_state["preset_question"]:
    user_input = st.session_state["preset_question"]
    st.session_state["preset_question"] = ""

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            temperature=0.3,
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ]
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"⚠️ Azure OpenAI Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

