

class Integer:
    def __init__(self,num, offset):
        self.val = num
        self.offset = offset

    def __add__(self, other):
        return self.val + other

    def __str__(self):
        num = self.get_val()
        return str(num)

    def get_val(self):
        if (isinstance(self.val,Integer)):
            return self.val.get_val() + self.offset
        else:
            return self.val + self.offset
    def sum(self,int):
        self.val += int

