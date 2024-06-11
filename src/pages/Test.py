import streamlit as st
from QnA import extract_text_from_pdf, generate_questions, evaluate_answer


# Streamlit app
st.title("Test 🤫")

# File upload
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job description input
job_description = st.text_area("Job Description", "Enter the job description here...")


if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Resume Text", resume_text, height=300)

    if st.button("Generate Questions"):
        st.session_state.questions = generate_questions(job_description, resume_text)
        st.session_state.answers = [""] * len(st.session_state.questions)

if "questions" in st.session_state:
    st.subheader("Generated Questions")
    for i, question in enumerate(st.session_state.questions, 1):
        st.text_area(f"Question {i}", question, key=f"question_{i}", height=100, disabled=True)
        st.session_state.answers[i-1] = st.text_input(f"Your Answer {i}", st.session_state.answers[i-1], key=f"answer_{i}")

    if st.button("Submit Answers"):
        scores = []
        for i, (question, answer) in enumerate(zip(st.session_state.questions, st.session_state.answers), 1):
            score = evaluate_answer(question, answer)
            scores.append((question, answer, score))
        
        st.subheader("Evaluation Results")
        for i, (question, answer, score) in enumerate(scores, 1):
            st.write(f"**Question {i}:** {question}")
            st.write(f"**Your Answer:** {answer}")
            st.write(f"**Score:** {score}")
            st.write("\n*************\n")