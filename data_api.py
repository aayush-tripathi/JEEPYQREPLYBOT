import json
import random


def random_choice(iterable):
    # Creating this so that if in the future we want to replace the python's random library with a better one, we won't
    # have to manually search and replace all usages.
    return random.choice(iterable)


def random_shuffle(iterable):
    random.shuffle(iterable)


class QuestionParser:
    COMMENT_TEMPLATE = """Here is a random jee previous year question for ya:

Q) {question}

>!Solution = {solution}!<   <--- Solution

Chapter = `{chapter_name}`

 - A)  {options[0]}
 - B)  {options[1]}
 - C)  {options[2]}
 - D)  {options[3]}"""

    def __init__(self, subject, topic, question_data):
        self.subject = subject
        self.topic = topic
        self.question_data = question_data
        self.__shuffle_options()

    @property
    def question_string(self):
        return self.question_data[0]

    @property
    def solutions(self):
        return self.question_data[1]

    @property
    def alphabetic_solutions(self):
        # Converts indices of solutions into alphabets
        # Example: [0, 1] will be converted to "A, B"
        solution_string = ""
        for solution in self.solutions:
            solution_letter = chr(97 + solution).upper()
            solution_string += solution_letter + ", "
        return solution_string.removesuffix(", ")

    @property
    def options(self):
        return self.question_data[2]

    def __shuffle_options(self):
        # This will randomize the options so that people don't memorize the option alphabet but rather focus on the
        # answer

        # temporary buffer to be able to find the indices of solutions after the options were shuffled
        solutions_buffer = [self.options[solution] for solution in self.solutions]

        random_shuffle(self.options)

        # Recalculate new solution indices
        new_solutions = []
        for solution in solutions_buffer:
            new_solutions.append(self.options.index(solution))
        self.question_data[1] = new_solutions

    def generate_comment_body(self):
        return self.COMMENT_TEMPLATE.format(
            question=self.question_string,
            solution=self.alphabetic_solutions,
            chapter_name=self.topic,
            options=self.options
        )


class DataAPI:
    def __init__(self, data_file="./data.json"):
        with open(data_file) as file:
            self.data: dict = json.load(file)

    def __random_subject(self):
        return random_choice(tuple(self.data.keys()))

    def __random_topic(self, subject):
        assert subject in self.data.keys()
        return random_choice(tuple(self.data[subject].keys()))

    def __random_question(self, subject, topic):
        assert subject in self.data.keys()
        assert topic in self.data[subject].keys()
        return random_choice(self.data[subject][topic])

    def random_question(self):
        subject = self.__random_subject()
        topic = self.__random_topic(subject)
        question_data = self.__random_question(subject, topic)
        return QuestionParser(subject, topic, question_data).generate_comment_body()
