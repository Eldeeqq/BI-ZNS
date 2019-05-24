import json
import random

# global lists and dicts
global_rules = []
global_questions = []
global_facts = {}
question_log = []
results = {}
final = None


class Rule:
    hypothesis = {}
    implicates = ""
    uncertainty = ""

    def __init__(self, hypothesis, implicates, uncertainty):
        self.hypothesis = hypothesis
        self._implicates = implicates
        self.uncertainty = uncertainty

        global global_rules
        global_rules.append(self)

    def __repr__(self):
        return str(str(self.hypothesis) + " -> " + self._implicates)


# Question self append to list
class Question:
    _text = ""
    _choices = {}
    _fact = ""
    _explain = ""

    def answered(self):
        response = input(self._text + '\n')

        # if user input is in choices
        if response in self._choices.keys():
            global_facts[self._fact] = self._choices[response]
            question_log.append(self)

            delete_contra(self._fact, not self._choices[response])
            global_questions.remove(self)
            return True

        # if user asks why
        if response not in self._choices.keys() and response == "why":
            print(self._explain + " It helps me prove:")
            print(get_rule_by_fact(self._fact))
            return False

        # if user input is invalid
        else:
            print("Invalid answer")
            return False

    def __repr__(self):
        return self._text

    def __init__(self, text, choices, fact, explain):
        self._text = text
        self._choices = choices
        self._fact = fact
        self._explain = explain

        global global_questions
        global_questions.append(self)


def delete_contra(fact, val):
    for x in global_rules:
        if fact in x.hypothesis:
            if x.hypothesis[fact] is val:
                global_rules.remove(x)


def check_rules():
    for item in global_rules:
        rules = item.hypothesis.copy()
        for x in item.hypothesis:
            if x in global_facts:
                if rules[x] == global_facts[x]:
                    # print(x)
                    rules.pop(x)
        item.hypothesis = rules
        if not item.hypothesis:
            # print("-> " + item._implicates)
            global_facts[item._implicates] = True
    check_final()


def load_knowledge_base(kb):
    with open(kb, 'r') as rule_file:
        rule_list = rule_file.read()

    base = json.loads(rule_list)
    for rule in base["rules"]:
        Rule(rule["hypothesis"], rule["implies"], rule["uncertainty"])
    # print(global_rules)

    for question in base["questions"]:
        Question(question["text"], question["choices"], question["implicate"], question["explain"])

    for result in base["results"]:
        global results
        results[result["fact"]] = result["text"]

    return True


def how(a, kb):
    if a is "quit":
        quit()

    if a is "how":
        for x in question_log:
            print("You answered " + str(global_facts[x._fact]) + " on " + x._text)
            print("which led me to " + final)
            load_knowledge_base(kb)
            final_rule = None
            for x in global_rules:
                if x._implicates == final:
                    final_rule = x
        print(final_rule)
    else:
        print("I don't understand.")

def check_final():
    for x in results:
        if x in global_facts:
            global final
            final = x


def get_rule_by_fact(key):
    for x in global_rules:
        if key in x.hypothesis:
            return str(x)


def response():
    print("I think you should " + results[final] + ".")


def ask():
    global global_questions
    global results
    check_final()
    while final is None and len(global_questions) > 0:
        rand = random.randrange(0, len(global_questions))

        while not global_questions[rand].answered():
            True
        try:
            check_rules()
        finally:
            pass


file = "KnowledgeBase.json"
print("Please answer 'yes' or 'no' to answer the question. Use 'why' if you need to know why am I asking.")
load_knowledge_base(file)
ask()
response()
how(input("(type quit to exit or why to find out how i found out)\n"), file)
