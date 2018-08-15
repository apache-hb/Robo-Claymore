#TODO get shit working

class TicTacToeException(Exception):
	pass

class OverwriteException(TicTacToeException):
	pass

class TicTacToeGame:
	def __init__(self):
		self.table = [
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0]
		]

	def set_tile(self, x, y, player):
		assert player in [1, 2], "Player must be 1 or 2"
		if self.table[y][x] != 0:
			raise OverwriteException()
		self.table[y][x] = player

	#return 0 if no winner, otherwise 1 or 2
	def get_winner(self) -> int:
		for x in range(1, 2):
			if all(y == x for y in self.table[z] for z in range(3)):
				return x
