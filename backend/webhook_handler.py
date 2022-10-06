import json
import re
import requests


class WebhookHandler:
    EVENT_SIGNATURES = {
        "issue_comment": sorted(["action", "issue", "comment", "repository", "sender", "installation"])
    }

    def __init__(self, api, admins):
        self.api = api
        self.admins = [admin.lower() for admin in admins]

    def handle_event(self, event):
        event = dict(event)
        event_type = self.check_event_type(event)

        if event_type == "issue_comment":
            self.handle_issue_comment(event)

    def check_event_type(self, event):
        for event_type, signature_keys in self.EVENT_SIGNATURES.items():
            if sorted(event.keys()) == signature_keys:
                return event_type

    def handle_issue_comment(self, event):
        owner = event["repository"]["owner"]["login"]
        repository = event["repository"]["name"]
        sender = event["sender"]["login"]
        issue_number = event["issue"]["number"]

        if event["action"] != "created":
            return
        comment_body = event["comment"]["body"]
        if "pyqbot ping" in comment_body:
            self.handle_ping(owner, repository, issue_number, sender)
        elif "pyqbot close" in comment_body:
            self.handle_close_issue(owner, repository, issue_number)
        elif "pyqbot approve" in comment_body:
            self.handle_approved_question(owner, repository, issue_number, sender, event)

    def handle_ping(self, owner, repository, issue_number, sender):
        reply = f"@{sender}, pong!"
        self.api.comment_on_issue(owner, repository, issue_number, reply)

    def handle_close_issue(self, owner, repository, issue_number):
        self.api.close_issue(owner, repository, issue_number)

    def handle_approved_question(self, owner, repository, issue_number, sender, event):
        # Check admin rights
        if sender.lower() not in self.admins:
            return self.api.comment_on_issue(
                owner, repository, issue_number, "You don't have the appropriate rights to approve a question."
            )

        # Trigger GitHub Action
        event_type = f"Merge Question: #{issue_number}"
        client_payload = {"issue_id": issue_number}
        try:
            self.api.create_repository_dispatch(owner, repository, event_type, client_payload)
            self.api.comment_on_issue(
                owner, repository, issue_number, "Merge sequence initiated. Closing this issue now."
            )
            self.api.close_issue(owner, repository, issue_number)
        except Exception:
            self.api.comment_on_issue(
                owner, repository, issue_number, "An error occurred while trying to initiate merge sequence."
            )
