import base64
import streamlit as st

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()


def render_header():
    img_base64 = get_base64_image("images/ravi-profile.jpg")

    st.markdown(
        f"""
<div style="text-align:center;padding:10px 0 15px 0;">
    <img src="data:image/jpeg;base64,{img_base64}" width="100" height="100" style="border-radius:50%;object-fit:cover;border:3px solid #d9d9d9;" />
    <h1>Ask Ravi</h1>
    <h3>AI-Powered Professional Portfolio</h3>
    <p>Built with Azure OpenAI • Azure AI Search • RAG</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.caption("Built using Azure OpenAI, Azure AI Search and Streamlit")

def render_sidebar():
    with st.sidebar:

        st.header("Quick Questions")

        questions = {
            "☁️ Azure Experience":
                "What Azure services has Ravi worked with?",

            "🏗️ Microservices":
                "Tell me about Ravi's microservices experience.",

            "🚀 Projects":
                "Tell me about Ravi's major projects.",

            "🏆 Certifications":
                "What Microsoft certifications does Ravi hold?",

            "🤖 AI Project":
                "Tell me about Ravi's AI-powered career assistant."
        }

        for title, question in questions.items():
            if st.button(title, use_container_width=True):
                st.session_state["preset_question"] = question

        st.divider()

        st.header("Connect")

        st.link_button(
            "LinkedIn",
            "https://www.linkedin.com/in/ravi-verma-2b757817b/",
            use_container_width=True
        )

        st.link_button(
            "GitHub",
            "https://github.com/raviverma9807/",
            use_container_width=True
        )

        with open("resume/Ravi_Verma_Resume.pdf", "rb") as pdf:
            st.download_button(
                "📄 Download Resume",
                pdf,
                file_name="Ravi_Verma_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )


def render_sources(sources):
    if not sources:
        return

    with st.expander("📚 Sources"):
        for source in sorted(set(sources)):
            st.write(f"• {source}")