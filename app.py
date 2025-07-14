import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- App Configuration ---
st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="📄",
    layout="wide"
)

# --- Groq API Client ---
# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# --- AI Function ---
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

    Please provide the following analysis in clear, easy-to-read markdown format:
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
            model="llama3-8b-8192", # A fast and capable model
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"


# --- UI Elements ---
st.title("📄 AI-Powered Job Application Assistant")
st.markdown("Paste your resume and a job description below to get tailored feedback.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Resume Text")
    resume_text = st.text_area("Paste your full resume here.", height=300, label_visibility="collapsed")

with col2:
    st.subheader("Job Description")
    job_description = st.text_area("Paste the full job description here.", height=300, label_visibility="collapsed")

analyze_button = st.button("✨ Analyze My Application", type="primary")

# --- Main Logic ---
if analyze_button:
    if not resume_text or not job_description:
        st.warning("Please paste both your resume and the job description.")
    else:
        # Show a spinner while the AI is working
        with st.spinner("Analyzing... please wait. This may take a moment."):
            ai_feedback = get_ai_response(resume_text, job_description)
            st.markdown("---")
            st.subheader("🤖 Your AI-Powered Feedback")
            st.markdown(ai_feedback)