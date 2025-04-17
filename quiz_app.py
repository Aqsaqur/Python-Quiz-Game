import streamlit as st
import requests

# API Endpoint
API_BASE_URL = 'http://127.0.0.1:8000/api/quizzes/'

# Function to add a new question
def add_question(quiz_id, question_text, answers):
    url = f"{API_BASE_URL}{quiz_id}/add_question/"
    data = {
        'text': question_text,
        'answers': answers
    }
    response = requests.post(url, json=data)
    return response.status_code == 201

# Function to add a new quiz
def add_quiz(title):
    url = API_BASE_URL
    data = {'title': title}
    response = requests.post(url, json=data)
    return response.json() if response.status_code == 201 else None

# Function to fetch all quizzes
def fetch_quizzes():
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Failed to fetch quizzes.')
        return []

# Function to fetch questions for a specific quiz
def fetch_question(quiz_id):
    response = requests.get(f"{API_BASE_URL}{quiz_id}/")
    if response.status_code == 200:
        return response.json().get('questions', [])
    else:
        st.error("Failed to fetch questions")
        return []

# Streamlit UI
st.title("Python Quiz")

mode = st.sidebar.selectbox("Choose Mode", ['Create Quiz', 'Add Questions', 'Play Quiz'])

# Create a new quiz
if mode == "Create Quiz":
    st.header("Generate A Quiz") 
    new_quiz_title = st.text_input("Enter Quiz Title")

    if st.button('Create Quiz'):
        if new_quiz_title.strip():
            new_quiz = add_quiz(new_quiz_title)
            if new_quiz:
                st.success(f"Quiz '{new_quiz_title}' created successfully!")
            else:
                st.error("Failed to create quiz.")
        else:
            st.error("Quiz title cannot be empty.")

# Add questions to a quiz
elif mode == "Add Questions":
    st.header("Add Questions to Quiz")
    quizzes = fetch_quizzes()

    if quizzes:
        quiz_titles = [quiz['title'] for quiz in quizzes]
        selected_quiz_title = st.selectbox("Select a Quiz", quiz_titles)
        selected_quiz = next(quiz for quiz in quizzes if quiz['title'] == selected_quiz_title)

        question_text = st.text_input("Enter the Question Text:")
        answers = []

        for i in range(4):
            answer_text = st.text_input(f"Answer {i+1} Text", key=f"answer_text_{i}")
            is_correct = st.checkbox(f"Is this the correct answer?", key=f"is_correct_{i}")
            if answer_text.strip():
                answers.append({"text": answer_text, "is_correct": is_correct})

        if st.button('Add Question'):
            if question_text.strip() and answers:
                if add_question(selected_quiz['id'], question_text, answers):
                    st.success("Question added successfully!")
                else:
                    st.error("Failed to add question.")
            else:
                st.error("Please provide question text and at least one answer.")

    else:
        st.info("No quizzes available. Please create a quiz first.")

# Play a quiz
elif mode == 'Play Quiz':
    st.header('Play Quiz')
    quizzes = fetch_quizzes()

    if quizzes:
        quiz_titles = [quiz['title'] for quiz in quizzes]
        selected_quiz_title = st.selectbox("Select a Quiz", quiz_titles)
        selected_quiz = next(quiz for quiz in quizzes if quiz['title'] == selected_quiz_title)

        questions = fetch_question(selected_quiz['id'])

        for question in questions:
            st.subheader(question['text'])
            answer_options = {ans['id']: ans['text'] for ans in question['answers']}

            selected_answer_id = st.radio(
                "Choose an answer:",
                list(answer_options.keys()),
                format_func=lambda x: answer_options[x],
                key=question['id']
            )

            if st.button('Submit Answer', key=f"submit_{question['id']}"):
                response = requests.post(
                    f"{API_BASE_URL}{selected_quiz['id']}/submit_answer/",
                    json={'question_id': question['id'], 'answer_id': selected_answer_id}
                )
                if response.status_code == 200:
                    st.success(response.json().get('result', 'No result received.'))
                else:
                    st.error("Failed to submit answer.")
    else:
        st.info("No quizzes available to play.")
