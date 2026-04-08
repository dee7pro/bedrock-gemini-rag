# 🔥 Enterprise Knowledge Base Q&A System

This project is a **Retrieval-Augmented Generation (RAG)** application that combines:

* **Amazon Bedrock Knowledge Base** for context retrieval
* **Google Gemini 2.5 Flash** for response generation
* **Streamlit** for an interactive chat interface

It answers user queries based on a custom knowledge base (PDF), ensuring **context-aware and accurate responses**.

---

## 🧠 How It Works

1. User enters a question
2. Amazon Bedrock retrieves relevant context from the knowledge base
3. Context is passed to Gemini
4. Gemini generates a grounded response

---

<h3>App Screenshots</h3>
<div style="display:flex; gap:10px; flex-wrap:wrap;">
<img width="300" alt="Screenshot 1" src="https://github.com/dee7pro/bedrock-gemini-rag/blob/c61cecece7415282a36f9ec712902ae937eb2015/assets/2.png" />
<img width="300" alt="Screenshot 2" src="https://github.com/dee7pro/bedrock-gemini-rag/blob/c61cecece7415282a36f9ec712902ae937eb2015/assets/1.png" />
<img width="300" alt="Code Screenshot" src="https://github.com/dee7pro/bedrock-gemini-rag/blob/c61cecece7415282a36f9ec712902ae937eb2015/assets/4.png" />

</div>

## 🛠️ Tech Stack

| Layer                  | Technology                    |
| ---------------------- | ----------------------------- |
| LLM                    | Gemini 2.5 Flash              |
| Retrieval              | Amazon Bedrock Knowledge Base |
| Framework              | Boto3 (AWS SDK)               |
| UI                     | Streamlit                     |
| Backend                | Python                        |
| API Handling           | Requests                      |
| Environment Management | Python Dotenv                 |
| Cloud                  | AWS EC2                       |
| Authentication         | IAM Role (AWS)                |
| Data Source            | PDF Knowledge Base            |


---

## 📂 Project Structure

```
.
├── app1.py              # Main Streamlit application
├── tribe_finale.pdf     # Knowledge base document
├── .env                 # Environment variables (not pushed to Git)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/dee7pro/bedrock-gemini-rag.git
cd bedrock-gemini-rag
```

---

### 2. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
```

---

### 3. Install Dependencies

```
pip install streamlit boto3 requests python-dotenv
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```
gemini_key=YOUR_GEMINI_API_KEY
KNOWLEDGE_BASE_ID=YOUR_BEDROCK_KB_ID
AWS_REGION=us-east-1
```

> ⚠️ Do NOT commit `.env` to GitHub

---

## ☁️ AWS Setup (Important)

* Deploy app on EC2
* Attach IAM Role with:

```
AmazonBedrockFullAccess
```

> No need to store AWS keys in `.env`

---

## ▶️ Run the Application

```
streamlit run app1.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🌐 Access the App

```
http://98.88.22.215:8501
```

---

## ✨ Features

* Context-aware Q&A
* PDF-based knowledge retrieval
* Secure IAM-based authentication
* Clean chat UI
* Error handling for API limits

---

## 🔐 Security Best Practices

* Never expose API keys
* Use IAM roles instead of AWS keys
* Keep `.env` in `.gitignore`

---

## 🚀 Future Improvements

* Chat history memory
* UI enhancements
* Domain + HTTPS deployment
* CI/CD automation

## 👨‍💻 Author

**Deepika A** — Gen AI Engineer  

## License
MIT License © 2026 dee7pro
