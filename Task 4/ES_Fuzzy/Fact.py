import re

class Fact:

    # constructor
    def __init__(self, data):
        # set name
        self._name = list(data.keys())[0]
        # set question string
        data = list(data.values())[0]
        self._question = data[0].pop("question")
        # set list of values
        data = data[1].pop("values")
        self._values = dict()
        for value in data:
            self._values.update(value)

        #print(self._name + ' added to knowledgebase.')
        #print(self._get_min_max())

    # name getter
    def get_name(self):
        return self._name

    # value range getter
    def _get_min_max(self):
        mini = 0
        maxi = 0
        for x in self._values:
            val = self._values[x]
            if mini > val[0]:
                mini = val[0]
            if maxi < val[3]:
                maxi = val[3]
        return [mini, maxi]

    # calculates value in left domain
    def _left(self, x, a, b):
        if x <= a:
            return 0
        elif x >= b:
            return 1
        elif a < x < b:
            return (x - a) / (b - a)
        else:
            print("Value error type left ["+x+","+a+","+b+"]")
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
            print("Value error type right [" +  x + "," + c + "," + d + "]")
            return None


    # returns numeric value for value
    def _fuzzy(self, num, v):
        return max(min(self._left(num, v[0], v[1]), 1, self._right(num, v[2], v[3])), 0)

    def _get_value_list(self, num):
        fin_dict = dict()
        for val in self._values:
            ret = self._fuzzy(num, self._values[val])
            if ret is not None:
                fin_dict.update({val: ret})
        return fin_dict

    def ask(self):
        print("How much do I think you should get a coffe?\n")
        a = self._get_min_max()
        print("On the scale (" + str(a[0]) + "," + str(a[1]) + ")\n" + self._question)
        num = input()
        while not re.match("^ *[0-9]+\.*[0-9]*$", num) or not float(a[0]) <= float(num) <= float(a[1] ):
            print("Invalid input! Try again.")
            num = input()
        x = self._get_value_list(float(num))
        return {self._name: x}
