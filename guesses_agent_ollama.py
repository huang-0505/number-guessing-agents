import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"
HIDER_API_URL = "http://127.0.0.1:8000/guess"

low = 1
high = 100
feedback = None
guess = None
attempts = 0

def ask_guesser_llm(low, high, last_guess, last_feedback):
    if last_guess is None:
        prompt = (
            f"You are a Guesser agent.\n"
            f"Guess a number between {low} and {high}.\n"
            f"Only output the number."
        )
    else:
        prompt = (
            f"You are a Guesser agent.\n"
            f"Your allowed guessing range is between {low} and {high}.\n"
            f"Previous guess was {last_guess}, and feedback was '{last_feedback}'.\n"
            f"Now guess a number strictly between {low} and {high}, inclusive.\n"
            f"Do not guess a number outside this range.\n"
            f"Only output the number."
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

while True:
    guess_text = ask_guesser_llm(low, high, guess, feedback)

    try:
        guess = int(guess_text)
    except ValueError:
        print(f"Invalid guess from LLM: {guess_text}. Retrying...")
        continue

    attempts += 1
    print(f"Guesser: I guess {guess}")

    res = requests.post(HIDER_API_URL, json={"guess": guess})
    feedback = res.json()["feedback"]

    print(f"Hider says: {feedback}")

    if feedback.lower() == "correct":
        print(f"\n🎯 Guesser found the correct number {guess} in {attempts} attempts!")
        break

    if feedback.lower() == "higher":
        low = guess + 1
    elif feedback.lower() == "lower":
        high = guess - 1

    time.sleep(0.5) 
