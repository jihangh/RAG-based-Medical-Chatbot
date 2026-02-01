# 🩺 Medical Chatbot with RAG

A **Retrieval-Augmented Generation (RAG)** chatbot for general medical question answering, powered by **OpenAI GPT-5 nano** and built with **LangChain**. The system uses a **hybrid retrieval pipeline** to search trusted medical knowledge from *The Gale Encyclopedia of Medicine* and generate concise, contextual, and informative answers.

This project demonstrates how to combine modern LLMs with vector databases and hybrid retrieval to build effective medical QA systems.

---

## ⚠️ Medical Disclaimer

> **IMPORTANT:** This chatbot is designed for **informational and educational purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.

✅ This tool should be used as a **supplement**, not a replacement, for professional medical consultation.

---

## ✨ Key Features

* **🚀 Fast & Cost-Effective LLM**
  Powered by **OpenAI GPT-5 nano** for concise, efficient responses.git init

* **🧠 Hybrid Retrieval (Dense + Sparse)**
  Combines semantic embeddings with keyword-based search for higher accuracy using a tunable `alpha` score.

* **📚 Trusted Medical Knowledge Base**
  Built from *The Gale Encyclopedia of Medicine*.

* **🧩 Domain-Specific Chunking**
  Uses LangChain’s `RecursiveCharacterTextSplitter` with medical-aware chunking strategy.

* **🔍 Vector Search with Pinecone**
  Stores and retrieves medical documents efficiently at scale.

* **🧠 Caching & Reprocessing Avoidance**  
Prevents unnecessary re-ingestion using:

- **Chunk Cache**: reuse previously processed document chunks.
- **Pipeline Fingerprinting**: a SHA-256 hash over ingestion configuration (embedding model, dimensions, chunking params, index, namespace, etc.) to detect any data ingestion configuration changes.
- **`rag_state.yaml`**: This file is generated after running the app for the first time. It persists fingerprint and vector count to determine whether document embeddings have been generated before or not.

Before embedding generation, the system compares the current pipeline fingerprint and vectors count in the vector store against the saved state. If nothing has changed, vector generation and upserts are skipped.

* **🔗 API-Driven RAG Pipeline**
Modular FastAPI endpoints for ingestion and chat:

- **/rag/vectorstore**: generate and upsert embeddings

- **/rag/chat**: run the full RAG workflow

* **🖥️ Interactive UI**
  Simple and clean **Gradio** interface for real-time medical Q&A.

* **🔗 LangChain Orchestration**
  Seamlessly integrates LLMs, retrievers, embeddings, and short-term memory.

* **🗂️ Session-Based Conversational Memory**
  Maintains conversation context per user session using `langgraph.checkpoint.memory.InMemorySaver`, with the Gradio `session_id` passed as the LangGraph `thread_id` to ensure stable, multi-turn interactions.


---

## 🏗️ Architecture Overview

```
User Query
   ↓
Gradio Interface
   ↓
FastAPI (/rag/chat)
   ↓
LangChain Orchestrator
   ↓
Hybrid Retriever (Dense + Sparse)
   ↓
Pinecone Vector Database
   ↓
Context Assembly
   ↓
OpenAI GPT-5 nano
   ↓
Answer to User
```

---

## 🔧 Tech Stack

* **LLM:** OpenAI GPT-5 nano
* **Framework:** LangChain
* **Vector DB:** Pinecone
* **Embeddings:**

  * `text-embedding-3-large` (dense)
  * `pinecone-sparse-english-v0` (sparse)
* **API Layer:** FastAPI
* **Interface:** Gradio
* **Language:** Python

---

## 🎮 Demo

You can interact with the chatbot via the **Gradio interface** for real-time medical Q&A.

![Medical Chatbot Demo](assets/demo_screenshot0.PNG)
<small>Screenshot: Multi-turn conversation showing context-aware answers</small>

---

## ✅ Prerequisites

* Python **3.10+** (tested on **3.12.9**)
* OpenAI API key
* Pinecone API key

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/medical-qa-chatbot.git
cd Medical-Chatbot
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate.bat
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

---

### 5️⃣ Configure the System

Edit `config.yaml`:

```yaml
index_name: your_index_name
name_space: your_namespace
```

Feel free to adjust other parameters such as chunk size, retriever alpha, and model settings.

---

### 6️⃣ Customize the System Prompt

You can modify the behavior of the assistant in:

```
system_prompt.txt
```

This controls tone, safety, and answer formatting.

---

## 💻 Usage

Start the chatbot:

```bash
uvicorn main:app
```

The Gradio interface will be available at:

```
http://localhost:8000/ui
```

---

## ⚠️ Limitations & Considerations

### 🔧 Technical

* Answers are limited to content in *The Gale Encyclopedia of Medicine*.
* May not reflect the most recent clinical guidelines.
* Performance depends on query clarity and retrieved context quality.

### ⚖️ Ethical

* Not suitable for emergency medical situations.
* Should not be used for self-diagnosis or treatment decisions.
* Possible biases from source material.
* Human medical professional oversight is essential.
---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to fork the project and submit a PR.

---

## ⭐ Acknowledgments

* OpenAI
* LangChain
* Pinecone
* The Gale Encyclopedia of Medicine

---

Happy building! 🚀
