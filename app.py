from dotenv import load_dotenv
import os

def configure():
    load_dotenv()


import openai
from flask import Flask, request, jsonify, render_template

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Q&A Application!"

## FORM to ask question and get the answer
@app.route('/form', methods=['GET', 'POST'])
def form():
    configure()
    answer = None  # Variable to store the answer

    if request.method == 'POST':
        question = request.form.get('question')  # Get the question from the form
        if question:
            try:
                # Call OpenAI's ChatCompletion method (new API)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",  # You can use "gpt-4" as well
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": question}
                    ]
                )

                # Extract the answer from the response
                answer = response['choices'][0]['message']['content']
            except Exception as e:
                answer = f"Error occurred: {str(e)}"
    
    return render_template("form.html", answer=answer)  # Render the form with the answer (if any)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)