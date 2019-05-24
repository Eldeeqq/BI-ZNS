class Rule:

    # gives a A => B form of an rule
    def __repr__(self):

        lnd = list(self._condition.keys())
        condition = "( "
        for x in range(0, len(lnd)):
            if not self._condition[lnd[x]]:
                condition += '!'
            condition += lnd[x]
            if x != len(lnd) - 1:
                condition += ' ^ '
            if x == len(lnd) - 1:
                condition += " )"

        lnd = list(self._conclusion.keys())
        conclusion = "( "
        for x in range(0, len(lnd)):
            if not self._conclusion[lnd[x]]:
                conclusion += '!'
            conclusion += lnd[x]
            if x != len(lnd) - 1:
                conclusion += ' ^ '

        return str(condition) + " => " + str(conclusion) + " ) "

    # constructor
    def __init__(self, facts, condition, conclusion, uncertainty):

        self._condition = dict()
        self._conclusion = dict()
        self._checker = facts
        self._uncertainty = uncertainty

        # init condition
        for literal in condition:
            _temp = list(literal.keys())[0]

            # if fact doesnt exist create it
            if not (_temp in facts):
                facts[_temp] = None

            # links checker
            self._condition.update(literal)

        # init conclusion
        for literal in conclusion:
            _temp = list(literal.keys())[0]
            self._conclusion.update({_temp: literal[_temp]})

            if _temp not in self._checker:
                self._checker.update({_temp: None})

    # getters
    def get_condition(self):
        return self._condition

    def get_conclusion(self):
        return self._conclusion

    def get_uncertainty(self):
        return self._uncertainty

    def validate(self):
        has_false = False
        has_none = False

        for key in self._condition:
            has_none += self._checker[key] is None
            has_false += self._checker[key] != self._condition[key] and self._checker[key] is not None

        if bool(has_false):
            return False

        elif bool(has_none):
            return None
        else:
            return True

    def count_none(self):
        count = 0
        for x in self._condition:
            if self._checker[x] is None:
                count += 1
        return count

    def is_deductable(self, questions):
        dedu_count = 0
        for x in self._condition:
            if x not in questions:
                dedu_count += 1
        return dedu_count > 0

    def has_implied(self, inter_rule):
        for x in self._condition:
            if x in inter_rule:
                return True
        return False
