from form_parser import parse_form_to_github_issue


def handle_valid_form(form_data, app_api, owner, repository):
    issue_title = "[New Question]: " + form_data["question"][:30] + "..."
    issue_body = parse_form_to_github_issue(form_data)
    response = app_api.create_issue(owner, repository, issue_title, issue_body)
    return response["number"]
