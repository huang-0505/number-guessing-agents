from fastapi import FastAPI
from pydantic import BaseModel
import random
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

class GuessRequest(BaseModel):
    guess: int

SECRET_NUMBER = random.randint(1, 100)

def generate_funny_comment(feedback, guess):
    prompt = (
        f"You are a Hider agent in a number guessing game.\n"
        f"The player guessed {guess}, and the correct feedback is '{feedback}'.\n"
        f"Respond with a short funny comment encouraging the player, without revealing the secret number."
    )
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()

@app.get("/")
def root():
    return {"message": "Hider API with secret number logic is running."}

@app.post("/guess")
def guess_number(request: GuessRequest):
    guess = request.guess
    if guess < SECRET_NUMBER:
        feedback = "Higher"
    elif guess > SECRET_NUMBER:
        feedback = "Lower"
    else:
        feedback = "Correct"

    funny_comment = generate_funny_comment(feedback, guess)

    return {
        "feedback": feedback,
        "comment": funny_comment
    }
