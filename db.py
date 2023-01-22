import os
from datetime import datetime
import certifi
from pymongo import MongoClient
from copy import deepcopy
from dotenv import load_dotenv
import pytz

import constants
# Load environment variables from .env file
load_dotenv()

MONGO_DB = os.environ.get('MONGO_DB')
MONGO_URL = os.environ.get('MONGO_URL')
client = MongoClient(MONGO_URL, tlsCAFile=certifi.where())
database = client[MONGO_DB]

# MongoDB

all_profiles_col = database["all_profiles"]
all_messages_col = database["all_messages"]
all_teams_col = database["all_teams"]


def utc_to_eastern(naive, timezone="Canada/Eastern"):
    return naive.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(timezone))


def get_doc(id, col):
    find = {constants.ID: id}

    return col.find_one(find)


def get_messages_for_current_user(user_id):
    find = {
        constants.RECIPIENT_USER_ID: user_id,
    }

    return list(all_messages_col.find(find).sort(constants.TIME, -1))


def write_to_col(id=None, col=None, data=None, is_update=False, is_delete=False, upsert=False):
    '''
    If upsert == True, db will insert a document if no document exists and update if document exists

    Note: id is NOT needed if inserting a document
    '''

    now = utc_to_eastern(datetime.utcnow())
    time = f"{now.strftime('%B %d, %Y')} at {now.strftime('%H:%M:%S')}"

    find = {constants.ID: id}

    if is_update:
        data.update(
            {
                constants.TIME: now,
                constants.TIME_FORMATTED: time,
            }
        )

        col.update_one(find, {'$set': data}, upsert=upsert)
        return
    if is_delete:
        col.delete_many(find)
        return

    data.update(
        {
            constants.TIME_CREATED: now,
            constants.TIME_CREATED_FORMATTED: time,
        }
    )

    col.insert_one(data)
