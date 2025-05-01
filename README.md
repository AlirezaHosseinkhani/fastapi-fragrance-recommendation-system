# Shuts By L'dora - Fragrance Personalization System

A luxury fragrance recommendation system that creates personalized scent blends based on a user's character and
preferences.

## Features

- Personalized quiz to understand user's fragrance preferences
- AI-powered matching to L'dora Private Blend Collection
- Custom blend recommendations using the multi-shot concept
- Beautiful storytelling descriptions of the personalized blend
- Enhanced by Groq AI for deep emotional storytelling

## API Endpoints

- `GET /`: Welcome message
- `POST /api/welcome`: Get initial welcome message
- `GET /api/quiz`: Get quiz questions
- `POST /api/recommend`: Submit quiz answers and get personalized recommendation

## Development

### Prerequisites

- Python 3.10+
- FastAPI
- Groq API key

### Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your Groq API key: `GROQ_API_KEY=your_key_here` and LLM Model:
   `LLM_MODEL_NAME="Your LLM name"`
6. Run the server: `uvicorn app.main:app --reload`

### API Documentation

When running locally, visit:

- http://localhost:8000/docs for Swagger documentation
- http://localhost:8000/redoc for ReDoc documentation

## Deployment

This app can be deployed to any platform that supports Python applications:

- Heroku
- AWS Lambda
- Google Cloud Run
- etc.

Don't forget to set the GROQ_API_KEY environment variable in your deployment environment.