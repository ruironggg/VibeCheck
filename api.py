import json
import time
from flask import Flask, request
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__, static_folder='../build', static_url_path='/')


# Health Check
@app.route('/time')
def get_current_time():
    return {'time': time.time()}


# Format of how to send in data using JSON, and then send it back in JSON
@app.route('/train-model', methods=['POST'])
def train_model():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json_input = request.get_json(force=True)
        print(json_input['graph'])
        graph = json_input['graph']
        return json.dumps({'agent': "agent"})
    else:
        return json.dumps({'error_message': 'Content-Type not supported!'})


# Add your APIs below
#
# @app.route('/test')
# def test():
#     # Initialize the sentiment analyzer
#     analyzer = SentimentIntensityAnalyzer()
#
#     # The text to be analyzed
#     text = "I am feeling great today! Everything is going well and I am very confident in my abilities."
#
#     # Get the sentiment scores
#     scores = analyzer.polarity_scores(text)
#     print(scores)
#
#     # Get the positive sentiment score
#     positive_sentiment = scores['pos']
#
#     # Get the compound sentiment score
#     confidence = scores['compound']
#
#     # Get the positive sentiment score
#     happy_sentiment = scores['pos']
#
#     print(f"The positive sentiment of the text is: {positive_sentiment}")
#     print(f"The confidence of the person is: {confidence}")
#     print(f"The happy sentiment of the text is: {happy_sentiment}")
#
#     nervous_bool = scores['neg'] > scores['pos']
#
#     # Check if the person is feeling unsure
#     unsure_bool = confidence < 0.1
#
#     # Check if the person is feeling happy
#     unhappy_bool = scores['pos'] > scores['neg']
#
#     # Check if the person is feeling proud
#     proud_bool = scores['pos'] > 0.6
#
#     return json.dumps({'agent': "agent"})