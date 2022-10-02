from lark import Lark, Transformer, Token
from typing import List

# Same contents as in the file grammar.lark, setting it as a variable in the transpiler file itself so that I don't have
# to deal with finding the grammar file if not run in this directory itself.
grammar = r"""
start                   : assignments*


assignments             : subject_assignment
                        | topic_assignment
                        | question_assignment
                        | options_assignment
                        | solutions_assignment


subject_assignment      : SUBJECT_START ASSIGNMENT_OPERATOR SUBJECT
                        | SUBJECT_START ASSIGNMENT_OPERATOR STRING
topic_assignment        : TOPIC_START ASSIGNMENT_OPERATOR STRING
question_assignment     : QUESTION_START STRING
options_assignment      : OPTIONS_START ASSIGNMENT_OPERATOR options_list
solutions_assignment    : SOLUTIONS_START ASSIGNMENT_OPERATOR solutions_list


options_list            : OPTION_INDEX STRING (SEPERATOR OPTION_INDEX STRING)*
solutions_list          : LETTER (SEPERATOR LETTER)*


SUBJECT_START           : "subject"i | "sub"i
TOPIC_START             : "topic"i
QUESTION_START          : "Q)"i | "Q."i
OPTIONS_START           : "options"i
SOLUTIONS_START         : "solution"i | "solutions"i | "soln"i | "solns"i

SUBJECT                 : "physics"i | "chemistry"i | "mathematics"i
                        | "phy"i | "phys"i | "chem"i | "maths"i | "math"i

ASSIGNMENT_OPERATOR     : "=" | ":" | "is"i | "are"i
SEPERATOR               : "," | /\n/
OPTION_INDEX            : /[a-z][.)]/i
LETTER                  : /[a-z A-Z]/
STRING                  : /@[^@]*@/


%import common.WS
%ignore WS
"""

parser = Lark(grammar)


def sort_options(raw_options_list):
    option_dict = {key.lower(): val for key, val in raw_options_list}
    options = []
    for index in sorted(option_dict.keys()):
        options.append(option_dict[index])
    return options


# noinspection PyMethodMayBeStatic,PyPep8Naming
class QuestionToJSON(Transformer):
    """
    This is the Reddit Comment Question Format (RCQF) to JSON transpiler. It will parse a valid comment (as defined in
    grammar.lark) to JSON with the keys: ["subject", "topic", "question", "solutions", "options"].
    """

    # Alias names for each subject
    SUBJECT_MAP = {
        "physics": ("physics", "phy", "phys"),
        "chemistry": ("chemistry", "chem"),
        "mathematics": ("mathematics", "maths", "math")
    }

    ###########################################################################
    # MAIN PARSING
    def start(self, tokens):
        return {key: value for key, value in tokens}

    def assignments(self, tokens):
        return tokens[0]

    ###########################################################################
    # ASSIGNMENTS
    def subject_assignment(self, tokens: List[Token]):
        for token in tokens:
            if token.type == "SUBJECT":
                return "subject", token.value

    def topic_assignment(self, tokens: List[Token]):
        for token in tokens:
            if token.type == "STRING":
                return "topic", token.value

    def question_assignment(self, tokens: List[Token]):
        for token in tokens:
            if token.type == "STRING":
                return "question", token.value

    def options_assignment(self, tokens: List[Token]):
        return "options", tokens[-1]

    def solutions_assignment(self, tokens: List[Token]):
        return "solutions", tokens[-1]

    ###########################################################################
    # SEQUENCES
    def options_list(self, tokens: List[Token]):
        options = []
        current_index, current_value = None, None

        for token in tokens:
            if token.type == "OPTION_INDEX":
                current_index = token.value
            elif token.type == "STRING":
                current_value = token.value
            elif token.type == "SEPERATOR":
                options.append((current_index, current_value))
            else:
                raise Exception("Invalid token type inside options list.")

        options.append((current_index, current_value))  # since the last option will not have a seperator at the end.
        return sort_options(options)

    def solutions_list(self, tokens: List[Token]):
        solutions = []
        for token in tokens:
            if token.type == "LETTER":
                solutions.append(token.value)
        return solutions

    ###########################################################################
    # TERMINALS
    def SUBJECT(self, token: Token):
        for proper_subject_name, aliases in self.SUBJECT_MAP.items():
            if token.value in aliases:
                token.value = proper_subject_name
        return token

    def STRING(self, token: Token):
        token.value = token.value[1:-1]
        return token


def parse_comment(source):
    tree = parser.parse(source)
    proto_dict = QuestionToJSON().transform(tree)
    return {
        proto_dict["subject"].title(): {
            proto_dict["topic"]: [
                proto_dict["question"],
                [ord(index.lower()) - 97 for index in proto_dict["solutions"]],  # Converts Alphabets to Numeric Indices
                proto_dict["options"]
            ]
        }
    }


if __name__ == "__main__":
    print(parse_comment("""
Subject is physics
Topic is @XYZ topic in physics@

Q) @Why does X do Y when Z happens?@

Options are
A) @Because XYZ@
B) @Because XZY@
C) @Because ZXY@
D) @Because ZYX@

Solutions are A, C
    """))

    print(parse_comment("""
Sub: physics
Topic = @XYZ topic in physics@

Q) @Why does X do Y when Z happens?
And what if I add a newline to this question?@

Options = A) @Because XYZ@, B) @Because XZY@, C) @Because ZXY@, D) @Because ZYX@, E) @Because YZX@

Solution is E
    """))
