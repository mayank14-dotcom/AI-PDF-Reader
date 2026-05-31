import streamlit as st
from pdf_reader import extract_text_from_pdf
from vector_store import create_vector_store
from chatbot import get_answer

st.set_page_config(
    page_title="Chat With PDF",
    page_icon="📄"
)

st.title("📄 Chat With PDF")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)

    st.success("PDF Uploaded Successfully")
    st.subheader("Extracted Text")
    st.text_area(
        "PDF Content",
        text,
        height=400
    )

    if "vector_store" not in st.session_state or st.session_state.get("pdf_name") != uploaded_file.name:
        with st.spinner("Building PDF embeddings..."):
            st.session_state.vector_store = create_vector_store(text)
            st.session_state.pdf_name = uploaded_file.name

    question = st.text_input("Ask a question about this PDF", key="question_input")

    if st.button("Get Answer"):
        if not question.strip():
            st.warning("Please enter a question before asking.")
        else:
            with st.spinner("Generating answer..."):
                try:
                    answer = get_answer(question, st.session_state.vector_store)
                except Exception as exc:
                    st.error(f"AI error: {exc}")
                else:
                    st.subheader("AI Answer")
                    st.write(answer)
else:
    st.info("Please upload a PDF to continue.")