import os
from dotenv import load_dotenv


load_dotenv()

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PORT = os.environ.get("PORT")

# all_profiles keys
ID = "id"
REAL_NAME = "real_name"
ADMIN_IDS = "admin_ids"
TIME = "time"
TIME_FORMATTED = "time_formatted"
TIME_CREATED = "time_created"
TIME_CREATED_FORMATTED = "time_created_formatted"

# all_messages keys
MESSAGE = "message"
CHANNEL_ID = "channel_id"
USER_ID = "user_id"
RECIPIENT_USER_ID = "recipient_user_id"
SENTIMENT_LABELS = "sentiment_labels"
SENTIMENT_SCORES = "sentiment_scores"
SUGGESTED_PROMPT = "suggested_prompt"

# all_teams keys
POSITIVE_LABELS = "positive_labels"
NEGATIVE_LABELS = "negative_labels"

# default sentiment labels

DEFAULT_POSITIVE_LABELS = ["contented", "confident", "excited"]
DEFAULT_NEGATIVE_LABELS = ["uneasy", "confused",
                           "tired", "overwhelmed"]

# message to consent to tracking
CONSENT_MESSAGE = "Hi, I consent to being tracked by VibeCheck to facilitate a better onboarding experience. My code is: "
