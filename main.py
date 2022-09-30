import os
import praw
from supabase_py import create_client, Client
from data_api import DataAPI
from Inorganicchemistry import *

from webserver import keep_alive
import time

# CREATING REDDIT INSTANCE
reddit = praw.Reddit(
    username=os.environ.get('praw_REDDIT_USERNAME'),
    password=os.environ.get('praw_REDDIT_PASSWORD'),
    client_id=os.environ.get('praw_REDDITAPI_CLIENT'),
    client_secret=os.environ.get('praw_REDDITAPI_SECRET'),
    user_agent="RandomPYQBOT")

# SUPABASE CONNECTION
url: str = os.environ.get("SUPABASE_URLRB1")
key: str = os.environ.get("SUPABASE_KEYRB1")
supabase: Client = create_client(url, key)
comments = supabase.table("CommentsID").select("*").execute()
RESPONDED = [comment['id'] for comment in comments.get("data", [])]

Subreddit = reddit.subreddit("JEENEETards")

api = DataAPI()

# submission.reply(body=bot_reply) future praw 8
keep_alive()
# submission.reply(body=bot_reply) future praw 8
while True:
    comments = supabase.table("CommentsID").select("*").execute()
    RESPONDED = [comment['id'] for comment in comments.get("data", [])]
    for submission in Subreddit.new(limit=60):
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:]
        while comment_queue:
            comment = comment_queue.pop(0)
            if 'pyq' in comment.body.lower() and comment.id not in RESPONDED:
                REPLY = api.random_question()
                comment.reply(REPLY)
                data = supabase.table("CommentsID").insert(
                    {"id": comment.id, "COMMENTBODY": comment.body}).execute()
                time.sleep(20)

            comment_queue.extend(comment.replies)
