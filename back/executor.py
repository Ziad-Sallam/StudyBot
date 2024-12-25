import spacy
import re
import datetime
from fuzzywuzzy import fuzz

class QueryProcessor:
    def __init__(self, query: str):
        self.nlp = spacy.load("en_core_web_md")
        self.subjects = ["discrete mathematics", "computer organization", "programming ii", "communication skills", 
                         "numerical analysis", "human computer interaction"]
        self.subject_keywords = {subject: subject.split() for subject in self.subjects}  # Break subject into keywords

    def extract_parameters(self, query, intent):
        doc = self.nlp(query)
        if intent == "create assignment":
            subject = self.extract_subject(query)
            deadline = self.extract_deadline(query)
            return subject, deadline
        elif intent == "create task":
            description = self.extract_description_with_spacy(query)
            return description
        elif intent == "get material":
            subject = self.extract_subject(query)
            return subject

    def extract_subject(self, query):
        """Extract subject from the query using fuzzy matching and keyword matching."""
        query_doc = self.nlp(query.lower())  # Convert query to lowercase for matching
        best_match = None
        highest_score = 0

        # Iterate through all predefined subjects and check if any part matches
        for subject in self.subjects:
            subject_keywords = self.subject_keywords[subject]
            
            # Check if any subject keyword exists in the query using fuzzy matching for better flexibility
            for keyword in subject_keywords:
                score = fuzz.partial_ratio(keyword.lower(), query.lower())  # Use fuzzy matching
                if score > highest_score:
                    highest_score = score
                    best_match = subject
            
        if highest_score > 60:  # Only return subject if score is above a threshold (adjustable)
            return best_match
        return None  # If no matching subject found

    def extract_deadline(self, query):
        """Extract deadline from the query using regex."""
        deadline = None
        deadline_match = re.search(r"\b(\d{1,2}([./-])\d{1,2}\2\d{2,4})\b", query)
        if deadline_match:
            deadline_str = deadline_match.group(0)
            try:
                # Adjusted date format to handle both "-" and "/" separators
                deadline = datetime.datetime.strptime(deadline_str, "%d-%m-%Y").date()
                return deadline
            except ValueError:
                try:
                    # Try other formats
                    deadline = datetime.datetime.strptime(deadline_str, "%d/%m/%Y").date()
                    return deadline
                except ValueError:
                    return "Invalid Date"
        return "No Deadline Found"

    def extract_description_with_spacy(self, query):
        """Extract all words after the word 'task' using spaCy."""
        doc = self.nlp(query)  # Process the query with spaCy
        
        words_after_task = []
        found_task = False

        # Iterate through the tokens in the document
        for token in doc:
            if found_task:
                words_after_task.append(token.text)  # Collect words after 'task'
            if token.text.lower() == 'task':
                found_task = True  # Set flag when 'task' is found
        
        # Join and return the words after 'task'
        if words_after_task:
            return " ".join(words_after_task)
        return None  # If 'task' is not found in the query


if __name__ == "__main__":
    # Example queries
    query1 = "Create an assignment for discrete"
    query2 = "make task to complete the project report by tomorrow"
    query3 = "Create task to finish all the documents"
    query4 = "Get materials for programming ii"
    
    processor = QueryProcessor(query1)
    subject, deadline = processor.extract_parameters(query1, "create assignment")
    print(f"Subject: {subject}, Deadline: {deadline}")
    
    processor = QueryProcessor(query2)
    description = processor.extract_parameters(query2, "create task")
    print(f"Task Description: {description}")
    
    processor = QueryProcessor(query3)
    description = processor.extract_parameters(query3, "create task")
    print(f"Task Description: {description}")

    processor = QueryProcessor(query4)
    subject = processor.extract_parameters(query4, "get material")
    print(f"Subject: {subject}")
