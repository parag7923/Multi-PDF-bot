import streamlit as st
from main import process_pdf, generate_answer
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="AI PDF Chatbot", page_icon="📄", layout="wide")

st.markdown("""
    <style>
        .main {background-color: #f5f7fa;}
        h1 {color: #007bff; text-align: center;}
        .stButton button {background-color: #007bff; color: white; border-radius: 10px;}
        .stTextInput input {border-radius: 10px;}
        .chat-container {height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; background-color: white;}
        .user-question {font-size: 18px; font-weight: bold; color: white; background-color: #007bff; padding: 10px; border-radius: 10px;}
        .ai-answer {font-size: 16px; color: white; background-color: #28a745; padding: 10px; border-radius: 10px; margin-top: 5px;}
    </style>
""", unsafe_allow_html=True)

st.title('📄 AI-Powered PDF Chatbot')
st.write('Upload a PDF and ask questions about its content. Get quick and accurate answers using AI.')

# Sidebar with Upload and Instructions
with st.sidebar:
    st.header("Upload your PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    st.info("Supported Format: PDF. The chatbot will analyze your document to generate relevant answers.")

# Initialize Chat History
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.db = None

# Process PDF
if uploaded_file is not None and st.session_state.db is None:
    with st.spinner('Processing PDF... Please wait.'):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.db = process_pdf("temp.pdf")
        st.success("PDF Uploaded and Processed Successfully!")

    st.session_state.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key="AIzaSyBpZUY9sQrxkPFc64bVlkaO8D-K0s84KlY")

# Chat Section
if st.session_state.db is not None:
    st.subheader("💬 Chat with your PDF")

    # Chat History Display (Maintaining natural flow)
    st.markdown("### Chat History")
    with st.container():
        for i, (question, answer) in enumerate(st.session_state.chat_history, 1):
            st.markdown(f"<p class='user-question'>🧑 Question {i}: {question}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='ai-answer'>🤖 AI: {answer}</p>", unsafe_allow_html=True)
            st.markdown("---")

    # Query Input
    if 'user_query' not in st.session_state:
        st.session_state.user_query = ""

    query = st.text_input("Enter your query about the PDF:", value=st.session_state.user_query, key='user_query_input')

    col1, col2 = st.columns([1, 0.2])

    if col1.button('Get Answer') and query.strip():
        with st.spinner('Generating Answer...'):
            result = generate_answer(query, st.session_state.db, st.session_state.llm)
            st.session_state.chat_history.append((query, result))
            st.session_state.user_query = query
            st.rerun()

    if col2.button('Clear Input'):
        st.session_state.user_query = ""
        st.rerun()
else:
    st.warning("Please upload a PDF to proceed.")
