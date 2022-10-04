import argparse
import subprocess
import json

# Find project root
project_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
data_file_path = project_root + "/src/data.json"

# Parsers
parser = argparse.ArgumentParser(
    description="A CLI tool to manage the database of the JEEPYQREPLYBOT."
)
subparsers = parser.add_subparsers(title="Commands", dest="command", required=True)

# Add Command
add_command = subparsers.add_parser("add", help="Append a question to the database.")
add_command.add_argument(
    "-d", "--dry-run", help="If passed", action="store_true"
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
        subject = input("Enter the subject [P/C/M]: ").lower()
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


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        if args.command == "add":
            add_question(args.dry_run)
    except KeyboardInterrupt:
        print("\n\nexiting...")
