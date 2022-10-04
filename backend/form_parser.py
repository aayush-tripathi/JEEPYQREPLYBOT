def parse_form(form_data):
    return {
        form_data["subject"]: {
            form_data["topic"]: [
                form_data["question"], *parse_options(form_data)
            ]
        }
    }


def parse_options(form_data):
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
