import spacy

# Load the spacy model: nlp
class QueryHandler:
    nlp = spacy.load("en_core_web_md")

    def __init__(self):
        self.reference_phrases = {
            "get assignment": self.nlp("get assignment"),
            "get task": self.nlp("get task"),
            "get material": self.nlp("get material"),
            "create task": self.nlp("create task"),
            "create assignment": self.nlp("create assignment"),
        }
        # Assign weights to specific words to adjust their impact on similarity
        self.weights = {
            "assignment": 1.2,  # Boost for "assignment"
            "task": 1.2,        # Boost for "task"
        }
        # Hardcoded synonymous verbs for "get" and "create"
        self.get_synonyms = ["get", "retrieve", "fetch", "obtain", "acquire", "see", "view"]        
        self.create_synonyms = ["create", "build", "make", "produce", "construct", "generate", "add", "set"]

    def is_synonym(self, token, verb_group):
        """Check if a token is a synonym of a specific verb group using hardcoded values."""
        if verb_group == "get":
            return token.lemma_ in self.get_synonyms
        elif verb_group == "create":
            return token.lemma_ in self.create_synonyms
        return False

    def adjust_similarity(self, query, doc, contains_get, contains_create):
        """Adjust similarity using predefined weights for specific words."""
        base_similarity = query.similarity(doc)
        weighted_similarity = base_similarity

        for word in query:
            if word.lemma_ in self.weights:
                weight = self.weights[word.lemma_]
                for ref_word in doc:
                    if word.lemma_ == ref_word.lemma_:
                        weighted_similarity += (weight - 1) * ref_word.similarity(word)

        # Boost for synonyms of "get"
        if contains_get:
            weighted_similarity += 0.4  # Increase the boost for "get"
        # Boost for synonyms of "create"
        if contains_create:
            weighted_similarity += 0.4  # Increase the boost for "create"

        return weighted_similarity

    def apply_penalty(self, similarity, contains_get, contains_create, phrase, query):
        """Apply penalties for mismatches and conflicting keywords."""
        # Penalty for mismatched 'get' vs 'create'
        if contains_get and "create" in phrase:
            similarity -= 0.4  # Penalty for mismatched 'get' vs 'create'
        elif contains_create and "get" in phrase:
            similarity -= 0.4  # Penalty for mismatched 'create' vs 'get'

        # Penalty if query contains 'task(s)' but reference phrase contains 'assignment(s)'
        query_lemmas = [token.lemma_ for token in query]
        if "task" in query_lemmas and "assignment" in phrase:
            # print(f"Task(s) in query, assignment(s) in phrase: {similarity:.4f}")
            similarity -= 0.4
        elif "assignment" in query_lemmas and "task" in phrase:
            # print(f"Assignment(s) in query, task(s) in phrase: {similarity:.4f}")
            similarity -= 0.4

        return similarity

    def identify_query(self, query, threshold=0.5):
        query_doc = self.nlp(query.lower())
        most_similar = "none"
        max_similarity = 0

        # Determine if the query contains hardcoded synonyms for "get" or "create"
        contains_get = any(self.is_synonym(token, "get") for token in query_doc)
        contains_create = any(self.is_synonym(token, "create") for token in query_doc)

        # Check if the query contains "material"
        contains_material = any(token.lemma_ == "material" for token in query_doc)

        # Special condition: "create" and "material"
        if contains_create and contains_material:
            return "This command can't be used here"

        # print(contains_get, contains_create, contains_material)
        # print("Debugging Similarity Scores with Weights, Keyword, and Verb Synonym Priority:")
        for phrases, doc in self.reference_phrases.items():
            if phrases == "get material" and not contains_material:
                # Set similarity to 0 if the query does not contain "material"
                # print(f"Setting similarity of 'get material' to 0 for the query '{query_doc.text}'.")
                similarity = 0
            else:
                similarity = self.adjust_similarity(query_doc, doc, contains_get, contains_create)
                similarity = self.apply_penalty(similarity, contains_get, contains_create, phrases, query_doc)

                # print(f"Base similarity of '{query_doc.text}' with '{phrases}' is {similarity:.4f}")

                # Boost similarity for hardcoded synonyms of "get" or "create"
                if contains_get and "get" in phrases:
                    similarity += 0.3
                elif contains_create and "create" in phrases:
                    similarity += 0.3

                # print(f"Adjusted similarity of '{query_doc.text}' with '{phrases}' is {similarity:.4f}")

            if similarity > max_similarity:
                most_similar = phrases
                max_similarity = similarity

        # Threshold check
        return most_similar if max_similarity > threshold else "I am sorry I didnt get that. Can you please rephrase?"




if __name__ == "__main__":
    # Get user input
    input_text = input("Enter your query: ")

    # Create a QueryHandler instance and identify the most similar phrase
    query_handler = QueryHandler()
    result = query_handler.identify_query(input_text)

    print(f"The input '{input_text}' is most similar to: {result}")
