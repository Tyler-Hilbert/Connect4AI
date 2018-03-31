import numpy as np
from random import *
import random



# Prints msg to console if enable is true
def PrintIfEnabled(msg, enabled):
	if enabled == True:
		print(msg)


# Places piece
# 0 means piece could not be placed
def Place(turn, col, grid, gameDisplay):
	for r in range (5, -1, -1):
		if grid[r,col] == '*':
			grid[r,col] = turn
			return 1

		if r == 0:
			PrintIfEnabled ("Row full", gameDisplay)
			return 0


# Checks if the game is won..... a R means game has been won by R, Y means game was won by Y, 1 means keep playing, T means tie
# TODO - check if all positions are being checked correctly... it's likely one of the edge positions isn't being checked
def CheckGrid(grid, gameDisplay):
	# Check vertical
	for c in range (0, 7):
		rCount = 0;
		yCount = 0;
		for r in range (0, 6):
			if grid[r, c] == 'R':
				rCount+=1
				yCount=0
			elif grid[r, c] == 'Y':
				yCount+=1
				rCount=0
			else:
				rCount=0;
				yCount=0;

			if rCount==4:
				PrintIfEnabled("Red wins vertical", gameDisplay);
				return 'R'
			elif yCount==4:
				PrintIfEnabled("Yellow wins vertical", gameDisplay)
				return 'Y'

	# Check horizontal
	for r in range (0, 6):
		rCount = 0;
		yCount = 0;
		for c in range (0, 7):
			if grid[r, c] == 'R':
				rCount+=1
				yCount=0
			elif grid[r, c] == 'Y':
				yCount+=1
				rCount=0
			else:
				rCount=0;
				yCount=0;

			if rCount==4:
				PrintIfEnabled("Red wins horizontal", gameDisplay);
				return 'R'
			elif yCount==4:
				PrintIfEnabled("Yellow wins horizontal", gameDisplay)
				return 'Y'

	# Check horizontals
	downRight = [[0,0], [0,1], [0,2], [0,3], [1,0], [2,0]]
	for pos in downRight:
		c=pos[1]-1 # Subtract 1 because incriments in each loop
		rCount = 0;
		yCount = 0;
		for r in range(pos[0], 6):
			c+=1
			if c==7:
				break;

			if grid[r, c] == 'R':
				rCount+=1
				yCount=0
			elif grid[r, c] == 'Y':
				yCount+=1
				rCount=0
			else:
				rCount=0;
				yCount=0;

			if rCount==4:
				PrintIfEnabled("Red wins diagonal (down right)", gameDisplay)
				return 'R'
			elif yCount==4:
				PrintIfEnabled("Yellow wins diagonal (down right)", gameDisplay)
				return 'Y'

	upLeft = [[3,0], [4,0], [5,0], [5,1], [5,2], [5,3]]
	for pos in upLeft:
		c=pos[1]-1 # Subtract 1 because incriments in each loop
		rCount = 0;
		yCount = 0;
		for r in range(pos[0], -1, -1):
			c+=1
			if c==7:
				break;

			if grid[r, c] == 'R':
				rCount+=1
				yCount=0
			elif grid[r, c] == 'Y':
				yCount+=1
				rCount=0
			else:
				rCount=0;
				yCount=0;

			if rCount==4:
				PrintIfEnabled("Red wins diagonal (up left)", gameDisplay);
				return 'R'
			elif yCount==4:
				PrintIfEnabled("Yellow wins diagonal (up left)", gameDisplay)
				return 'Y'


	# Check if board is full
	for c in range(0, 7):
		if grid[0, c] == '*':
			return 1

	return 'T'



def BestPlay(grid):
	# Check for win next play
	for c in range (0, 7):
		g = np.copy(grid)
		Place('R', c, g, gameDisplay)
		if CheckGrid(g, gameDisplay) == 'R':
			return c
	
	# Check for pieces that cause a loss next turn
	possibleMoves = []
	for c in range (0, 7):
		g = np.copy(grid)
		badMove = False
		Place('R', c, g, gameDisplay)
		# Check each possible opponent next move
		for opponentC in range (0, 7):
			opponentG = np.copy(g)
			Place('Y', opponentC, opponentG, gameDisplay)
			if CheckGrid(opponentG, False) == 'Y':
				badMove = True # Determine the move shouldn't be played
				break

		if badMove == False:
			possibleMoves.append(c)

	if len(possibleMoves):
		return random.choice(possibleMoves)

	return randint(0, 6)	

# Plays game. 
# Return 'Y' for yellow win and 'R' for red (AI) win
# Param gameDisplay: If information about the game should be printed
def PlayGame(gameDisplay):
	# Create Grid
	grid = np.repeat('*', 7*6).reshape(6, 7)

	# Play game
	turn = 'R'
	if gameDisplay:
		PrintIfEnabled(grid, gameDisplay)
		PrintIfEnabled('\n', gameDisplay)
	gameWinner = 1		# Who the game was won by..... A 1 will indicate the game is still being played.. This is updated in loop
	while (gameWinner== 1):
		if turn == 'R':
			Place(turn, BestPlay(grid), grid, gameDisplay)
		else:
			while(Place(turn, randint(0,6), grid, gameDisplay) == 0):
				pass

		gameWinner = CheckGrid(grid, gameDisplay)

		if gameDisplay:
			PrintIfEnabled(grid, gameDisplay)
			PrintIfEnabled('\n', gameDisplay)

		# Update turn
		if turn == 'R':
			turn = 'Y'
		else:
			turn = 'R'

	return gameWinner


numberOfTurns = 1000
rWins = 0
yWins = 0
tieCount = 0
gameDisplay = False		# If the game should print boards and info

for i in range (1, numberOfTurns+1):
	winner = PlayGame(gameDisplay)
	if winner == 'R':
		rWins += 1
	elif winner == 'Y':
		yWins += 1
	else:
		tieCount += 1

print ("R win ratio: ", rWins, " to ", numberOfTurns-tieCount, " tie count:", tieCount)