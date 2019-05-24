from KnowlegeBase import KnowledgeBase
import re
from Rule import Rule


class ExpertSystem:
    _KB = KnowledgeBase("knowledgebase.json")

    def print(self):
        if not self._KB.answers:
            print("I don't know how to help you. Need more knowledge.")
        else:
            print("Tell me what is the lowest probability you care about? (0,100).")
            que = input()

            while not re.match("[0-9]", que):
                print("Insert number in (0,100).")
                que = input()

            answ = self._KB.Bayes()
            coef = 0
            lister = []
            newlist = []
            for a in answ:
                coef += answ[a]

            for a in answ:
                answ[a] = answ[a] / coef
                lister.append({a: answ[a] * 100})

            newlist = sorted(lister, key=lambda k: k[list(k.keys())[0]], reverse=True)

            if int(que) > newlist[0][list(newlist[0])[0]]:
                print("No rules like that :(")
            else:
                count = 0
                for item in newlist:
                    for key in item:
                        if float(item[key]) > float(que):
                            print("== " + str(count) + " == ")
                            print(self._KB.messages[key] + " [{0:.2f} %]".format(item[key]))
                            count += 1
            print("-----------------------\nNumber of results: "+str(len(self._KB.answers)) )
    def check_possible(self):
        if self._KB.rules:
            for rule in self._KB.rules:

                if rule.validate() is False:
                    self._KB.rules.remove(rule)

                elif rule.validate() is True:
                    self._KB.append_another_rule(rule)

                elif rule.count_none() is 1 and not rule.is_deductable(self._KB.questions):
                    if self._KB.try_prove(rule):
                        pass

    def ask(self):
        while len(self._KB.answers) is 0 and self._KB.rules:
            self._KB.ask_rule()
            self._KB.select_rule()

    def how(self):
        print("\nIf you want to know how type [how all - how <id> - exit]")
        a = input()

        if a == "how all":
            if not self._KB.answers:
                print("No condition fulfilled.")
            else:
                for fact in self._KB.answers:
                    print()
                    print(self._KB.messages[fact])
                    print("Deducted from: ")
                    for answer in self._KB.proven_rules:
                        if fact in answer.get_conclusion():
                            for lit in answer.get_condition():
                                text = ""
                                if lit in self._KB.questions:
                                    text = str(self._KB.questions[lit])
                                else:
                                    text = "[Deducted fact] " + str(
                                        self._KB.get_rule_by_conclusion(lit)) + " was proven:"
                                print("" + text + " " + str(self._KB.facts[lit]))
            return None
        elif "how" in a:
            a = a.strip("how")
            answer = a.strip(" ")
            try:
                int(a)
            except ValueError:
                print("Wrong input.")
                return None
            if int(a) not in range(0, len(self._KB.answers)):
                print("Index out of range.")
                return None
            print()
            print(self._KB.messages[self._KB.answers[int(answer)]])
            print("Deducted from: ")
            answer = self._KB.get_rule_by_conclusion(self._KB.answers[int(answer)])

            for fact in self._KB.answers:
                if fact in answer.get_conclusion():
                    for lit in answer.get_condition():
                        text = ""
                        if lit in self._KB.questions:
                            text = str(self._KB.questions[lit])
                        else:
                            text = "[Deducted fact] " + str(
                                self._KB.get_rule_by_conclusion(lit)) + " was proven:"
                        print("" + text + " " + str(self._KB.facts[lit]))
            return None
        elif a == "exit":
            return None
        else:
            print("I don't understand.")
            return self.how()


ES = ExpertSystem()
ES.ask()
ES.check_possible()
ES.print()
ES.how()
print("\nThank you!")

input()