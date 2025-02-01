import streamlit as st
import json
from supabase import create_client

# ✅ Correct Python Syntax for Supabase Client
SUPABASE_URL = st.secrets["https://trdfbxqjtwbpardosclu.supabase.co'"]
SUPABASE_KEY = st.secrets["process.env.SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to register a user
def register_user(name, email, password):
    response = supabase.auth.sign_up({"email": email, "password": password})
    
    # ✅ Corrected error handling
    if response and "user" in response:
        supabase.table("users").insert({"name": name, "email": email}).execute()
        st.success("✅ Account Created! Proceed to the psychological test.")
        return True
    else:
        st.error("❌ Error creating account. Email may already exist.")
        return False

# Function to store answers
def save_answers(email, answers):
    supabase.table("users").update({"answers": json.dumps(answers)}).eq("email", email).execute()
    st.success("✅ Answers saved! Proceed to qualities ranking.")

# Function to rank qualities
def save_qualities(email, qualities):
    supabase.table("users").update({"qualities": json.dumps(qualities)}).eq("email", email).execute()
    st.success("✅ Your profile is complete! Finding a match...")

# Streamlit UI
st.title("💖 Soulfriend Finder")

# Step 1: Signup
with st.form("signup_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit_signup = st.form_submit_button("Sign Up")

if submit_signup:
    if register_user(name, email, password):
        st.session_state["email"] = email

# Step 2: Psychological Questions
if "email" in st.session_state:
    st.subheader("🧠 Psychological Test")

    questions = [
        "Do you prefer deep conversations or lighthearted fun?",
        "Are you an introvert or extrovert?",
        "How do you handle conflict in a relationship?",
        "What is your ideal way to spend a weekend?",
        "Do you believe in soulmates?",
        "How important is shared humor in a friendship?",
        "What is your biggest fear in a friendship?",
        "How do you show appreciation to a friend?",
        "What is a deal-breaker for you in a friendship?",
        "How do you handle disagreements?"
    ]

    answers = {}
    for i, question in enumerate(questions):
        answers[f"Q{i+1}"] = st.radio(question, ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"])

    if st.button("Submit Answers"):
        save_answers(st.session_state["email"], answers)

# Step 3: Ranking Qualities
if "email" in st.session_state and "answers" in locals():
    st.subheader("⭐ Rank the qualities you want in a soulfriend")

    qualities = ["Loyalty", "Humor", "Empathy", "Adventurousness", "Honesty"]
    rankings = {q: st.slider(q, 1, 5, 3) for q in qualities}

    if st.button("Save Preferences"):
        save_qualities(st.session_state["email"], rankings)

