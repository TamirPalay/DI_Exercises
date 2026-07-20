from nltk.tokenize import word_tokenize

# Step 1: Define intents and responses
intents = {
    "greeting": ["hello", "hi", "hey"],
    "opening_hours": ["open", "opening", "hours"],
    "pricing": ["price", "cost", "how much"]
}

responses = {
    "greeting": "Hello! How can I help you today?",
    "opening_hours": "We are open from 9 AM to 6 PM, Monday to Friday.",
    "pricing": "Our pricing starts at $10 per month.",
    "default": "Sorry, I didn't understand that. Can you please rephrase?"
}

# Step 2: Build the chatbot
def rule_based_chatbot(user_input):
    tokens = word_tokenize(user_input.lower())

    for intent, keywords in intents.items():
        if any(keyword in tokens for keyword in keywords):
            return responses[intent]

    return responses["default"]

# Step 3: Test the chatbot
print(rule_based_chatbot("What are your opening hours?"))  # Output: We are open from 9 AM to 6 PM, Monday to Friday.
print(rule_based_chatbot("How much does it cost?"))       # Output: Our pricing starts at $10 per month.
print(rule_based_chatbot("Tell me a joke"))               # Output: Sorry, I didn't understand that. Can you please rephrase?
