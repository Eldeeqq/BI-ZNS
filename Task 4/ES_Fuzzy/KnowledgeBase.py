from Fact import Fact
from Rule import Rule
import json


class KnowledgeBase:
    _fact_definition = dict()
    _proven_facts = dict()
    _rule_list = list()
    _final_results = dict()

    def __init__(self, file):
        # loads data from file
        with open(file, "r+") as reader:
            data = reader.read()

        # loads fact definitions
        facts = json.loads(data)["FactBase"]
        for fact in facts:
            temp = Fact(fact)
            self._fact_definition.update({temp.get_name(): temp})
            del temp

        # loads rules
        rules = json.loads(data)["Rules"]
        for rule in rules:
            self._rule_list.append(Rule(rule))

        # loads results
        results = json.loads(data)["Results"]
        self._functions_final = results

        #print("KB done")

    def check_fact(self, key):
        fact = None
        for defined_fact in self._fact_definition:
            name = defined_fact.get_name()
            if name == key:
                print(defined_fact)
                fact = defined_fact.ask()
                print(fact)
                self._proven_facts.update(fact)
        return fact

    def _left(self, x, a, b):
        if x <= a:
            return 0
        elif x >= b:
            return 1
        elif a < x < b:
            return (x - a) / (b - a)
        else:
            print("Value error type left [" + x + "," + a + "," + b + "]")
            return None

    # calculates value in right domain
    def _right(self, x, c, d):
        if x <= c:
            return 1
        elif x >= d:
            return 0
        elif c < x < d:
            return (x - d) / (c - d)
        else:
            print("Value error type right [" + x + "," + c + "," + d + "]")
            return None

    def _fuzzy(self, num, v):
        return max(min(self._left(num, v[0], v[1]), 1, self._right(num, v[2], v[3])), 0)

    def ask(self):
        for rule in self._rule_list:
            condition = rule.get_condition()
            for item in condition.keys():
                if item not in self._proven_facts:
                    self._proven_facts.update((self._fact_definition[item]).ask())
        #print(self._proven_facts)
        for rule in self._rule_list:
            maxi = 0
            mini = 1
            # print(rule)
            condition = rule.get_condition()
            for key in condition.keys():
                # print(key)
                # print(self._proven_facts[key])
                # print(str(self._proven_facts[key][condition[key]]))
                mini = min(mini, self._proven_facts[key][condition[key]])
            #print(str(rule) + "->" + str(mini))
            if rule.get_conclusion() not in self._final_results:
                self._final_results.update({rule.get_conclusion(): mini})
            elif self._final_results[rule.get_conclusion()] < mini:
                self._final_results.update({rule.get_conclusion(): mini})
        #print(self._final_results)

        top = 0
        bot = 0
        for x in range(0, 11):
            micro = max(min(self._fuzzy(x, self._functions_final["no"]), self._final_results["no"]),
                        min(self._fuzzy(x, self._functions_final["maybe"]), self._final_results["maybe"]),
                        min(self._fuzzy(x, self._functions_final["yes"]), self._final_results["yes"]))
            top += x * micro
            bot += micro
        sum = top / bot
        print("\nThe result is "+str(round(sum,2))+"/10.")
