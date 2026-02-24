
class TicTacToe:
	def __init__(self):
		self.board = [' ' for _ in range(9)]
		self.scores = {'X': 0, 'O': 0}
		self.current_player = 'X'

	def print_board(self):
		print("\n")
		for i in range(3):
			print(' | '.join(self.board[i*3:(i+1)*3]))
			if i < 2:
				print("---------")
		print("\n")

	def make_move(self, position):
		if self.board[position] == ' ':
			self.board[position] = self.current_player
			return True
		return False

	def check_winner(self):
		win_combos = [
			[0,1,2], [3,4,5], [6,7,8], # rows
			[0,3,6], [1,4,7], [2,5,8], # columns
			[0,4,8], [2,4,6]           # diagonals
		]
		for combo in win_combos:
			if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
				return self.board[combo[0]]
		return None

	def is_draw(self):
		return all(cell != ' ' for cell in self.board)

	def switch_player(self):
		self.current_player = 'O' if self.current_player == 'X' else 'X'

	def reset_board(self):
		self.board = [' ' for _ in range(9)]

	def play(self):
		print("Tic Tac Toe: First to 3 points wins!")
		while max(self.scores.values()) < 3:
			self.reset_board()
			winner = None
			while not winner and not self.is_draw():
				self.print_board()
				try:
					pos = int(input(f"Player {self.current_player}, enter position (1-9): ")) - 1
					if pos < 0 or pos > 8:
						print("Invalid position. Try again.")
						continue
				except ValueError:
					print("Invalid input. Enter a number 1-9.")
					continue
				if not self.make_move(pos):
					print("Position already taken. Try again.")
					continue
				winner = self.check_winner()
				if not winner:
					self.switch_player()
			self.print_board()
			if winner:
				print(f"Player {winner} wins this round!")
				self.scores[winner] += 1
			else:
				print("It's a draw!")
			print(f"Scores: X = {self.scores['X']}, O = {self.scores['O']}")
		overall_winner = 'X' if self.scores['X'] == 3 else 'O'
		print(f"Player {overall_winner} wins the game with 3 points!")


if __name__ == "__main__":
	game = TicTacToe()
	game.play()
