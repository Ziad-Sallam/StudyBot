import spacy
from spacy.training.example import Example

# Load a blank English model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner", last=True)  # Add NER component

# Add custom labels
ner.add_label("REQUEST")
ner.add_label("REQUEST_TYPE")
ner.add_label("MATERIAL")
ner.add_label("ASSIGNMENT")
ner.add_label("TASK")
ner.add_label("GET")
ner.add_label("CREATE")

# Training data (manually labeled)
TRAINING_DATA = [
    ("get material", {"entities": [(0, 3, "GET"), (4, 11, "MATERIAL")]}),
    ("create assignment", {"entities": [(0, 6, "CREATE"), (7, 17, "ASSIGNMENT")]}),
    ("get assignment", {"entities": [(0, 3, "GET"), (4, 8, "ASSIGNMENT")]}),
    ("create task", {"entities": [(0, 6, "CREATE"), (7, 11, "TASK")]}),
    ("get task", {"entities": [(0, 3, "GET"), (4, 8, "TASK")]}),
]

# Train the model
optimizer = nlp.begin_training()
for epoch in range(10):  # Iterating 10 times for training
    for text, annotations in TRAINING_DATA:
        # Convert data to spaCy's format
        example = Example.from_dict(nlp.make_doc(text), annotations)
        # Update the model
        nlp.update([example], losses={})

# Function to handle the user input and trigger actions
def handle_query(user_input):
    # Convert user input to lowercase to make it case-insensitive
    user_input = user_input.lower()

    # First, check if the input exactly matches any of the training data
    if user_input in [t[0].lower() for t in TRAINING_DATA]:  # Compare in lowercase
        doc = nlp(user_input)

        
        # Output the recognized entities
        print("\nRecognized Entities:")
        for ent in doc.ents:
            print(f"{ent.text} ({ent.label_})")
        
        # Execute corresponding behavior based on the full match
        if user_input == "get task":
            print("Executing: Retrieving task...")
        elif user_input == "create task":
            print("Executing: Creating a new task...")
        elif user_input == "get material":
            print("Executing: Retrieving material...")
        elif user_input == "create assignment":
            print("Executing: Creating a new assignment...")
        elif user_input == "get assignment":
            print("Executing: Retrieving assignment...")
        return

    # If not a full match, tokenize without labeling
    doc = nlp.make_doc(user_input)  # Make doc without using the NER pipeline
    
    # Check if any token is recognizable
    recognized_tokens = []
    for token in doc:
        if token.text in ["task", "material", "assignment", "get", "create"]:
            recognized_tokens.append(token.text)
    
    # If we found recognized tokens, suggest related actions
    if recognized_tokens:
        print("\nDid you mean any of the following?")
        if "get" in recognized_tokens:
            print("Press 't' for 'get task'")
            print("Press 'a' for 'get assignment'")
            print("Press 'm' for 'get material'")
        if "create" in recognized_tokens:
            print("Press 't' for 'create task'")
            print("Press 'a' for 'create assignment'")
        if "task" in recognized_tokens:
            print("Press 'g' for 'get task'")
            print("Press 'c' for 'create task'")
        if "material" in recognized_tokens:
            print("Press 'g' for 'get material'")
        if "assignment" in recognized_tokens:
            print("Press 'g' for 'get assignment'")
            print("Press 'c' for 'create assignment'")
        
        # Ask the user to confirm their choice
        user_choice = input("Enter your choice : ").strip().lower()
        
        # Execute based on the user's choice
        if user_choice == 'g' and "task" in recognized_tokens:
            print("\nExecuting: Retrieving task...")
        elif user_choice == 'c' and "task" in recognized_tokens:
            print("\nExecuting: Creating a new task...")
            
        elif user_choice == 'g' and "material" in recognized_tokens:
            print("\nExecuting: Retrieving material...")
            
        elif user_choice == 'g' and "assignment" in recognized_tokens:
            print("\nExecuting: Retrieving assignment...")
        elif user_choice == 'c' and "assignment" in recognized_tokens:
            print("\nExecuting: Creating a new assignment...")
            
        elif user_choice == 't' and "get" in recognized_tokens:
            print("\nExecuting: Retrieving task...")
        elif user_choice == 'a' and "get" in recognized_tokens:
            print("\nExecuting: Retrieving assignment...")
        elif user_choice == 'm' and "get" in recognized_tokens:
            print("\nExecuting: Retrieving material...")
            
        elif user_choice == 't' and "create" in recognized_tokens:
            print("\nExecuting: Creating a new task...")
        elif user_choice == 'a' and "create" in recognized_tokens:
            print("\nExecuting: Creating a new assignment...")
        
        else:
            print("\nUnknown choice or invalid input.")
    else:
        # If no recognized tokens, print invalid input
        print("\nInvalid input. Could not recognize any valid entities.")

# Test the system with user input
user_input = input("Enter your query: ")
handle_query(user_input)
