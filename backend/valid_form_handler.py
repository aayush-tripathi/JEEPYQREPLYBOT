import os
from dotenv import load_dotenv

from github_api import GithubApp
from form_parser import parse_form_to_github_issue

load_dotenv(".env")

KEY = os.environ.get("KEY_FILE_PATH")
APP_ID = os.environ.get("APP_ID")

app = GithubApp(KEY, APP_ID)


def handle_valid_form(form_data):
    owner, repository = os.environ.get("MAIN_REPOSITORY").split("/")
    issue_title = "[New Question]: " + form_data["question"][:30]
    issue_body = parse_form_to_github_issue(form_data)
    app.create_issue(owner, repository, issue_title, issue_body)
