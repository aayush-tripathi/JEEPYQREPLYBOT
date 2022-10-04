import re
import requests

with requests.get("https://raw.githubusercontent.com/TriAay249/JEEPYQREPLYBOT/master/src/data.json") as response:
    DB = dict(response.json())


def validate_form(form_data: dict):
    keys_are_valid, err_reason = validate_keys(form_data.keys())
    if not keys_are_valid:
        return False, err_reason
    return validate_values(form_data)


def validate_keys(keys):
    option_count = 0
    correct_option_count = 0

    for key in keys:
        key: str
        if key in ("subject", "topic", "question", "url"):
            continue
        elif validate_option_key(key):
            option_count += 1 if "text" in key else 0
            correct_option_count += 1 if "correct" in key else 0
        else:
            return False, "Invalid data field present in form."

    if option_count < 2:
        return False, "Form should have at least 2 options."
    elif correct_option_count == 0:
        return False, "At least one option should be correct."
    elif correct_option_count >= option_count:
        return False, "All options can't be correct."
    return True, ""


def validate_option_key(key):
    # valid example: option-1-text or option-20-correct
    return bool(re.fullmatch(r"option-[1-9]\d*-(correct|text)", key))


def validate_values(form_data):
    has_empty_values, err_msg = check_empty_values(form_data)
    if has_empty_values:
        return False, err_msg

    is_valid_subject = form_data["subject"] in DB.keys()
    if not is_valid_subject:
        return False, "No such subject exists in the database."

    is_valid_topic = form_data["topic"] in DB[form_data["subject"]].keys()
    if not is_valid_topic:
        return False, "No such topic exists in the database."

    is_duplicate_question = not check_duplicate_question(
        [field[0].lower() for field in DB[form_data["subject"]][form_data["topic"]]],
        form_data["question"]
    )

    if is_duplicate_question:
        return False, "A question like this already exists."
    return True, ""


def check_empty_values(form_data):
    for key in form_data.keys():
        if form_data[key] == "":
            return True, f"The data field '{key}' is empty."
    return False, ""


def check_duplicate_question(question_list, question):
    # TODO: implement more advanced search algorithms here to detect not just exactly same questions but similar
    #  questions too
    return question.lower() not in question_list
