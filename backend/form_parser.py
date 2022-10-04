QUESTION_TEMPLATE = """
__Subject:__ {subject}
__Topic:__ {topic}

---
Q) {question} 

Options:
{'\n'.join([chr(i + 97).upper() + ') ' + option for i, option in enumerate(options)])}

Solutions are: {', '.join([chr(sol + 97).upper() for sol in solutions])}
"""

ISSUE_TEMPLATE = """
# Human Readable Format

{question_body}

# JSON
```json
{parsed_json}
```
"""


def parse_form_to_db_format(form_data):
    return {
        form_data["subject"]: {
            form_data["topic"]: [
                form_data["question"], *parse_options_for_json(form_data)
            ]
        }
    }


def parse_options_for_json(form_data):
    text_option_keys = []
    correct_option_keys = []

    for key in form_data.keys():
        if not key.startswith("option-"):
            continue
        if key.endswith("-text"):
            text_option_keys.append(key)
        elif key.endswith("-correct"):
            correct_option_keys.append(key)

    text_option_keys = sorted(text_option_keys, key=lambda k: int(k.split("-")[1]))
    correct_option_keys = sorted(correct_option_keys, key=lambda k: int(k.split("-")[1]))

    return [int(key.split("-")[1]) - 1 for key in correct_option_keys], [form_data[key] for key in text_option_keys]


def parse_form_to_github_issue(form_data):
    subject = form_data["subject"]
    topic = form_data["topic"]
    question = form_data["question"]
    solutions, options = parse_options_for_json(form_data)

    question_body = QUESTION_TEMPLATE.format(
        subject=subject, topic=topic, question=question, options=options, solutions=solutions
    )
    parsed_json = parse_form_to_db_format(form_data)

    return ISSUE_TEMPLATE.format(question_body=question_body, parsed_json=parsed_json)
