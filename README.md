# VoiceQuery AI

VoiceQuery AI is a full-stack AI-powered analytics platform that converts natural language and voice inputs into SQL queries, executes them on a PostgreSQL database, and returns structured results with visualizations and AI-generated insights.

The system is designed to simplify data access for non-technical users while maintaining flexibility for advanced analytics workflows.

---

# LINKS:
Backend - https://voicequery-ai.onrender.com/docs/
Frontend - https://voice-query-frontend.vercel.app/


## Features

### Natural Language to SQL
Users can input business questions in plain English, which are converted into executable SQL queries using large language models.

### Voice Input Interface
Supports browser-based speech recognition for converting voice input into text queries.

### Query Execution Engine
Generated SQL queries are validated and executed against a PostgreSQL database.

### Interactive Analytics Dashboard
Provides key metrics such as:
- Total queries
- Average execution time
- Total rows processed
- Query activity trends
- Most frequently used queries

### Data Visualization
Query results are automatically rendered into interactive charts for better interpretation of data.

### AI Insights Layer
Generates business-focused insights from query results, highlighting patterns, trends, and anomalies.

### Query History
Stores and displays previously executed queries with execution metrics and timestamps.

### Export Functionality
Supports exporting query results in CSV and PDF formats.

### Authentication System
Implements JWT-based authentication with role-based access control for users and administrators.

---

## System Architecture

User Input (Text / Voice)  
→ Language Model (Groq LLM)  
→ SQL Generation Layer  
→ PostgreSQL Database  
→ Query Execution Engine  
→ Results Processing Layer  
→ Visualization + AI Insights  
→ Frontend Dashboard

---

## Tech Stack

Frontend:
- Next.js
- TypeScript
- Tailwind CSS
- Recharts

Backend:
- FastAPI
- Python
- SQLAlchemy
- Alembic

AI Layer:
- Groq API (LLaMA models)

Database:
- PostgreSQL

Authentication:
- JWT

Voice Processing:
- Web Speech API

Deployment:
- Frontend: Vercel 
- Backend: Render

---

## Project Structure

voicequery-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── services/
│   │   ├── db/
│   │   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── lib/
│
└── README.md

---

## Example Workflow

Input:
Show top products by revenue

Generated SQL:
SELECT product, SUM(revenue) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;

Output:
- Tabular results
- Visual chart representation
- AI-generated insights
- Export options

---

## Setup Instructions

### Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

### Frontend
cd frontend
npm install
npm run dev

---

## Environment Variables

Create a `.env` file in the backend directory:

GROQ_API_KEY=
DATABASE_URL=
JWT_SECRET=

---

## Future Improvements

- Streaming AI responses
- Scheduled reporting system
- Multi-database support
- Advanced role-based permissions
- Query optimization suggestions

---

## Author

Cathrine Grace S
B.Tech (Artificial Intelligence and Machine Learning)
