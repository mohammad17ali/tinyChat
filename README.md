# tinyChat
A simple RAG powered chatbot, built on TinyLlama 1.1B, using FAISS for similarity search in the vector database. 

## Architecture
```
┌───────────────┐     ┌────────────────┐     ┌──────────────────────┐
│  Flutter App  │◄────┤   API Server   │◄────┤    tinyChat Engine   │
│  (Frontend)   │────►│   (Backend)    │────►│    (Your Model)      │
└───────────────┘     └────────────────┘     └──────────────────────┘
                             │                          │
                             ▼                          ▼
                      ┌──────────────┐          ┌───────────────┐
                      │  Auth/User   │          │ Vector DB     │
                      │  Database    │          │ (FAISS/Milvus)│
                      └──────────────┘          └───────────────┘

```
