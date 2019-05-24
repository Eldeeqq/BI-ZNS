import json
from Rule import Rule


class KnowledgeBase:
    # lists and dictionaries
    rules = []
    facts = {}
    questions = {}
    proven_rules = []
    answers = []
    messages = {}
    accuracy = {}
    inter_rule = []
    relations = {}
    # placeholders
    actual_rule = None
    all_rules = []
    btr = {}

    # constructor
    def __init__(self, data_file):
        # loads data
        with open(data_file, "r") as read_file:
            data = json.load(read_file)
        read_file.close()
        self.questions = data["questions"]
        self.messages = data["messages"]
        holder = data["rules"]
        self.inter_rule = data["deducted"]
        for rule in holder:
            self.rules.append(
                Rule(self.facts,
                     rule["condition"],
                     rule["conclusion"],
                     rule["uncertainty"]))

        self.rules = self.rules[::-1]
        self.relations = data["relations"]
        self.accuracy = data["accuracy"]
        self.all_rules = self.rules.copy()
        self.btr = data["additional"]
        self.select_rule()

    def get_rule_by_conclusion(self, fact):
        for x in self.proven_rules:
            if fact in x.get_conclusion():
                return x
        return None
    # rule selector
    def select_rule(self):
        if not self.rules:
            return False
        else:
            self.actual_rule = self.rules[len(self.rules) - 1]

    # asks for specific thing
    def ask_literal(self, literal):
        if literal in self.questions:
            print(self.questions[literal])
        else:
            return None

        response = input()

        if response == "yes":
            self.facts.update({literal: True})

        elif response == "no":
            self.facts.update({literal: False})

        elif response == "why":
            print("I want to prove: \n" + str(self.actual_rule) + "\n")
            return self.ask_literal(literal)

        else:
            print("I don't understand, chose from [ yes, no, why ]")
            return self.ask_literal(literal)

    # deletes x moves rule
    def take_care_of_rule(self):
        status = self.actual_rule.validate()

        if status is False:
            self.rules.pop(len(self.rules) - 1)
            self.actual_rule = None
            return None

        elif status is None:
            # print("An error occurred.")
            self.rules.pop(len(self.rules) - 1)
            self.actual_rule = None
            return None

        elif status is True:
            _temp = self.actual_rule.get_conclusion()
            for x in _temp:
                self.facts.update({x: _temp[x]})
                if x in self.messages:
                    self.answers.append(x)
            self.proven_rules.append(self.rules.pop(len(self.rules) - 1))
        self.actual_rule = None
        return None

    # asks user for actual rule
    def ask_rule(self):
        # print(self.actual_rule)
        a = self.actual_rule.validate()
        if a is None:
            for x in self.actual_rule.get_condition():
                if self.facts[x] is None:
                    self.ask_literal(x)

        self.take_care_of_rule()

    # adds another final rule after finding first one
    def append_another_rule(self, rule):
        conclusion = rule.get_conclusion()
        for x in conclusion:
            self.facts[x] = conclusion[x]
            if x in self.messages:
                self.answers.append(x)
        self.proven_rules.append(rule)

    # tries to prove another rule
    def try_prove(self, rule):
        condition = rule.get_condition()
        fact = None
        for x in condition:
            if self.facts[x] is None:
                fact = x
        self.ask_literal(fact)
        a = rule.validate()
        if a is False:
            return False
        if a is None:
            return None
        if a is True:
            self.append_another_rule(rule)
            return True

    def get_direct(self, answr):
        value = 1
        for x in self.relations[answr]:
            value *= self.relations[answr][x]
        value *= self.accuracy[answr]
        return value

    def find_similar(self, dic):
        dc = self.relations.copy()
        for x in self.relations:
            if not (dic.keys() <= self.relations[x].keys()):
                dc.pop(x)
        return dc

    def grbca(self, answer):
        b = self.get_direct(answer)
        dic = self.find_similar(self.relations[answer])
        sum = 0
        for x in dict:
            a=self.get_direct(x)
            sum += a
        return b/sum

    def get_answers_accuracy(self):
        acc = {}
        for fact in self.answers:
            acc.update({fact: self.grbca(fact)})
        return acc

    def final_containing(self, cond):
        temp = self.relations.copy()
        for x in self.relations:
            if not temp[x].keys() >= cond.keys():
                temp.pop(x)
        return temp

    def calc(self, ans, cond):
        num = 1
        for x in cond:
            if x in self.btr.keys():
                num *= self.relations[ans][x]*self.btr[x]
            else:
                num *= self.relations[ans][x]
        return num*self.accuracy[ans]

    def Bayes(self):
        final = {}
        for item in self.answers:
            cond = self.relations[item]
            temp = self.final_containing(cond)
            top = self.calc(item, cond)
            bot = 0
            for x in temp:
                bot += self.calc(x, cond)
            final.update({item: top/bot})
        #print(final)
        return final
