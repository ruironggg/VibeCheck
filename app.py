import logging
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import os
import os
import re
from flask import Flask, request
# from slack_bolt.adapter.flask import SlackRequestHandler
from waitress import serve
# from gevent.pywsgi import WSGIServer
from uuid import uuid4  # For security
import db
import util
import constants

app = App()
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# LABELS COMMAND


@app.command("/labels")
def update_labels(ack, client, command):
    '''
    Update a list of labels that one can use to classify messages
    '''
    # Acknowledge command request
    ack()
    try:
        channel_id = command.get("channel_id")
        util.private_message(client, channel_id,  message="Would you like to add or delete a label?", attachments=[
            {
                "text": '''Note: If a negative label is added, a prompt will be generated for the user if our model predicts that the user is feeling that emotion.''',
                "fallback": "Error: unable to generate menu buttons",
                "callback_id": "label_options",
                "color": "#3AA3E3",
                "attachment_type": "default",
                            "actions": [
                                {
                                    "name": f"delete_label",
                                    "text": "Delete",
                                    "type": "button",
                                    "value": "delete",
                                    "confirm": {
                                        "title": "Are you sure?",
                                        "text": "Warning: You are about to permanently delete a label. This action cannot be undone.",
                                        "ok_text": "Yes",
                                        "dismiss_text": "No"
                                    }
                                },
                                {
                                    "name": f"add_label",
                                    "text": "Add",
                                    "type": "button",
                                    "value": "add",

                                },
                            ]
            }
        ]
        )

    except Exception as e:
        # print(e)
        util.private_message(client, channel_id,
                             message=f"Error: {e}")
        return


@app.action("select1")
def handle_some_action(ack, body, logger):
    '''Just to prevent errors from getting thrown when a user selects an option'''
    ack()
    logger.info(body)


@app.action("label_options")
def handle_user_options(ack, respond, action, context, client, body):
    '''
    Handles the following user actions
    (A) Delete
    (B) Add positive
    (C) Add negative
    '''

    # required: used to acknowledge that the request was received from Slack
    try:
        ack()
        channel_id = context.get("channel_id")
        team_id = context.get("team_id")
        selected_value = action.get("value")

        # if the selected value is delete, we display to users a list of available options to delete
        if selected_value == "delete":
            # check if we can find the teams document in the database
            team_doc = db.get_doc(team_id, db.all_teams_col)
            # if we can, generate a list of options from the labels
            if team_doc:
                positive_labels = team_doc.get(constants.POSITIVE_LABELS)
                negative_labels = team_doc.get("negative_labels")
                all_labels = positive_labels + negative_labels
            else:
                all_labels = constants.DEFAULT_POSITIVE_LABELS + constants.DEFAULT_NEGATIVE_LABELS

            # generate a list of options from the labels
            options = []
            for label in all_labels:
                options.append({
                    "text": label.title(),
                    "value": label
                })

            # send a message to the user with a list of options to delete
            util.private_message(client, channel_id,  message="Which label would you like to delete?", attachments=[
                {
                    "text": '''List of users available to track''',
                    "fallback": "Error: unable to generate menu buttons",
                    "callback_id": "delete_label_options",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "actions": [
                            {
                                "name": "delete_label",
                                "text": "Select a label to delete...",
                                "type": "select",
                                "options": options
                            }
                    ]
                }
            ]
            )

        # otherwise, we prompt the user to add a new label
        elif selected_value == "add":
            # Call views_open with the built-in client
            client.views_open(
                # Pass a valid trigger_id within 3 seconds of receiving it
                trigger_id=body["trigger_id"],
                # View payload
                view={
                    "type": "modal",
                    # View identifier
                    "callback_id": "add_label_modal",
                    "title": {"type": "plain_text", "text": "My App"},
                    "submit": {"type": "plain_text", "text": "Submit"},
                    "blocks": [
                        {
                            "type": "input",
                            "block_id": "input1",
                            "label": {"type": "plain_text", "text": "What is the name of your new label?"},
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "label_input",
                            }
                        },
                        {
                            "type": "actions",
                            "block_id": "actions1",
                            "elements": [{
                                "action_id": "select1",
                                "type": "static_select",
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": "Select a label type..."
                                },
                                "options": [
                                    {
                                        "text": {
                                            "type": "plain_text",
                                            "text": "Positive"
                                        },
                                        "value": "positive"
                                    },
                                    {
                                        "text": {
                                            "type": "plain_text",
                                            "text": "Negative"
                                        },
                                        "value": "negative"
                                    },
                                ]
                            }]
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": "Note: *If a negative label is added*, a prompt will be generated for the user if our model predicts that the user is feeling that emotion"
                                }
                            ]
                        },
                    ]
                }
            )

    except Exception as e:
        print(f"Error: {e}")
        util.private_message(client, channel_id, f"{e}")


@app.view("add_label_modal")
def handle_submission(ack, view, client, body):
    try:
        ack()
        user_id = body["user"]["id"]
        values_selected = view["state"]["values"]
        label = values_selected["input1"]["label_input"]["value"].lower()
        label_type = values_selected["actions1"]["select1"]["selected_option"]["value"]
        team_id = view.get("team_id")
        team_doc = db.get_doc(team_id, db.all_teams_col)
        if team_doc:
            if label_type == "positive":
                team_doc[constants.POSITIVE_LABELS].append(label)
                # remove duplicates
                team_doc[constants.POSITIVE_LABELS] = list(
                    set(team_doc[constants.POSITIVE_LABELS]))
            else:
                team_doc[constants.NEGATIVE_LABELS].append(label)
                # remove duplicates
                team_doc[constants.NEGATIVE_LABELS] = list(
                    set(team_doc[constants.NEGATIVE_LABELS]))

            # update the team document
            db.write_to_col(id=team_id, col=db.all_teams_col,
                            data=team_doc, is_update=True)
        else:
            positive_labels = constants.DEFAULT_POSITIVE_LABELS
            negative_labels = constants.DEFAULT_NEGATIVE_LABELS
            if label_type == "positive":
                positive_labels.append(label)
            else:
                negative_labels.append(label)
            team_doc = {
                constants.ID: team_id,
                constants.POSITIVE_LABELS: positive_labels,
                constants.NEGATIVE_LABELS: negative_labels
            }
            # insert document into database
            db.write_to_col(col=db.all_teams_col, data=team_doc)

        util.private_message(
            client, user_id, f"You have successfully added the label *{label}* to the list of *{label_type}* labels.")

    except Exception as e:
        print(f"Error: {e}")
        util.private_message(client, user_id, f"{e}")


@app.action("delete_label_options")
def handle_label_options(ack, respond, action, context, client):
    '''
    Deletes a label from the team's list of labels
    '''
    # required: used to acknowledge that the request was received from Slack
    ack()
    try:
        team_id = context.get("team_id")
        channel_id = context.get("channel_id")
        team_doc = db.get_doc(team_id, db.all_teams_col)
        selected_label = action.get("selected_options")[0].get("value")
        if team_doc:
            positive_labels = team_doc[constants.POSITIVE_LABELS]
            negative_labels = team_doc[constants.NEGATIVE_LABELS]

        else:
            positive_labels = constants.DEFAULT_POSITIVE_LABELS
            negative_labels = constants.DEFAULT_NEGATIVE_LABELS

        if selected_label in positive_labels:
            positive_labels.remove(selected_label)
        else:
            negative_labels.remove(selected_label)

        if team_doc:
            # update the team document
            db.write_to_col(id=team_id, col=db.all_teams_col,
                            data=team_doc, is_update=True)
        else:
            team_doc = {
                constants.ID: team_id,
                constants.POSITIVE_LABELS: positive_labels,
                constants.NEGATIVE_LABELS: negative_labels
            }
            # insert document into database
            db.write_to_col(col=db.all_teams_col, data=team_doc)

        respond(
            f"You have successfully deleted *{selected_label}*")
        return

    except Exception as e:
        print(f"Error: {e}")
        util.private_message(client, channel_id, f"{e}")


# INTERNS COMMAND
@app.command("/interns")
def show_interns(ack, client, command):
    '''
    Shows a list of interns in the workspace that one can conduct sentiment analysis on
    '''
    # Acknowledge command request
    ack()
    try:
        # check if the current user is an admin
        user_info = client.users_info(user=command.get("user_id"))
        is_admin = user_info["user"]["is_admin"]
        is_owner = user_info["user"]["is_owner"]
        is_primary_owner = user_info["user"]["is_primary_owner"]
        # if the current user is not an admin, send an error message and return
        if not is_admin and not is_owner and not is_primary_owner:
            util.private_message(client, command.get("channel_id"),
                                 message="Sorry, you do not have permission to use this command.")
            return

        users_list = client.users_list()
        users = users_list["members"]
    except Exception as e:
        print(e)
        util.private_message(client, channel_id,
                             message="Rate limit error: Unable to retrieve users list as rate limit has been reached. Please try again in a few minutes.")
        return
    channel_id = command.get("channel_id")

    options = []
    for user in users:
        if user["is_bot"] == False:
            is_admin = user["is_admin"]
            is_owner = user["is_owner"]
            is_primary_owner = user["is_primary_owner"]
            is_bot = user["is_bot"]
            # split by underscore to remove any "_" in the name
            # then join the list back together
            user_id = user["id"]
            if is_admin or is_owner or is_primary_owner or is_bot or user_id == "USLACKBOT":
                continue

            user_name = " ".join(user["real_name"].split("_"))

            options.append({
                "text": user_name.title(),
                "value": f"{user_id}_{user_name}"
            })

    if len(options):
        util.private_message(client, channel_id,  message="Please select a user you would like to track", attachments=[
            {
                "text": '''List of users available to track''',
                "fallback": "Error: unable to generate menu buttons",
                "callback_id": "user_options",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "user_list",
                        "text": "Select a user...",
                        "type": "select",
                        "options": options
                    }
                ]
            }
        ]
        )
    else:
        util.private_message(client, channel_id,
                             message="No users available to track. Please add more users to continue.")


# Listen for a button invocation with callback_id `user_options`
@app.action("user_options")
def handle_user_options(ack, respond, action, context, client):
    '''
    Sends a request to the user selected asking for consent to be tracked
    '''
    # required: used to acknowledge that the request was received from Slack
    ack()
    try:

        channel_id = context.get("channel_id")
        user_id = context.get("user_id")
        selected_user_id, selected_user_name = action.get(
            "selected_options")[0].get("value").split("_")

        # check if selected_user_id already exists within mongodb
        user_doc = db.get_doc(selected_user_id, db.all_profiles_col)

        # if the user document exists, append user_id to the admin_ids array if it is not already inside
        if user_doc:
            if user_id in user_doc["admin_ids"]:
                respond(f"You are already tracking {selected_user_name}")
                return

        # otherwise, send a message to the other user_id to notify them that they have been selected to be tracked
        util.private_message(client, selected_user_id,
                             message=f"Hey there! VibeCheck would like to use your messages to help your mentor better understand you and to facilitate a better onboarding experience. To consent to this, please copy the message below and send it to your mentor <@{user_id}>:\n\n`{constants.CONSENT_MESSAGE}{user_id}`")

        respond(
            f"You have successfully sent a request to {selected_user_name} to be tracked by VibeCheck.")
        return

    except Exception as e:
        respond(f"Failed to track user. Please try again in a few minutes.")
        util.private_message(client, channel_id, f"{e}")


@app.message(re.compile(constants.CONSENT_MESSAGE))
def consent_message(event, client):
    '''
    Find the consent message. Split by the consent message to extract out the mentor's user_id.
    Then, add the mentor's user_id to the mentee's document in the database.
    '''
    channel_id = event.get("channel")
    user_id = event.get("user")
    # get user_info
    user_info = client.users_info(user=user_id)
    # get real name
    real_name = user_info["user"]["real_name"]
    message = event.get("text")
    try:
        # split by the consent message to extract out the mentor's user_id
        mentor_id = message.split(constants.CONSENT_MESSAGE)[1]
        # get the mentee's document
        mentee_doc = db.get_doc(user_id, db.all_profiles_col)
        print(
            f"mentee_doc: {mentee_doc} | mentor_id: {mentor_id} | channel_id: {channel_id}")
        # if the mentee's document exists
        if mentee_doc:
            # add the mentor's user_id to the mentee's document
            mentee_doc["admin_ids"][mentor_id] = channel_id
            # update the mentee's document in the database
            db.write_to_col(
                id=user_id, col=db.all_profiles_col, data=mentee_doc, is_update=True)
        # otherwise, create a new document with the following keys
        # (A) id = selected_user_id
        # (B) user_name = selected_user_name
        # (C) admin_ids = {mentor_id: channel_id}
        else:
            mentee_doc = {
                constants.ID: user_id,
                constants.REAL_NAME: real_name,
                constants.ADMIN_IDS: {
                    mentor_id: channel_id,
                }
            }
            # insert document into database
            db.write_to_col(col=db.all_profiles_col,
                            data=mentee_doc)

        # get mentor user info
        mentor_user_info = client.users_info(user=mentor_id)
        # get mentor real name
        mentor_real_name = mentor_user_info["user"]["real_name"]

        util.private_message(client, user_id,
                             message=f"Thank you for consenting to {mentor_real_name}'s request.")

    except Exception as e:
        print(f"Error: {e}")
        util.private_message(client, user_id, f"{e}")
        return

# VISUALISE COMMAND


@app.command("/visualise")
def visualise(ack, client, command):
    '''
    Visualise sentiments of messages sent to you by your interns
    '''
    # Acknowledge command request
    ack()
    channel_id = command.get("channel_id")

    # try:
    # get all messages where the recipient_id is the current user_id
    user_id = command.get("user_id")
    all_messages_for_user = db.get_messages_for_current_user(user_id)
    top_sentiment = util.get_insights(all_messages_for_user)

    # read image file contents as bytes
    filename = "wordcloud.png"

    with open(filename, 'rb') as file_data:
        bytes_content = file_data.read()

        client.files_upload_v2(
            token=constants.SLACK_BOT_TOKEN,
            channel=channel_id,
            title="Word Cloud",
            filename=filename,
            file=bytes_content,
            initial_comment=f"You received *{len(all_messages_for_user)}* messages from your interns. The most common sentiment was *{top_sentiment}*.")

    # respond("File uploaded!")

    # except Exception as e:
    #     print(e)
    #     util.private_message(client, channel_id,
    #                          message=f"Error: {e}")
    #     return


# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
# @slack_events_adapter.on("message")
# Matches all messages without a subtype


@ app.event("message")
def message(event, client):
    '''
    If the user is an admin, and the user receives a DM, this bot will analyse the sentiments of this message and send back the message with the sentiment score.

    Thereafter, the bot will add this message to a database.
    '''
    try:
        # if the message is sent by the bot, return
        if event.get("message") and event.get("message").get("subtype") == "bot_message":
            return
        channel_id = event.get("channel")
        team_id = event.get("team")
        text = event.get("text")
        user_id = event.get("user")
        user_info = client.users_info(user=user_id)
        real_name = user_info["user"]["real_name"]
        # attempt to retrieve user document from mongodb
        user_doc = db.get_doc(user_id, db.all_profiles_col)
        # if the user does not exist, return
        if not user_doc:
            return
        # otherwise, retrieve the admin_ids array
        admin_ids = user_doc[constants.ADMIN_IDS]

        labels, scores = util.analyse_message(
            text=text, team_id=team_id)

        top_sentiment = labels[0]

        # for each user id in the list of admin_ids, send a private message to the admin with the sentiment score
        for mentor_id, mentor_channel_id in admin_ids.items():
            if mentor_channel_id == channel_id:
                # note: we are sending the message back to the mentor_id instead of the mentor_channel_id
                # because the bot does not have enough permissions to send a message directly to a private channel between two users
                message = f'''
{real_name}: {text}
Sentiment: *{top_sentiment.title()} * ({scores[0]*100: .2f}%)'''

                prompt = util.get_suggested_prompt(
                    top_sentiment, message=text, team_id=team_id)
                if prompt:
                    message += f"\n\n\n*Suggested Reply*:\n{prompt}"

                util.private_message(client, mentor_id, message=message)

                message_doc = {
                    constants.ID: uuid4().hex[:16],
                    # channel_id = the id of the private channel between the mentor and mentee
                    constants.CHANNEL_ID: channel_id,
                    constants.USER_ID: user_id,
                    constants.REAL_NAME: real_name,
                    constants.RECIPIENT_USER_ID: mentor_id,
                    constants.MESSAGE: text,
                    constants.SUGGESTED_PROMPT: prompt,
                    constants.SENTIMENT_LABELS: labels,
                    constants.SENTIMENT_SCORES: scores,
                }

                # upload the message to the database
                db.write_to_col(col=db.all_messages_col, data=message_doc)

    except Exception as e:
        print(f"Error: {e}")
        util.private_message(client, channel_id, f"{e}")


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    serve(flask_app, host="0.0.0.0", port=constants.PORT or 8000)
