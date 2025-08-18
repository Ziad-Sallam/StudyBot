from datetime import datetime
import os
import spacy
import google.generativeai as genai
from .models import Subject, AssignmentType

api_key = os.getenv('GEMINI_API_KEY')

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 4000,
    "response_mime_type": "text/plain",
}


class QueryHandler:
    def __init__(self):
        # configure API once
        genai.configure(api_key=api_key)

        # create the model
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=generation_config,
        )

        # ✅ correct chat history format (no "system")
        self.chat = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [{"text": "You are an assistant that classifies queries into actions."}],
                },
                {
                    "role": "user",
                    "parts": [{"text": "Your name is Trixie."}],
                },
            ]
        )

    def identify_query(self, query, threshold=0.4):
        # send the query into the ongoing chat
        response = self.chat.send_message(f"""
        The user message is: "{query}".
        Choose exactly one action from this list:
        - create assignment : like (sheet, project, lab).
        - create notification
        - create material
        - none
        Respond ONLY with the action name, nothing else.
        """)
        result = response.text.strip()
        if result == "none":
            response = self.chat.send_message(f"""
                        The user message is: "{query}".
                        respond normally.
                        """)
            result = response.text.strip()
            return result
       
        return result
    
    def get_task_description(self, query):
        # send the query into the ongoing chat
        response = self.chat.send_message(f"""
        The user message is: "{query}".
        Respond with a short title of the task.
        """)
        result = response.text.strip()
        print(f"Task description: {result}")
        return result
    
    def get_notification_description(self, query):
        # send the query into the ongoing chat
        title = self.chat.send_message(f"""
        The user message is: "{query}".
        Respond with a short title of the notification.
        """)
        title = title.text.strip()
        description = self.chat.send_message(f"""The user message is: "{query}".
        Respond with a short description of the notification.
        """)
        description = description.text.strip()
        result = f"{title} - {description}"
        print(f"Notification description: {result}")
        return title, description

    def get_assignment_description(self, query):
        subjects = Subject.objects.all()
        subject_names = [subject.name for subject in subjects]
        subject_names_str = ", ".join(subject_names)
        # send the query into the ongoing chat
        print(f"Subjects: {subject_names_str}")
        subject = self.chat.send_message(f"""The user message is: "{query}".
                                            Respond with the subject of the assignment from this list: {subject_names_str}.
                                            """)
        subject = subject.text.strip()
        print(f"Subject: {subject}")
        deadline = self.chat.send_message(f"""
        The user message is: "{query}".

        Your task:
        - Identify if the user mentioned a deadline (e.g., "tomorrow", "next week", "August 20 at 5pm").
        - Convert it into an absolute datetime in the format: YYYY-MM-DD HH:MM:SS
        - Use the current date/time as reference: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        - If no deadline is mentioned, respond ONLY with: no deadline
        - Output must contain ONLY the datetime or "no deadline" — no extra words.
        """)

        deadline = deadline.text.strip()

        description = self.chat.send_message(f"""The user message is: "{query}".
                                            Respond with a short description of the assignment.
                                            """)
        description = description.text.strip()
        assignment_type = self.chat.send_message(f"""The user message is: "{query}".
                                            Respond with the type of the assignment from this list: {', '.join([at.type for at in AssignmentType.objects.all()])}.
                                            """)
        assignment_type = assignment_type.text.strip()


        result = f"{subject} - {deadline} - {description} - {assignment_type}"
        print(f"Assignment description: {result}")
        return subject, deadline, description, assignment_type
    
    def coustom_query(self, query):
        # send the query into the ongoing chat
        response = self.chat.send_message(f"""
        The user message is: "{query}".
        Respond normally.
        """)
        result = response.text.strip()
        return result
                                          
       


if __name__ == "__main__":
    input_text = input("Enter your query: ")

    query_handler = QueryHandler()
    result = query_handler.identify_query(input_text)

    print(f"{result}")
