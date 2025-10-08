# LLM Code Deployment Project

This project provides an API endpoint that accepts code generation requests, uses LLM to generate code, and deploys it to GitHub Pages. It handles both initial requests and revision requests.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```

## Running the Server

```bash
uvicorn main:app --reload
```

The server will start at http://localhost:8000

## API Endpoints

### POST /api/submit

Accepts JSON requests for code generation and deployment. See the API documentation for request/response formats.

## Project Structure

```
project-1/
├── app/
│   ├── api/
│   │   └── endpoints.py
│   └── core/
│       └── config.py
├── main.py
├── requirements.txt
└── .env
```