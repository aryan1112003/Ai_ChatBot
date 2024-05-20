from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Initialize the Hugging Face model
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def get_response_from_model(user_message):
    # Tokenize the input
    inputs = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors="pt")
    # Generate a response
    outputs = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Get the last sentence (response) by the bot
    bot_response = response.split(user_message)[-1].strip()
    return bot_response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    print("User message received:", user_message)
    
    # Generate response from the model
    bot_response = get_response_from_model(user_message)
    print("Bot response generated:", bot_response)
    
    # Save the conversation to the database
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (user_message, bot_response) VALUES (?, ?)', (user_message, bot_response))
    conn.commit()
    conn.close()
    
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
