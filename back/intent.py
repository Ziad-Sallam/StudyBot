from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/get-intent', methods=['POST'])
def get_intent():
    user_input = request.json.get("message", "")
    intent = identify_intent(user_input)  # Or use `identify_intent_spacy`
    return jsonify({"intent": intent})

if __name__ == "__main__":
    app.run(debug=True)
