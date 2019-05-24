class Rule:

    def get_condition(self):
        return self._condition

    def get_conclusion(self):
        return self._name

    def __init__(self, container):
        self._name = list(container.keys())[0]
        self._condition = list(container.values())[0]

    def __repr__(self):
        string = ''
        length = len(self._condition)
        for key in self._condition.keys():
            length -= 1
            if length == 0:
                string += key + ' = ' + self._condition[key] + ' => '
            else:
                string += key + ' = ' + self._condition[key] + ' ^ '
        string += self._name
        return string
