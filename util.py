import db
import constants
import re
import matplotlib.pyplot as plt
from transformers import pipeline
from wordcloud import WordCloud, STOPWORDS
import openai
import pandas as pd
import matplotlib
matplotlib.use('Agg')

# Set the API key
openai.api_key = constants.OPENAI_API_KEY


def private_message(client, channel_id, message, attachments=None):
    '''
    Sends a private / direct message
    '''
    if attachments:
        # text is still required as it is used as a fallback
        client.chat_postMessage(
            channel=channel_id,
            username="VibeCheckBot",
            attachments=attachments,
            text=message
        )
    else:
        client.chat_postMessage(
            channel=channel_id,
            username="VibeCheckBot",
            text=message
        )


def ephemeral_message(client, channel_id, user_id, message, attachments=None):
    '''
    Sends a message to current user only
    '''
    if attachments:
        # text is still required as it is used as a fallback
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            attachments=attachments,
            text=message
        )
    else:
        client.chat_postEphemeral(
            channel=channel_id,
            user=user_id,
            text=message
        )


def analyse_message(text, team_id):
    # get the team document
    team_doc = db.get_doc(team_id, db.all_teams_col)
    if team_doc:
        all_labels = team_doc[constants.POSITIVE_LABELS] + \
            team_doc[constants.NEGATIVE_LABELS]
    else:
        all_labels = constants.DEFAULT_POSITIVE_LABELS + constants.DEFAULT_NEGATIVE_LABELS
    classifier = pipeline("zero-shot-classification")
    res = classifier(text,
                     candidate_labels=all_labels)
    labels = res["labels"]
    scores = res["scores"]
    return labels, scores


def get_suggested_prompt(sentiment, message, team_id):
    # Define the prompt
    team_doc = db.get_doc(team_id, db.all_teams_col)
    if team_doc:
        negative_labels = team_doc[constants.NEGATIVE_LABELS]
    else:
        negative_labels = constants.DEFAULT_NEGATIVE_LABELS

    # we apply lower() again here just in case
    if sentiment.lower() in negative_labels:
        # Make the API request
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"I'm supervising an intern at my company. He sent me this message:'{message}' and he is feeling {sentiment}, how should I reply him? Please reply in the following format in less than 250 characters: 'Answer: '",
            max_tokens=50,
        )

        # replace 'Answer: ' with ''
        # return the generated text
        return re.sub(r"Answer:", "", response["choices"][0]["text"]).strip()
    else:
        return None


def get_insights(data):
    '''
    1. Generates a wordcloud and saves it to wordcloud.png
    2. Returns the top sentiment out of all messages
    '''
    comment_words = ''
    stopwords = set(STOPWORDS)

    # iterate through the csv file
    sentiment_frequency = dict()
    for doc in data:
        top_sentiment = doc[constants.SENTIMENT_LABELS][0]
        sentiment_frequency[top_sentiment] = sentiment_frequency.get(
            top_sentiment, 0) + 1
        for val in doc[constants.MESSAGE].split(" "):

            # typecaste each val to string
            val = str(val)

            # split the value
            tokens = val.split()

            # Converts each token into lowercase
            for i in range(len(tokens)):
                tokens[i] = tokens[i].lower()

            comment_words += " ".join(tokens)+" "

    if len(comment_words):
        wordcloud = WordCloud(width=1000, height=1000, background_color='white',
                              stopwords=stopwords, min_font_size=10).generate(comment_words)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)

        plt.savefig("wordcloud.png")

    top_sentiment = sorted(sentiment_frequency.items(),
                           key=lambda x: x[1], reverse=True)[0][0]

    return top_sentiment
