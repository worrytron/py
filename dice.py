from random import choice
import re

dice_pattern = re.compile("(?P<numdice>\d*)(?P<d>d)(?P<die>\d*)(?P<bonus>\+|\-)(?P<amount>\d*)")

class Dice(object):
	SIDES = 2
	def __init__(self, num_rolls=1):
		self._nr    = num_rolls
		self._rolls = [0 for x in range(num_rolls)]
		self._sides = [i+1 for i in range(self.__class__.SIDES)]
		self.roll()

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
		self.average = sum(self._rolls)/float(len(self._rolls))


class D2(Dice):   SIDES = 2
class D3(Dice):   SIDES = 3
class D4(Dice):   SIDES = 4
class D6(Dice):   SIDES = 6
class D8(Dice):   SIDES = 8
class D10(Dice):  SIDES = 10
class D12(Dice):  SIDES = 12
class D20(Dice):  SIDES = 20
class D100(Dice): SIDES = 100

class Attack(object):
	def __init__(self, dice)
		pass