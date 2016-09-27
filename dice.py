from random import choice
import re

dice_pattern = re.compile("(?P<numdice>\d*)(?P<d>d)(?P<die>\d*)(?P<op>\+|\-)(?P<bonus>\d*)")

class Dice(object):
    SIDES = 2
    def __init__(self, num_rolls=1, b=0):
        self._nr    = num_rolls
    	self._bonus = b
        self._rolls = [0 for x in range(num_rolls)]
        self._sides = [i+1 for i in range(self.__class__.SIDES)]
        self.roll()
        self.sum()

    def __getitem__(self, index):
        return self._rolls[index]

    def __repr__(self):
        if (self._nr == 1): return str(self._rolls[0])
        else: return str(None)

    def __int__(self):
        if (self._nr == 1): return self._rolls[0]
        else: return None 

    def roll(self):
        for i in range(len(self._rolls)):
            self._rolls[i] = choice(self._sides)
        
    def sum(self):
        _sum = sum(self._rolls) + self._bonus
        self.sum = _sum if _sum > 1 else 1
        self.average = sum(self._rolls)/float(self._nr)


class d2(Dice):   SIDES = 2
class d3(Dice):   SIDES = 3
class d4(Dice):   SIDES = 4
class d6(Dice):   SIDES = 6
class d8(Dice):   SIDES = 8
class d10(Dice):  SIDES = 10
class d12(Dice):  SIDES = 12
class d20(Dice):  SIDES = 20
class d100(Dice): SIDES = 100

def roll(dice):
    d     = re.match(dice_pattern, dice)
    die   = int(d.group('die'))
    num   = int(d.group('numdice'))
    bonus = int(d.group('bonus'))
    if (d.group('op') == '-'):
    	bonus *= -1

    class ThisDie(Dice):
        SIDES = die
    d_roll = ThisDie(num, bonus)

    print d_roll.sum

roll('2d12-20')