# Voice-Enabled Science Tutor (RAG Powered) 🧬

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)
![AI](https://img.shields.io/badge/AI-RAG%20%7C%20LangChain-orange?style=flat-square)
![Voice](https://img.shields.io/badge/Voice-SpeechRecognition%20%7C%20TTS-green?style=flat-square)

**Voice-Enabled Science Tutor** is an interactive AI assistant designed to answer 5th-grade science questions using voice commands. It features two different architectural approaches: a lightweight fuzzy matching system and an advanced **Retrieval-Augmented Generation (RAG)** pipeline using **LangChain** and **ChromaDB**.

The system listens to the user's voice, transcribes the query, retrieves the most relevant answer from a custom knowledge base, and responds audibly using Text-to-Speech (TTS).

---

## 🚀 Key Features

*   **🎙️ Voice Interaction:** Uses `SpeechRecognition` for input and `pyttsx3` for Turkish text-to-speech output.
*   **🧠 Hybrid Architecture:**
    *   **V1 (Lightweight):** Uses fuzzy logic (`fuzzywuzzy`) for quick Q&A matching without heavy ML models.
    *   **V2 (Advanced RAG):** Implements **LangChain**, **HuggingFace Embeddings** (BERT Turkish), and **ChromaDB** for semantic search and context-aware responses.
*   **📚 Custom Knowledge Base:** Built on a structured dataset (`data.txt`) covering topics like the Solar System, Force, and Biology.

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `assistant_v1_fuzzy.py` | Basic version using fuzzy string matching logic. |
| `assistant_v2_rag.py` | Advanced version using LangChain, Vector Store, and LLM integration. |
| `data_generator.py` | Script to generate or update the `data.txt` knowledge base. |
| `data.txt` | The raw dataset containing Q&A pairs. |

---

## 🛠 Prerequisites

### System Dependencies
You need to install **PyAudio** for microphone access.
*   **Windows:** `pip install pyaudio`
*   **Linux:** `sudo apt-get install python3-pyaudio`
*   **Mac:** `brew install portaudio && pip install pyaudio`

### Python Packages
```bash
pip install -r requirements.txt

# Option 1: Run the Fuzzy Logic Assistant (No GPU required) Best for exact match questions and low-resource environments.
python assistant_v1_fuzzy.py

#Option 2: Run the RAG Assistant (AI Powered)
#Requires an OpenAI API Key or a local LLM setup.
#Open assistant_v2_rag.py and set your API key if using OpenAI.
#Run the script:
python assistant_v2_rag.py
## Architecture (V2 - RAG)
#Ingestion: The data.txt file is loaded and split into chunks.
#Embedding: Text chunks are converted into vectors using dbmdz/bert-base-turkish-cased.
#Storage: Vectors are stored in a local ChromaDB index.
#Retrieval: The user's voice query is converted to text and used to perform a semantic similarity search.
#Generation: The retrieved context + question are sent to the LLM to generate a natural answer.
