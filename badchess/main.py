import os
import requests
import logging

def get_best_move_from_chatgpt(legal_moves: list[str]) -> str:
    # Retrieve the API key from environment variables or a config file
    api_key = os.getenv('API_KEY')
    if not api_key:
        try:
            with open('.config/api_key', 'r') as file:
                api_key = file.read().strip()
        except FileNotFoundError:
            logging.error('API key not found in environment variables or .config/api_key file.')
            return ""

    # Define the API endpoint and headers
    api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Prepare the payload with the list of legal moves
    payload = {
        "prompt": f"Given the following legal chess moves: {legal_moves}, determine the best move.",
        "max_tokens": 10
    }

    # Send the request to ChatGPT
    response = requests.post(api_url, headers=headers, json=payload)

    # Extract the best move from the response
    if response.status_code == 200:
        best_move = response.json().get("choices", [{}])[0].get("text", "").strip()
        return best_move
    else:
        logging.error(f"Failed to get response from ChatGPT: {response.status_code}")
        return ""