import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

# --- App Configuration ---
st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background-color: #000000;
        color: #e0e0e0; 
    }
    /* Sidebar background */
    .st-emotion-cache-16txtl3 {
        background-color: rgba(0, 0, 0, 0.2);
    }
    /* Text input boxes */
    .st-emotion-cache-133i22w {
        background-color: rgba(255, 255, 255, 0.05);
    }
    /* Primary button */
    .st-emotion-cache-1lp5q8v {
        background-color: #00bfff;
        color: white;
    }
    /* Subheaders */
    h2 {
        color: #00bfff;
    }
    /* Widget labels */
    label {
        color: white !important;
    }
    /* Hide the default status box header */
    [data-testid="stStatus"] > div:first-child {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# --- Groq API Client ---
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- Helper Functions ---
@st.cache_data
def load_gif_as_base64(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return data

def get_ai_response(resume, job_desc):
    """
    Sends the resume and job description to the Groq AI for analysis.
    """
    prompt = f"""
    You are an expert career coach and resume reviewer. Your task is to analyze a resume against a job description.

    Here is the user's resume:
    --- RESUME ---
    {resume}
    --- END RESUME ---

    Here is the job description:
    --- JOB DESCRIPTION ---
    {job_desc}
    --- END JOB DESCRIPTION ---

    Please provide the following analysis in clear, easy-to-read markdown format with sections clearly separated by horizontal rules (---):
    1.  **Overall Match Score:** Give a percentage score (e.g., 85%) representing how well the resume matches the job description and briefly explain your reasoning.
    2.  **Missing Keywords:** Identify crucial keywords and skills from the job description that are missing from the resume.
    3.  **Suggested Bullet Points:** Rewrite 2-3 bullet points from the user's resume to better align with the language and requirements of the job description.
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# --- Sidebar UI ---
with st.sidebar:
    st.header("About")
    st.info(
        "This tool helps you tailor your resume to a specific job description "
        "using the power of Large Language Models."
    )
    st.markdown("---")
    st.subheader("Connect with me:")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/aazain-irfan/)", unsafe_allow_html=True)
    st.markdown("[GitHub](https://github.com/AazainIrfan)", unsafe_allow_html=True)

# --- Main Page UI ---
st.title("🤖 AI Job Application Assistant")
st.markdown("Get instant, tailored feedback to make your application stand out.")

with st.container(border=True):
    st.subheader("📝 Paste Your Details Here")
    col1, col2 = st.columns(2)
    with col1:
        resume_text = st.text_area("Your Resume Text", height=300, label_visibility="visible")
    with col2:
        job_description = st.text_area("Job Description", height=300, label_visibility="visible")
    analyze_button = st.button("✨ Analyze My Application", type="primary", use_container_width=True)

# --- Main Logic ---
placeholder = st.empty()

if analyze_button:
    if not resume_text or not job_description:
        st.warning("Please paste both your resume and the job description.")
    else:
        with placeholder.container():
            col1, col2, col3 = st.columns([1, 1, 1]) 
            with col2:
                gif_data = load_gif_as_base64("loader.gif")
                st.markdown(
                    f'<img src="data:image/gif;base64,{gif_data}" width="300">',
                    unsafe_allow_html=True,
                )

        ai_feedback = get_ai_response(resume_text, job_description)

        placeholder.empty()
        st.subheader("🤖 Your AI-Powered Feedback")
        with st.expander("**Click here to see the analysis**", expanded=True):
            st.markdown(ai_feedback)