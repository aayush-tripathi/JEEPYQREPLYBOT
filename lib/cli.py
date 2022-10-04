import argparse
import json
import os
import sys
import requests

# Find project root
project_root = __file__.removesuffix("/lib/cli.py")
data_file_path = project_root + "/src/data.json"
tmp_dir_path = project_root + "/tmp"
if not os.path.exists(tmp_dir_path):
    os.mkdir(tmp_dir_path)

# Parsers
parser = argparse.ArgumentParser(
    description="A CLI tool to manage the database of the JEEPYQREPLYBOT."
)
subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)

# Add Command
add_command = subparsers.add_parser("add", help="Append a question to the database.")
add_command.add_argument(
    "-d", "--dry-run", help="Will not make changes to database", action="store_true"
)
add_command.add_argument(
    "-p", "--patch", help="Pass the path to a JSON file to be merged into the database, not intended for use by humans",
)

# Parse JSON from issue
parse_command = subparsers.add_parser("parse", help="Parses different formats and creates a patch file in tmp/")
parse_command.add_argument(
    "-i", "--issue", help="Pass the issue number of the issue to be parsed"
)


def input_options():
    print("Input options, enter $$ to move to next option and @@ to move to next data field.")
    options = []

    while True:
        option_buffer = []
        print("Enter option:")

        while True:
            option_line = input(">>> ")
            if option_line not in ("$$", "@@"):
                option_buffer.append(option_line)
                continue
            break

        options.append("\n".join(option_buffer))
        if option_line != "@@":
            continue
        break

    if len(options) < 2:
        print("At least enter two options, try again.")
        return input_options()

    return options


def input_solutions(options):
    solutions = []
    print("Input solutions (in numeric indices starting from 0), enter @@ to finish.")
    while True:
        solution = input("Enter solution index: ")
        if solution == "@@":
            break
        elif len(solutions) == len(options) - 1:  # not every option can be the solution
            break
        elif solution.isdigit() and (0 <= int(solution) < len(options)):
            solutions.append(int(solution))
        else:
            print("Invalid solution, try again.")
    return solutions


def add_question(dry_run=True):
    # Input Subject
    while True:
        subject = input("Enter the subject [P/I/C/O/M]: ").lower()
        if subject not in ("p", "i", "c", "o", "m"):
            print("Please enter a valid subject.")
            continue
        break

    subject = {
        "p": "Physics",
        "i": "Inorganic Chemistry",
        "c": "Physical Chemistry",
        "o": "Organic Chemistry",
        "m": "Mathematics"
    }[subject]

    # Input Topic
    topic = input("Enter the topic: ")

    # Input Question
    question = ""
    question_buffer = []
    print("Enter the question (enter @@ to continue to the next data field):")
    while True:
        question_line = input(">>> ")
        if question_line.strip() != "@@":
            question_buffer.append(question_line)
            continue
        question = "\n".join(question_buffer)
        break

    # Input Options
    options = input_options()

    # Input Solutions
    solutions = input_solutions(options)

    # Main
    if dry_run:
        proto_dict = {
            subject: {
                topic: [
                    [question, solutions, options]
                ]
            }
        }
        print(json.dumps(proto_dict, indent=2))
    else:
        with open(data_file_path, "r") as file:
            data = json.load(file)
            if topic not in data[subject].keys():
                data[subject][topic] = []
            data[subject][topic].append([question, solutions, options])

        with open(data_file_path, "w") as file:
            json.dump(data, file)


def add_patch(patch_file_path):
    try:
        with open(patch_file_path) as patch_file:
            json_data = json.load(patch_file)
    except json.JSONDecodeError:
        print("invalid json passed")
        sys.exit(1)

    with open(data_file_path) as db:
        data = json.load(db)

    subject = list(json_data.keys())[0]
    topic = list(json_data[subject].keys())[0]
    question_data = json_data[subject][topic]
    data[subject] = data.get(subject, {topic: []})
    data[subject][topic] = data[subject].get(topic, [])
    data[subject][topic].append(question_data)

    with open(data_file_path, "w") as db:
        json.dump(data, db)


def parse_issue_body(body):
    return body.split("```json")[-1].strip().removesuffix("```")


def parse_issue(issue_number):
    with requests.get("https://api.github.com/repos/TriAay249/JEEPYQREPLYBOT/issues") as response:
        if not response.ok:
            raise Exception("Error fetching issue from GitHub api")
        issues = list(response.json())
    body = ""
    for issue in issues:
        if str(issue["number"]) == str(issue_number):
            body = issue["body"]
            break
    body = parse_issue_body(body)
    with open(tmp_dir_path + "/patch.json", "w") as file:
        json.dump(json.loads(body), file)


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        if args.command == "add":
            if args.patch is None:
                add_question(args.dry_run)
            else:
                add_patch(args.patch)
        if args.command == "parse":
            if args.issue is not None:
                parse_issue(args.issue)
    except KeyboardInterrupt:
        print("\n\nexiting...")
