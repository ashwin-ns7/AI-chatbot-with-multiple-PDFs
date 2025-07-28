import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmltemps import css, bot_template, user_template
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Step 1: Extract Text from PDFs
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            extracted = page.extract_text() or ""
            text += extracted
    return text

# Step 2: Chunk the Text
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Step 3: Generate Embeddings and Create Vector Store
def get_vectorstore(text_chunks):
    st.write("🔍 Generating embeddings with OpenAI...")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    st.success("✅ FAISS vector store created!")
    return vectorstore

# Step 4: Setup LLM and Retrieval Chain
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

# Step 5: Ask Questions
def handle_userinput(user_question):
    st.write(f"🗨️ User Question: {user_question}")
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, msg in enumerate(st.session_state.chat_history):
        tmpl = user_template if i % 2 == 0 else bot_template
        st.write(tmpl.replace("{{MSG}}", msg.content), unsafe_allow_html=True)

# Step 6: Main UI
def main():
    st.set_page_config(page_title="Chat with Multiple PDFs", page_icon="📚")
    st.write(css, unsafe_allow_html=True)
    st.header("📚 Chat with Multiple PDFs")

    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("📄 Upload Documents")
        pdf_docs = st.file_uploader("Upload PDFs and click 'Process'", accept_multiple_files=True)

        if st.button("Process"):
            if not pdf_docs:
                st.warning("❗ Please upload at least one PDF.")
                return

            with st.spinner("🔄 Processing..."):
                # Step 1
                raw_text = get_pdf_text(pdf_docs)
                st.write("### ✅ Extracted PDF Text:")
                st.code(raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text)

                # Step 2
                text_chunks = get_text_chunks(raw_text)
                st.write(f"### 📚 Text Chunks ({len(text_chunks)} chunks):")
                st.code(text_chunks[:3])

                # Step 3 & 4
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

if __name__ == "__main__":
    main()
