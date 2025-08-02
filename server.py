"""
server.py

This Flask application receives text input from users via a GET request,
analyzes the emotional content using the emotion_detector module, and
returns the emotion scores and the dominant emotion in the input text.
Includes error handling for blank or invalid input.
"""

from flask import Flask, request, render_template, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def get_emotion():
    """
    Handle emotion analysis via GET request.
    Returns a formatted string of emotion scores or an error message.
    """
    text_to_analyze = request.args.get("textToAnalyze")

    if not text_to_analyze:
        return "Invalid text! Please try again!"

    try:
        result = emotion_detector(text_to_analyze)

        if result.get('dominant_emotion') is None:
            return "Invalid text! Please try again!"

        formatted_response = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )
        return formatted_response

    except (KeyError, TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400


if __name__ == '__main__':
    app.run(debug=True)
