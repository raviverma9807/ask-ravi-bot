import base64
import streamlit as st

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()


def render_header():
    img_base64 = get_base64_image("images/ravi-profile.jpg")

    st.markdown(
        f"""
        <div style="display:flex;align-items:center;justify-content:space-between;">
            <h1 style="margin:0;">Ask Ravi</h1>
            <img src="data:image/jpeg;base64,{img_base64}"
                 style="width:55px;height:55px;border-radius:50%;
                 border:2px solid #ccc;object-fit:cover;">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="margin-top:-8px;margin-bottom:8px;font-size:18px;color:#666;font-weight:500;">
            AI-Powered Professional Portfolio
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Built using Azure OpenAI, Azure AI Search and Streamlit")


def render_sidebar():
    with st.sidebar:

        col1, col2 = st.columns(2)

        # -----------------------------
        # Quick Questions
        # -----------------------------
        with col1:
            st.subheader("Quick Questions")

            questions = {
                "☁️ Azure":
                    "Provide a comprehensive summary of Ravi's Azure experience.",

                "🏗️ Microservices":
                    "Tell me about Ravi's microservices experience.",

                "🚀 Projects":
                    "Tell me about Ravi's major projects.",

                "🏆 Certifications":
                    "What Microsoft certifications does Ravi hold?",

                "🤖 AI Projects":
                    "Tell me about Ravi's AI-powered projects.",

                "💼 Experience":
                    "Provide a summary of Ravi's work experience.",

                "🎓 Education":
                    "Provide info about Ravi's educational background."
            }

            for title, question in questions.items():
                if st.button(title, key=title, use_container_width=True):
                    st.session_state["preset_question"] = question

        # -----------------------------
        # Connect
        # -----------------------------
        with col2:
            st.subheader("Connect")

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
                    "⬇️ Resume",
                    pdf,
                    file_name="Ravi_Verma_Resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )