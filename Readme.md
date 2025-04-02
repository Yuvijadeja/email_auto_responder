# AI Email Responder

This Python script automates email responses using OpenAI's GPT model and Gmail API. It fetches unread emails, generates AI-driven replies, and sends responses automatically.

## Features
- Authenticate with Gmail API.
- Fetch unread emails from the inbox.
- Generate AI-based responses using OpenAI's GPT model.
- Send replies to the original sender.
- Mark emails as read after responding.

## Prerequisites
- Python 3.x installed
- A Google Cloud project with Gmail API enabled
- OpenAI API key
- Required Python packages installed

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/ai-email-responder.git
   cd ai-email-responder
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up Google API credentials:
   - Enable Gmail API in Google Cloud Console.
   - Download `credentials.json` and place it in the project folder.

4. Set up OpenAI API key:
   - Create a `.env` file and add your OpenAI API key:
     ```sh
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage
Run the script with:
```sh
python main.py
```

## How It Works
1. Authenticates with Gmail using OAuth 2.0.
2. Fetches unread emails.
3. Uses GPT model to generate responses.
4. Sends replies and marks emails as read.

## Configuration
- Modify `SCOPES` to change Gmail permissions.
- Adjust `generate_response()` to customize AI behavior.

## Security Notes
- Keep `credentials.json` and `token.json` secure.
- Avoid exposing API keys in public repositories.

## License
MIT License
