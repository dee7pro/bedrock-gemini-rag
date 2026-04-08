import os
import boto3
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("gemini_key")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

if not GEMINI_API_KEY:
    st.error("Please set gemini_key in your .env file.")
    st.stop()

if not KNOWLEDGE_BASE_ID:
    st.error("Please set KNOWLEDGE_BASE_ID in your .env file.")
    st.stop()

st.set_page_config(page_title="Bedrock KB + Gemini Chat", page_icon="💬", layout="centered")

# ---------------- Sidebar: About + KB PDF ----------------
with st.sidebar:
    st.header("About")
    st.markdown("""
    **Bedrock KB + Gemini Chat** is a demo app that:
    - Retrieves context from your Amazon Bedrock Knowledge Base
    - Generates answers using Google Gemini 2.5 Flash
    - Provides context-aware responses to your questions
    
    **Instructions:**
    1. Enter a question in the input box
    2. Click "Ask" to get an AI-generated answer
    3. Expand "Retrieved Context" to see supporting information

    **Developed by:** deepika
    """)

    st.header("Knowledge Base PDF")
    pdf_file_path = "tribe_finale.pdf"
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, "rb") as f:
            PDFbyte = f.read()
        st.download_button(
            label="Download KB PDF",
            data=PDFbyte,
            file_name="Knowledge_Base.pdf",
            mime="application/pdf"
        )
        st.markdown("Preview not supported in sidebar. Download to view full KB.")
    else:
        st.info("No KB PDF uploaded. Place your trained KB PDF as 'trained_kb.pdf'.")

# ---------------- Main Interface ----------------
st.markdown("<h1 style='text-align:center;'>Enterprise Knowledge Base Q&A System</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#555;'>Powered by Amazon Bedrock Knowledge Bases and Gemini</p>",
    unsafe_allow_html=True
)

# ---------------- Chat CSS ----------------
st.markdown("""
<style>
.chat-container {
    max-width: 700px;
    margin: auto;
}
.chat-row {
    display: flex;
    margin: 10px 0;
}
.user {
    justify-content: flex-end;
}
.bot {
    justify-content: flex-start;
}
.bubble {
    padding: 12px 14px;
    border-radius: 12px;
    max-width: 75%;
    font-size: 15px;
    line-height: 1.5;
}
.user-bubble {
    background-color: #2563eb;
    color: white;
}
.bot-bubble {
    background-color: #f3f4f6;
    color: #111827;
}
.block-container {
    padding-bottom: 80px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Input ----------------
col1, col2 = st.columns([8,1])

with col1:
    question = st.text_input("Ask something...", label_visibility="collapsed")

with col2:
    send = st.button("➤")

# ---------------- Session ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "context" not in st.session_state:
    st.session_state.context = ""

# ---------------- Ask ----------------
if send and question.strip():
    try:
        bedrock = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

        kb_response = bedrock.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": question},
            retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 5}},
        )

        chunks = [
            item.get("content", {}).get("text", "")
            for item in kb_response.get("retrievalResults", [])
            if item.get("content", {}).get("text")
        ]

        context = "\n\n".join(chunks) if chunks else "No context retrieved from KB."

        # ✅ store context safely
        st.session_state.context = context

        # ✅ Context limit
        MAX_CONTEXT_LENGTH = 4000
        if len(context) > MAX_CONTEXT_LENGTH:
            context = context[:MAX_CONTEXT_LENGTH] + "\n\n[Context truncated]"
            st.session_state.context = context

        # ✅ Casual fallback
        if question.lower() in ["hi", "hello", "hey"]:
            answer_text = "Hey! 👋 How can I help you today?"

        else:
            prompt = f"""
Answer ONLY from the context below.
If answer not found, say "Not available in knowledge base".

Context:
{context}

Question:
{question}
"""

            gemini_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "maxOutputTokens": 3000
                }
            }

            r = requests.post(gemini_endpoint, headers=headers, json=payload)
            response_json = r.json()

            # ✅ Error handling
            if "error" in response_json:
                error_msg = str(response_json["error"])

                if "quota" in error_msg.lower() or "RESOURCE_EXHAUSTED" in error_msg:
                    answer_text = "⚠️ Token limit / quota exceeded. Try again later."

                elif "PERMISSION_DENIED" in error_msg:
                    answer_text = "⚠️ API key issue. Please generate a new key."

                else:
                    answer_text = f"⚠️ Gemini Error:\n{error_msg}"

            else:
                answer_text = response_json["candidates"][0]["content"]["parts"][0]["text"]

        st.session_state.chat_history.append({"role": "user", "message": question})
        st.session_state.chat_history.append({"role": "gemini", "message": answer_text})

    except Exception as e:
        st.error(f"Error: {str(e)}")

# ---------------- Display Chat ----------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for chat in st.session_state.chat_history:
    msg = chat["message"].replace("\n", "<br>")

    if chat["role"] == "user":
        st.markdown(f"""
        <div class="chat-row user">
            <div class="bubble user-bubble">{msg}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-row bot">
            <div class="bubble bot-bubble">{msg}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Display Retrieved Context ----------------
if st.session_state.chat_history:
    with st.expander("Retrieved Context from KB"):
        st.write(st.session_state.context)