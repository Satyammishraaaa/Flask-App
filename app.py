from dotenv import load_dotenv
import os
import openai
from flask import Flask, request, jsonify, render_template

# Load environment variables at the start of the app
load_dotenv()

# Check if the OpenAI API key is available
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found in environment variables.")

app = Flask(__name__)

## FORM to ask question and get the answer
@app.route('/', methods=['GET', 'POST'])
def form():
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
            except openai.error.AuthenticationError:
                answer = "Authentication Error: Invalid API key."
            except Exception as e:
                answer = f"Error occurred: {str(e)}"
    
    return render_template("form.html", answer=answer)  # Render the form with the answer (if any)


if __name__ == '__main__':
    # Use dynamic port from environment variables for deployment
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if not set
    app.run(host='0.0.0.0', port=port)
