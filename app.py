from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def get_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        return None
    except openai.RateLimitError as e:
        print(f"OpenAI Rate Limit error: {e}")
        return None
    except openai.AuthenticationError as e:
        print(f"OpenAI Authentication error: {e}")
        return None
    except openai.APIConnectionError as e:
        print(f"OpenAI API Connection error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data.get('expression')

        if not expression:
            return jsonify({"error": "Missing 'expression' parameter"}), 400

        prompt = f"""
        You are a helpful calculator. Evaluate the following arithmetic expression and provide the result.
        Expression: {expression}
        Provide the result and the explanation in the format
        result : Explanation
        """

        result = get_completion(prompt)

        if result is None:
            return jsonify({"error": "Failed to get a response from OpenAI"}), 500

        try:
            numeric_result = float(result)
            return jsonify({"result": numeric_result}), 200
        except ValueError:
            return jsonify({"result": result, "message": "The result from the llm is not a valid number"}), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')  # Render the HTML page


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))