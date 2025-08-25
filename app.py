import os
import base64
import streamlit as st
from openai import AzureOpenAI

# --- Page setup ---
st.set_page_config(page_title="Chat with Ravi 🤖", page_icon="🤖")

def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
img_base64 = get_base64_of_image("ravi-profile.jpg")

st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 10px;">
        <h1 style="margin: 0;">Ask me</h1>
        <img src="data:image/png;base64,{img_base64}"  style="width:55px; height:55px; 
        border-radius:50%; object-fit:cover; border:2px solid #ccc;">
    </div>
    """,
    unsafe_allow_html=True
)


st.caption("Powered by Azure OpenAI · Ask me about Ravi")

# --- Load Azure OpenAI credentials ---
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT") or st.secrets.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY") or st.secrets.get("AZURE_OPENAI_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT") or st.secrets.get("AZURE_DEPLOYMENT")

if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_KEY or not AZURE_DEPLOYMENT:
    st.error("❌ Azure OpenAI credentials not found. Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_DEPLOYMENT.")
    st.stop()

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01",   # latest Azure API version
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# --- Resume & Personal Knowledge Base ---
facts_text = """
My name is Ravi Verma.  
I am a human, not the AI 😄 — this AI bot represents me.  

General info:
- Full Name: Ravi Verma  
- Current Location: Noida, India  
- Languages: English (Professional), Hindi (Native)  
- Hobbies: Coding, exploring AI tools, learning new technologies, and solving problems.  
- Personality: Friendly, curious, and helpful.  

Career:
- Current Role: Consulatnt at Capgemini India (2025–present).  
- Past Role: System Engineer at TCS (2023–2025).
- Past Role: Senior System Engineer at Infosys (2020–2023).  
- Key Skills: .NET Core, ASP.NET, C#, Minimal APIs, SQL, Microsoft Azure (Functions, Logic Apps, APIM, Blob Storage, Service Bus), Kafka, OpenTelemetry, microservices.  

Projects:
- Health - US based CVS Pharmacy 
- Retail - Walmart ASDA  
- Logistics - UK based Yoyal Mail account
- Enery and Utilities - welsh water

Education:
- High School-2013 (88%) and Intermediate-2015 (88%) from Brightland Inter College Lko and B.Tech in Computer Science from Ajay Kumar Garg Engineering College, Ghaziabad (2016–2020, CGPA 8.41). 

Certifications:
- Microsoft Azure Fundamentals (2022)  
- Microsoft Azure AI Fundamentals (2022) 
- Microsoft Azure Developer Associate (2025)  

Achievements:
- Infosys Insta Award for outstanding performance.  

Social:
- LinkedIn: https://www.linkedin.com/in/ravi-verma-2b757817b/  

Fun facts:
- If someone asks "What's your name?" → the answer is Ravi Verma.  
- If someone says "How are you?" → respond politely (e.g., "I’m doing well, thanks for asking!").  
- If someone asks something unrelated to my resume, the bot should reply: "I don't know."
"""

# --- System Prompt ---
system_prompt = f"""
You are Ravi Verma's personal AI assistant.

📌 Rules:
1. Always answer using Ravi's information from the resume and personal facts below.
2. Keep answers **concise, professional, and natural**. Do not add closing phrases like 
   "If you have any other questions, feel free to ask."
3. If asked casual questions like "How are you?", respond politely 
   (e.g., "I’m doing well, thanks for asking!").
4. If asked "What’s your name?", answer: "My name is Ravi Verma."
5. If asked about hobbies, mention Ravi enjoys coding, exploring AI tools, learning new technologies, 
   and solving problems.
6. If the answer is NOT in Ravi’s resume or facts, reply: 
   "I don’t have that information. Could you rephrase or ask something else?"
7. Never repeat the same phrase in multiple answers.

📖 Resume & Personal Facts:
{facts_text}
"""


# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm Ravi's assistant 🤖. Ask me anything about Ravi's background, skills, or career."}
    ]

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---
if user_input := st.chat_input("Ask me something..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,   # your deployment name (e.g., gpt-35-turbo)
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
