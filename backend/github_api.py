import time
import json

import jwt
import requests


# Errors
class HTTPError(Exception):
    def __init__(self, status_code):
        super().__init__(f"HTTP {status_code} error while trying to reach github API.")
        self.status_code = status_code


# Decorators
def automatic_jwt_renew(function):
    # decorators are new for me, if you know how to implement this better please do send a PR
    retry_buffer = 1

    def wrapper_function(*args, **kwargs):
        nonlocal retry_buffer
        self = args[0]
        try:
            return function(*args, **kwargs)
        except HTTPError as http_error:
            if http_error.status_code != 401 or retry_buffer >= self.RETRY_LIMIT:
                raise http_error
            self.update_jwt_token()
            retry_buffer += 1
            return wrapper_function(*args, **kwargs)

    return wrapper_function


def automatic_token_renew(function):
    retry_buffer = 1

    def wrapper_function(*args, **kwargs):
        nonlocal retry_buffer
        self = args[0]
        try:
            return function(*args, **kwargs)
        except HTTPError as http_error:
            if http_error.status_code != 401 or retry_buffer >= self.RETRY_LIMIT:
                raise http_error
            self.update_access_token()
            retry_buffer += 1
            return wrapper_function(*args, **kwargs)

    return wrapper_function


class GithubApp:
    API_BASE_URL = "https://api.github.com/"
    RETRY_LIMIT = 3

    def __init__(self, private_key_path: str, app_id: str | int):
        with open(private_key_path) as key_file:
            self.private_key = key_file.read()
        self.app_id = app_id

        self.jwt_token = None
        self.access_token = None

        self.update_jwt_token()
        self.update_access_token()

    @property
    def jwt_header(self):
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + self.jwt_token
        }

    @property
    def token_header(self):
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + self.access_token
        }

    def endpoint(self, endpoint: str):
        return self.API_BASE_URL.removesuffix("/") + "/" + endpoint.removeprefix("/")

    def update_jwt_token(self):
        # Ad defined on: https://docs.github.com/en/developers/apps/building-github-apps/authenticating-with-github-apps
        # In section: #authenticating-as-a-github-app
        payload = {
            # issued at time, 60 seconds in the past to allow for clock drift
            "iat": int(time.time()) - 60,
            # JWT expiration time (10 minute maximum)
            "exp": int(time.time()) + (10 * 60),
            # GitHub App's identifier
            "iss": self.app_id
        }

        self.jwt_token = jwt.encode(payload, self.private_key, algorithm="RS256")

    @automatic_jwt_renew
    def get_installations(self):
        endpoint = self.endpoint("app/installations")

        with requests.get(endpoint, headers=self.jwt_header) as response:
            if not response.ok:
                raise HTTPError(response.status_code)
            return response.json()

    @automatic_jwt_renew
    def get_installation_access_token(self):
        # This will get the installation access token for only the first item it finds in the installation list
        installation_id = self.get_installations()[0]["id"]
        endpoint = self.endpoint(f"app/installations/{installation_id}/access_tokens")

        with requests.post(endpoint, headers=self.jwt_header) as response:
            if not response.ok:
                raise HTTPError(response.status_code)
            return response.json()

    def update_access_token(self):
        self.access_token = self.get_installation_access_token()["token"]

    @automatic_token_renew
    def comment_on_issue(self, owner, repository, issue_number, comment_body):
        endpoint = self.endpoint(f"repos/{owner}/{repository}/issues/{issue_number}/comments")
        data = json.dumps({"body": comment_body})
        with requests.post(endpoint, headers=self.token_header, data=data) as response:
            if not response.ok:
                raise HTTPError(response.status_code)
            return response.json()

    @automatic_token_renew
    def create_issue(self, owner, repository, title, body="", labels=()):
        endpoint = self.endpoint(f"repos/{owner}/{repository}/issues")
        data = json.dumps({"title": title, "body": body, "labels": labels})
        with requests.post(endpoint, headers=self.token_header, data=data) as response:
            if not response.ok:
                raise HTTPError(response.status_code)
            return response.json()
