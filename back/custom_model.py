import spacy
from spacy.training.example import Example

class QueryHandler:
    def __init__(self):
        # Initialize the spaCy model and add NER component
        self.nlp = spacy.blank("en")
        self.ner = self.nlp.add_pipe("ner", last=True)
        
        # Add custom labels
        self.ner.add_label("REQUEST")
        self.ner.add_label("REQUEST_TYPE")
        self.ner.add_label("MATERIAL")
        self.ner.add_label("ASSIGNMENT")
        self.ner.add_label("TASK")
        self.ner.add_label("GET")
        self.ner.add_label("CREATE")
        
        # Training data (manually labeled)
        self.TRAINING_DATA = [
            ("get material", {"entities": [(0, 3, "GET"), (4, 11, "MATERIAL")]}),
            ("create assignment", {"entities": [(0, 6, "CREATE"), (7, 17, "ASSIGNMENT")]}),
            ("get assignment", {"entities": [(0, 3, "GET"), (4, 8, "ASSIGNMENT")]}),
            ("create task", {"entities": [(0, 6, "CREATE"), (7, 11, "TASK")]}),
            ("get task", {"entities": [(0, 3, "GET"), (4, 8, "TASK")]}),
        ]

        # Train the model
        self.optimizer = self.nlp.begin_training()
        for epoch in range(10):  # Iterating 10 times for training
            for text, annotations in self.TRAINING_DATA:
                # Convert data to spaCy's format
                example = Example.from_dict(self.nlp.make_doc(text), annotations)
                # Update the model
                self.nlp.update([example], losses={})

    def handle_query(self, user_input):
        responses = []  # List to store responses

        # Convert user input to lowercase to make it case-insensitive
        user_input = user_input.lower()

        # First, check if the input exactly matches any of the training data
        if user_input in [t[0].lower() for t in self.TRAINING_DATA]:  # Compare in lowercase
            doc = self.nlp(user_input)

            # Add the recognized entities to the response list
            responses.append("\nRecognized Entities:")
            for ent in doc.ents:
                responses.append(f"{ent.text} ({ent.label_})")
            
            # Execute corresponding behavior based on the full match
            if user_input == "get task":
                responses.append("Executing: Retrieving task...")
            elif user_input == "create task":
                responses.append("Executing: Creating a new task...")
            elif user_input == "get material":
                responses.append("Executing: Retrieving material...")
            elif user_input == "create assignment":
                responses.append("Executing: Creating a new assignment...")
            elif user_input == "get assignment":
                responses.append("Executing: Retrieving assignment...")
            return responses

        # If not a full match, tokenize without labeling
        doc = self.nlp.make_doc(user_input)  # Make doc without using the NER pipeline
        
        # Check if any token is recognizable
        recognized_tokens = []
        for token in doc:
            if token.text in ["task", "material", "assignment", "get", "create"]:
                recognized_tokens.append(token.text)
        
        # If we found recognized tokens, suggest related actions
        if recognized_tokens:
            responses.append("\nDid you mean any of the following?")
            if "get" in recognized_tokens:
                responses.append("Press 't' for 'get task'")
                responses.append("Press 'a' for 'get assignment'")
                responses.append("Press 'm' for 'get material'")
            if "create" in recognized_tokens:
                responses.append("Press 't' for 'create task'")
                responses.append("Press 'a' for 'create assignment'")
            if "task" in recognized_tokens:
                responses.append("Press 'g' for 'get task'")
                responses.append("Press 'c' for 'create task'")
            if "material" in recognized_tokens:
                responses.append("Press 'g' for 'get material'")
            if "assignment" in recognized_tokens:
                responses.append("Press 'g' for 'get assignment'")
                responses.append("Press 'c' for 'create assignment'")
            
            # Ask the user to confirm their choice
            # Here, you can add logic to collect user choice, but for now, let's assume a choice is made directly
            user_choice = input("Enter your choice : ").strip().lower()
            
            # Execute based on the user's choice
            if user_choice == 'g' and "task" in recognized_tokens:
                responses.append("\nExecuting: Retrieving task...")
            elif user_choice == 'c' and "task" in recognized_tokens:
                responses.append("\nExecuting: Creating a new task...")
                
            elif user_choice == 'g' and "material" in recognized_tokens:
                responses.append("\nExecuting: Retrieving material...")
                
            elif user_choice == 'g' and "assignment" in recognized_tokens:
                responses.append("\nExecuting: Retrieving assignment...")
            elif user_choice == 'c' and "assignment" in recognized_tokens:
                responses.append("\nExecuting: Creating a new assignment...")
                
            elif user_choice == 't' and "get" in recognized_tokens:
                responses.append("\nExecuting: Retrieving task...")
            elif user_choice == 'a' and "get" in recognized_tokens:
                responses.append("\nExecuting: Retrieving assignment...")
            elif user_choice == 'm' and "get" in recognized_tokens:
                responses.append("\nExecuting: Retrieving material...")
                
            elif user_choice == 't' and "create" in recognized_tokens:
                responses.append("\nExecuting: Creating a new task...")
            elif user_choice == 'a' and "create" in recognized_tokens:
                responses.append("\nExecuting: Creating a new assignment...")
            
            else:
                responses.append("\nUnknown choice or invalid input.")
        else:
            # If no recognized tokens, print invalid input
            responses.append("\nInvalid input. Could not recognize any valid entities.")

        return responses

# Usage
query_handler = QueryHandler()

# To test the system with user input
user_input = input("Enter your query: ")
responses = query_handler.handle_query(user_input)
for response in responses:
    print(response)
