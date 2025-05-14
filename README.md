# 🎯 Number Guessing Agents with Ollama 
# (Doing it because this is an interview question I failed miserably lol)

This project creates two AI agents that play a number guessing game, powered by a local LLM (Mistral) through Ollama.

- **Hider Agent**: FastAPI server that holds a secret number between 1 and 100 and provides honest feedback ("Higher", "Lower", "Correct"). (Actually need to use python logic to see compare numbers instead of LLM)
- **Guesser Agent**: Python script that uses the LLM to intelligently guess the hidden number through HTTP requests.

## 🛠 Technologies Used
- FastAPI
- Python 3
- Ollama (Mistral model)
- REST APIs (HTTP)


## 
