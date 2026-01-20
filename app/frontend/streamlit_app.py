# import streamlit as st
# import requests

# API_URL = "http://localhost:8000/ask"

# st.set_page_config(page_title="Clinical Guidelines Assistant")
# st.title("🩺 Clinical Guidelines Assistant")

# question = st.text_input("Ask a clinical question")

# if st.button("Ask") and question:
#     with st.spinner("Searching clinical guidelines..."):
#         response = requests.post(
#             API_URL,
#             json={"question": question}
#         )

#     if response.status_code == 200:
#         data = response.json()

#         st.markdown("### 🧠 Answer")
#         st.write(data["answer"])

#         if data["sources"]:
#             st.markdown("### 📚 Sources")
#             for src in data["sources"]:
#                 st.write(f"- {src}")
#     else:
#         st.error("API error")

import streamlit as st
import requests
from typing import List

# -----------------------------
# Configuration
# -----------------------------
API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Clinical Guidelines Assistant",
    layout="centered",
)

# -----------------------------
# UI Header
# -----------------------------
st.title("🩺 Clinical Guidelines Assistant")
st.caption(
    "Retrieval-Augmented Generation (RAG) over clinical guideline PDFs. "
    "For educational use only — not medical advice."
)

st.divider()

# -----------------------------
# User Input
# -----------------------------
question = st.text_area(
    label="Enter a clinical question",
    placeholder="What is the first-line treatment for type 2 diabetes?",
    height=100,
)

ask_button = st.button("Ask")

# -----------------------------
# Query API
# -----------------------------
if ask_button:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving guidelines and generating answer..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=60,
                )

                if response.status_code != 200:
                    st.error(f"API Error ({response.status_code})")
                    st.text(response.text)
                else:
                    data = response.json()

                    # -----------------------------
                    # Display Answer
                    # -----------------------------
                    st.subheader("📌 Answer")
                    st.write(data.get("answer", "No answer returned."))

                    # -----------------------------
                    # Display Sources
                    # -----------------------------
                    sources: List[str] = data.get("sources", [])

                    if sources:
                        st.subheader("📚 Sources")
                        for src in sources:
                            st.markdown(f"- `{src}`")
                    else:
                        st.info("No sources returned.")

            except requests.exceptions.RequestException as e:
                st.error("Failed to connect to the backend API.")
                st.text(str(e))
