# MediBot-

# 🩺 RAG-Based Medical Chatbot

An AI-powered **offline medical chatbot** built using **Retrieval-Augmented Generation (RAG)**.  
This system retrieves relevant medical information from documents and generates accurate answers using a local language model.

---

## 🚀 Features

- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 Context-aware responses using FAISS
- 📚 Supports custom medical PDFs
- 🔒 Fully offline (No API required)
- 💬 Chat UI using Flask
- ⚡ Fast local processing
- 🎯 Improved accuracy (reranking + query expansion)

---

## 🏗️ Architecture


---

## 🛠️ Tech Stack

- **Language:** Python  
- **Backend:** Flask  
- **AI Framework:** LangChain  
- **Vector Database:** FAISS  
- **Embeddings:** Sentence Transformers  
- **LLM:** FLAN-T5 (HuggingFace)  
- **Frontend:** HTML, CSS, JavaScript  

---

## 📂 Project Structure
Medical-Chatbot/
│
├── app.py
├── store_index.py
├── requirements.txt
├── data/
├── faiss_index/
├── src/
│ └── helper.py
├── templates/
│ └── index.html
└── README.md


---

## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/medical-chatbot.git
cd medical-chatbot

### 2️⃣ Create Virtual Environment
python -m venv myenv
myenv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt