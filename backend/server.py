import os
from dotenv import load_dotenv
from urllib.parse import quote

from flask import Flask, request, redirect
from form_validator import validate_form
from valid_form_handler import handle_valid_form
from webhook_handler import WebhookHandler
from github_api import GithubApp

load_dotenv(__file__.removesuffix("server.py") + ".env")

KEY = os.environ.get("KEY_FILE_PATH")
APP_ID = os.environ.get("APP_ID")
OWNER, REPOSITORY = os.environ.get("MAIN_REPOSITORY").split("/")
ADMINS = os.environ.get("ADMINS").split(",")

app = Flask(__name__)
github_api = GithubApp(KEY, APP_ID)
webhook_handler = WebhookHandler(github_api, ADMINS)


@app.route('/form_submit', methods=['POST'])
def form_submit():
    form_data = dict(request.form)
    is_valid_form, err_msg = validate_form(form_data)
    base_url = form_data.get("url").split("index.html")[0].removesuffix("/")

    if is_valid_form:
        issue_id = handle_valid_form(form_data, github_api, OWNER, REPOSITORY)
        redirect_url = base_url + f"/submitted.html?id={issue_id}"
        return redirect(redirect_url)
    else:
        base_url = form_data.get("url").split("index.html")[0].removesuffix("/")
        redirect_url = base_url + "/invalid-form.html?err=" + quote(err_msg)
        return redirect(redirect_url)


@app.route('/pyqbot_webhook', methods=['POST'])
def pyqbot_webhook():
    webhook_handler.handle_event(request.json)
    return "Ok", 200


if __name__ == "__main__":
    app.run(port=50696)
