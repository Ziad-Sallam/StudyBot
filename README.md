# StudyBot

StudyBot is a web application designed to help students manage assignments, chat with a bot powered by Gemini API, and access course materials. The project combines a Django backend with a React + Vite frontend for a modern, scalable solution.

## Project Structure

```
back/      # Django backend
front/     # React + Vite frontend
```

## Backend Setup

1. **Navigate to the `back` directory:**
    ```sh
    cd back
    ```

2. **Create and activate a Python virtual environment (recommended):**
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Start the backend server:**
    ```sh
    python manage.py runserver
    ```

## Frontend Setup

1. **Navigate to the `front` directory:**
    ```sh
    cd front
    ```

2. **Install dependencies:**
    ```sh
    npm install
    ```

3. **Start the frontend development server:**
    ```sh
    npm run dev
    ```

## Gemini API Integration

StudyBot uses the Gemini API to power its chatbot feature, enabling intelligent responses and assistance for students.

### How Gemini API is Used

- The backend communicates with the Gemini API to process natural language queries from users.
- When a student sends a message in the chat, the frontend sends the message to the backend, which then forwards it to the Gemini API.
- The Gemini API returns a response, which is sent back to the frontend and displayed to the user.

### Configuration

1. **Obtain a Gemini API key** from Google AI Studio or your organization.
2. **Set the API key as an environment variable** in your backend:
    ```sh
    set GEMINI_API_KEY=your_api_key_here
    ```
3. **Configure the Gemini API endpoint** in your Django settings or a dedicated configuration file.

### Example Usage

```python
import os
import requests

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

def get_gemini_response(user_message):
    headers = {'Authorization': f'Bearer {GEMINI_API_KEY}'}
    payload = {
        "contents": [{"parts": [{"text": user_message}]}]
    }
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
    return response.json()
```

## Usage

- Access the frontend at [http://localhost:5173](http://localhost:5173)
- The backend runs at [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Use the chatbot to interact with Gemini AI for study help and information.

## Features

- Assignment management
- Course material upload and download
- Chatbot for student assistance (powered by Gemini API)
- Notifications
- Secure authentication with JWT

## Technologies

- **Backend:** Django, Django REST Framework, Celery, Gemini API
- **Frontend:** React, Vite

## License

MIT License

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Contact

For questions or support, please contact me.