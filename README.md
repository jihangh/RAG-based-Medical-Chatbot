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
  Powered by **OpenAI GPT-5 nano** for concise, efficient responses.

* **🧠 Hybrid Retrieval (Dense + Sparse)**  
  Combines semantic embeddings with keyword-based search for higher accuracy using a tunable `alpha` score.

* **📚 Trusted Medical Knowledge Base**  
  Built from *The Gale Encyclopedia of Medicine*.

* **🧩 Domain-Specific Chunking**  
  Uses LangChain’s `RecursiveCharacterTextSplitter` with medical-aware chunking strategy.

* **🔍 Vector Search with Pinecone**  
  Stores and retrieves medical documents efficiently at scale.

* **🧠 Caching & Reprocessing Avoidance**  
  Avoids recomputing embeddings unless something meaningful changes.
  * **Pipeline Fingerprinting**: SHA-256 hash over ingestion configuration.  
  * **`rag_state.yaml`**: persists fingerprint and vector count.

* **🔗 API-Driven RAG Pipeline**  
  * **/rag/vectorstore**: generate and upsert embeddings  
  * **/rag/chat**: run the full RAG workflow  
  * **/rag/chathistory**: view persisted chat history

* **🖥️ Interactive UI**  
  Simple and clean **Gradio** interface for real-time medical Q&A.

* **🔗 LangChain Orchestration**  
  Seamlessly integrates LLMs, retrievers, embeddings, and short-term memory.

* **🗂️ Session-Based Conversational Memory (Persistent)**  
  Maintains conversation context per user session and **persists chat history in PostgreSQL**.  
  The Gradio `session_id` is passed as the LangGraph `thread_id`, allowing conversations to survive requests and container restarts.  
  Stored conversations can be retrieved via **/rag/chathistory**.

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
* **Database:** PostgreSQL (via Docker)  
* **Language:** Python

---

## 🎮 Demo

![Medical Chatbot Demo](assets/demo_screenshot0.PNG)  
<small>Screenshot: Multi-turn conversation showing context-aware answers</small>

---

## ✅ Prerequisites

* Docker Desktop installed and running  
* OpenAI API key  
* Pinecone API key

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/jihangh/RAG-based-Medical-Chatbot.git
cd RAG-based-Medical-Chatbot
```

---

### 2️⃣ Create `.env` file in project root

```env
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
POSTGRES_USER=yourrolename
POSTGRES_PASSWORD=yourdbpassword
POSTGRES_DB=yournameofdb
DATABASE_URL="postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}"
```

> PostgreSQL is provided automatically via Docker Compose.  
> You do **NOT** need to install PostgreSQL locally when using Docker.  
> The database hostname is internally configured as `db`.  
> `DATABASE_URL` is added in case you want to run the project locally, not on Docker.

---

### 3️⃣ Configure the System

Edit `config.yaml`:

```yaml
index_name: your_index_name
name_space: your_namespace
```

Feel free to adjust other parameters such as chunk size, retriever alpha, and model settings.

---

### 4️⃣ Customize the System Prompt

Edit:

```
system_prompt.txt
```

This controls tone, safety, and answer formatting.

---

## 💻 Usage

```bash
docker compose up --build
```

APIs: [http://localhost:8888/docs](http://localhost:8888/docs)  
UI: [http://localhost:8888/ui](http://localhost:8888/ui)

---

## 🐍 Optional: Run Without Docker

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate.bat # Windows

pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8888
```

> You must provide your own PostgreSQL instance and update the DB connection accordingly.

---

### PostgreSQL Setup (if running locally)

✅ 1. Install PostgreSQL  
🖥️ macOS  
```bash
brew install postgresql
brew services start postgresql
```

🖥️ Ubuntu / Debian  
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

🖥️ Windows  
Download from [postgresql.org](https://www.postgresql.org/download/windows/) and follow instructions.

✅ 2. Access PostgreSQL  
```bash
psql postgres
# or on macOS/Ubuntu
sudo -u postgres psql
```

✅ 3. Create Role & Database

```sql
-- Create a new user
CREATE ROLE userrole WITH LOGIN PASSWORD 'yourpassword';

-- Allow the user to create databases (optional)
ALTER ROLE userrole CREATEDB;

-- Create the app database
CREATE DATABASE nameofdb OWNER userrole;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE nameofdb TO userrole;

-- Exit
\q
```

Replace `userrole`, `yourpassword`, and `nameofdb` with your values.

---

## ⚠️ Limitations & Considerations

### 🔧 Technical

* Answers limited to *The Gale Encyclopedia of Medicine*  
* May not reflect the most recent clinical guidelines  
* Performance depends on query clarity and context quality

### ⚖️ Ethical

* Not suitable for emergency situations  
* Not for self-diagnosis or treatment decisions  
* Possible source biases  
* Human medical oversight is essential

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to fork the project and submit a PR.
