# Grand Nexus Mall - Smart Concierge Chatbot

Welcome to the **Grand Nexus Mall Concierge**, an intelligent, conversational AI assistant designed to help mall visitors navigate the premises, find food options, discover discounts, and access mall services.

## 📖 Project Overview
This project was built utilizing the Retrieval-Augmented Generation (RAG) architectural pattern on Microsoft Azure. It started as a fork of the Microsoft "Serverless Azure OpenAI & AI Search" template (originally an HR Assistant) and was heavily customized to fit our retail/mall persona.

### How We Developed It
1. **Persona Pivot**: we shifted the AI's "brain" by rewriting the system prompts in `app/backend/approaches/prompts/chat_answer.system.jinja2`. The chatbot was instructed to act as an enthusiastic "Shopping Mall Concierge", completely changing the tone and context of its answers.
2. **UI Revamp**: We updated the default React frontend questions in `translation.json` to showcase mall-specific examples (e.g., "Where is the nearest food court?", "Which stores have seasonal sales?").
3. **Data Cleanup & Re-ingestion**: We wiped the default Northwind HR documents from our Azure AI Search database and uploaded our custom 600KB+ `fake_mall_dataset.pdf` containing store directories, floor plans, and service hours.
4. **Overcoming Cloud Quotas**: Due to running on an Azure Free Trial account with a strict 1,000 Tokens-Per-Minute (TPM) limit, the massive dataset initially crashed the data upload pipeline. To fix this, we modified the `OpenAIEmbeddings` class (down-throttling batch sizes from 16 to 2 and increasing exponential backoff retry patience up to 120 seconds).
5. **Accuracy Tuning**: We resolved the "I don't know" generic responses by enforcing **Semantic Ranking** natively in the Backend Approach layer and increasing the context retrieval window (chunks) from 7 to 10 to guarantee comparative queries (Store A vs Store B) had sufficient context space.

## ☁️ Azure Resources Used
This application lives entirely within the Azure cloud ecosystem using the following managed services:

* **Azure App Service (Compute):** Hosts our live web server. The backend is powered by Python (using the Quart async framework), and the frontend is a modern React/Vite Single Page Application.
* **Azure Document Intelligence:** The powerhouse behind our data intake. When we upload mall PDFs, this service meticulously scans the layout to properly digitize tables, headers, and paragraphs before it gets sent to the AI.
* **Azure OpenAI (Embeddings Model):** Translates our text chunks into "Vectors" (mathematical arrays) so that the search engine can understand the semantic meaning of the words, not just exact keyword matches.
* **Azure OpenAI (GPT Model):** The "brain" of the chatbot. It ingests the user's question along with the relevant text snippets retrieved from the database and constructs a polite, human-like response honoring the Concierge persona.
* **Azure AI Search:** Our Vector Database. It stores the text chunks and their vector meanings, and efficiently executes Hybrid Searches (Keyword + Vector) when a user asks a question to find the most relevant document sections in milliseconds.
* **Azure Blob Storage:** Acts as our secure filing cabinet. It stores the original uploaded PDF files so that the Web UI can retrieve and display the exact source page in the "Citation" tab for user verification.

## ⚙️ Project Flow (The RAG Architecture)
Our application separates "Knowledge" from "Logic" by leveraging the **Chat-Read-Retrieve-Read** pattern.

1. **Ask (The User):** The user types a question like, *Where is the exit on the second floor?*
2. **Translate to Query (GPT):** The Python backend forwards the chat history and the user's question to Azure OpenAI to generate an optimized search query.
3. **Retrieve Information (AI Search):** The backend queries the Azure AI Search index using the generated query. Azure AI Search returns the top 10 most relevant text chunks from our mall PDF.
4. **Read & Synthesize (GPT):** The Python backend formats a final prompt containing the System Persona, the retrieved chunks, and the user's question, sending it to Azure OpenAI one last time.
5. **Answer:** OpenAI generates the natural language response, automatically appending citation tags (e.g., `[fake_mall_dataset.pdf#page=1]`), which the React frontend parses to display clickable link citations. 


