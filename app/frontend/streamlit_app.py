import streamlit as st
import requests

API_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="Clinical Guidelines Assistant")
st.title("🩺 Clinical Guidelines Assistant")

question = st.text_input("Ask a clinical question")

if st.button("Ask") and question:
    with st.spinner("Searching clinical guidelines..."):
        response = requests.post(
            API_URL,
            json={"question": question}
        )

    if response.status_code == 200:
        data = response.json()

        st.markdown("### 🧠 Answer")
        st.write(data["answer"])

        if data["sources"]:
            st.markdown("### 📚 Sources")
            for src in data["sources"]:
                st.write(f"- {src}")
    else:
        st.error("API error")

