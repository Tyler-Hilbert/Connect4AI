import numpy as np
from random import *
import random
from external_input import *
import model

Q1 = model.createModel()
Q2 = model.createModel()
try:
	Q1.load_weights("Q1.h5", by_name=True)
	Q2.load_weights("Q2.h5", by_name=True)
	print("Model weights loaded")
except Exception as e:
	print("Model weights failed to load")
	print(e)
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
		Place('R', c, g, False)
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
			Place('Y', opponentC, opponentG, False)
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
def PlayGame(gameDisplay, samples, epsilon):
	# Create Grid
	grid = np.repeat('*', 7*6).reshape(6, 7)

	# Play game
	turn = 'R'
	if gameDisplay:
		PrintIfEnabled(grid, gameDisplay)
		PrintIfEnabled('\n', gameDisplay)
	gameWinner = 1		# Who the game was won by..... A 1 will indicate the game is still being played.. This is updated in loop
	while (gameWinner == 1):
		state = 0
		# Create grids
		OneHotGrid = np.zeros((1,6, 7, 3))
		# Fill grid with what pieces are taken
		for c in range (0, 7):
			for r in range (0, 6):
				if grid[r, c] == 'Y':
					OneHotGrid[0, r, c, 1] = 1 
				elif grid[r, c] == 'R':
					OneHotGrid[0, r, c, 2] = 1
				else:
					OneHotGrid[0, r, c, 0] = 1
		gameBuffer.append([OneHotGrid])
		if (samples > 1):
			gameBuffer[samples].append(OneHotGrid)
			gameBuffer[samples-1][1] = OneHotGrid
			gameBuffer[samples-2][1] = OneHotGrid
		elif(samples == 1):
			gameBuffer[samples].append(OneHotGrid)
			gameBuffer[samples-1][1] = OneHotGrid
		elif(samples == 0):
			gameBuffer[samples].append(OneHotGrid)
		while (state == 0):
			if turn == 'R':
				guess = Q1.predict(OneHotGrid)
			else:
				guess = Q2.predict(OneHotGrid)
			gameBuffer[samples].append(guess)
			guessColumn = np.argmax(guess)
			if epsilon < random.random():
				guessColumn = random.randint(0,6)
			gameBuffer[samples].append(guessColumn)
			state = Place(turn, guessColumn, grid, gameDisplay)
		gameWinner = CheckGrid(grid, gameDisplay)
		if (gameWinner == 1):
			gameBuffer[samples].append(turnReward)
			
		elif (gameWinner == turn):
			gameBuffer[samples].append(1)
			gameBuffer[samples-1][3] = 0
		elif (gameWinner == "T"):
			gameBuffer[samples-1][3] = 0.1

		if gameDisplay:
			PrintIfEnabled(grid, gameDisplay)
			PrintIfEnabled('\n', gameDisplay)

		# Update turn
		if turn == 'R':
			turn = 'Y'
		else:
			turn = 'R'
		samples += 1
	return gameWinner, samples



# Setup game 
nEpochs = 50
nSamples = 20000 #Split between AIs
batch_size = 2000
gameDisplay = False		# If the game should print boards and info
turnReward = .01
gamma = .99
epsilon = 0.1
epsilonDecay = .9



for i in range (1, nEpochs+1):
	gameBuffer = []
	samples = 0
	numberOfGames = 0
	rWins = 0
	yWins = 0
	tieCount = 0
	while (samples < nSamples):
		(winner, samples) = PlayGame(gameDisplay, samples, epsilon)
		numberOfGames += 1
		if winner == 'R':
			rWins += 1
		elif winner == 'Y':
			yWins += 1
		else:
			tieCount += 1
	buffer1 = []
	buffer2 = []
	for i in range(0, nSamples, 2):
		buffer1.append(gameBuffer[i])
		buffer2.append(gameBuffer[i+1])
	array1 = np.zeros((int(nSamples/2),6,7,3))
	array2 = np.zeros((int(nSamples/2),7))
	for (i,state) in enumerate(buffer1):
		array1[i] = state[0]
		array2[i] = state[2]
		guess = np.argmax(state[2])
		Q = state[3]
		if state[3] == .01:
			Q += gamma*np.amax(Q1.predict(state[1]))
		array2[i][guess] = Q
	Q1.fit(x = array1, y = array2, batch_size = batch_size)
	array1 = np.zeros((int(nSamples/2),6,7,3))
	array2 = np.zeros((int(nSamples/2),7))
	for (i,state) in enumerate(buffer2):
		array1[i] = state[0]
		array2[i] = state[2]
		guess = np.argmax(state[2])
		Q = state[3]
		if state[3] == .01:
			Q += gamma*np.amax(Q2.predict(state[1]))
		array2[i][guess] = Q
	Q2.fit(x = array1, y = array2, batch_size = len(array1))
	print ("R win ratio: ", rWins, " to ", numberOfGames-tieCount, " tie count:", tieCount)
	epsilon *= epsilonDecay
	Q1.save("Q1.h5")
	Q2.save("Q2.h5")