import numpy as np
from random import *
import random
import model
import tqdm

Q1 = model.createModel()
Q2 = model.createModel()
try:
	Q1.load_weights("Q1.h5", by_name=True)
	print("Model Q1 weights loaded")
except Exception as e:
	print("Model Q1 weights failed to load")
	print(e)
try:
	Q2.load_weights("Q2.h5", by_name=True)
	print("Model Q2 weights loaded")
except Exception as e:
	print("Model Q2 weights failed to load")
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
def PlayGame(gameDisplay, samples, epsilon, trainingPlayer, length, gamePause):
	# Create Grid
	grid = np.repeat('*', 7*6).reshape(6, 7)

	# Play game
	if random.randint(0,1) == 0:
		turn = 'R'
	else:
		turn = 'Y'
	if gameDisplay:
		PrintIfEnabled(grid, gameDisplay)
		PrintIfEnabled('\n', gameDisplay)
		if gamePause:
			input()
	gameWinner = 1		# Who the game was won by..... A 1 will indicate the game is still being played.. This is updated in loop
	while (gameWinner == 1):
		state = 0
		# Create grids
		OneHotGrid = np.zeros((1,6, 7, 3))
		mask = np.ones((1,7,1))
		# Fill grid with what pieces are taken
		for c in range (0, 7):
			for r in range (0, 6):
				if grid[r, c] == 'Y':
					OneHotGrid[0, r, c, 1] = 1 
					if r == 0:
						mask[0,c,0] = 0
				elif grid[r, c] == 'R':
					OneHotGrid[0, r, c, 2] = 1
					if r == 0:
						mask[0,c,0] = 0
				else:
					OneHotGrid[0, r, c, 0] = 1
		gameBuffer=[[OneHotGrid, mask]]
		gameBuffer.append([OneHotGrid, mask])
		while (state == 0):
			if turn == 'R':
				guess = Q1.predict([OneHotGrid,mask])
			else:
				guess = Q2.predict([OneHotGrid,mask])
			
			gameBuffer.append(guess)
			guessColumn = np.argmax(guess)
			if epsilon > random.random() and turn == trainingPlayer:
				guessColumn = random.randint(0,6)
			# Overwrite Yellow guess with column one for training purposes
			if (turn == 'Y'):
				guessColumn = 1
				if (random.randint(0,10) == 0): # Chance to guess other to prevent getting stuck
					guessColumn = random.randint(0,6) 
			gameBuffer.append(guessColumn)
			state = Place(turn, guessColumn, grid, gameDisplay)
		gameWinner = CheckGrid(grid, gameDisplay)
		if (gameWinner == 1):
			gameBuffer.append(turnReward)
			
		elif (gameWinner == turn and gameWinner == trainingPlayer):
			gameBuffer.append(1)
		elif (gameWinner == "T"):
			gameBuffer.append(0.2)
		else:
			if trainingPlayer == "R":
				gameBuffer1[-1][3] = 0
			else:
				gameBuffer2[-1][3] = 0
		if trainingPlayer == "R" and turn == "R":
			gameBuffer1.append(gameBuffer)
			samples += 1
		elif trainingPlayer == "Y" and turn == "Y":
			gameBuffer2.append(gameBuffer)
			samples += 1
		if gameDisplay:
			PrintIfEnabled(grid, gameDisplay)
			PrintIfEnabled('\n', gameDisplay)
			if gamePause:
				input()
		# Update turn
		if turn == 'R':
			turn = 'Y'
		else:
			turn = 'R'
		length += 1
	return gameWinner, samples, length



# Setup game 
nEpochs = 500
nSamples = 10000#Split between AIs
batch_size = 1000
gameDisplay = False		# If the game should print boards and info
gamePause = True		# If game displays should pause after displaying
turnReward = .01
gamma = .98
epsilon = 0.2
epsilonDecay = .99



for i in range (1, nEpochs+1):
	print("\nEpoch ", i)
	gameBuffer1 = []
	gameBuffer2 = []
	samples1 = 0
	samples2 = 0
	numberOfGames1 = 0
	numberOfGames2 = 0
	length1 = 0
	length2 = 0
	rWins1 = 0
	yWins1 = 0
	tieCount1 = 0
	rWins2 = 0
	yWins2 = 0
	tieCount2 = 0
	print("Red playing")
	if not gameDisplay:
		pbar = tqdm.tqdm(total = nSamples)
		lastI = 0
	while (samples1 < nSamples):
		(winner, samples1, length1) = PlayGame(gameDisplay, samples1, epsilon, "R", length1, gamePause)
		numberOfGames1 += 1
		if not gameDisplay:
			pbar.update(samples1 - lastI)
			lastI = samples1
		if winner == 'R':
			rWins1 += 1
		elif winner == 'Y':
			yWins1 += 1
		else:
			tieCount1 += 1
	if not gameDisplay:
		pbar.close()
	array1 = np.zeros((int(nSamples),6,7,3))
	maskarray = np.zeros((int(nSamples),7,1))
	array2 = np.zeros((int(nSamples),7,1))
	for (i,state) in enumerate(gameBuffer1[:nSamples]):
		array1[i] = state[0][0]
		maskarray[i] = state[0][1]
		array2[i] = state[2]
		guess = np.argmax(state[2])
		Q = state[3]
		if state[3] == .01:
			Q += gamma*np.amax(Q1.predict(state[1]))
		array2[i][guess] = Q
	print("\nRed Training")
	Q1.fit(x = [array1, maskarray], y = array2, batch_size = batch_size)
	print ("R win ratio: ", rWins1, " to ", numberOfGames1-tieCount1, "\tPercent: ", round(100*rWins1/(numberOfGames1-tieCount1),2))
	print("Avg game length: ", round(length1/numberOfGames1,2), "\tTie count: ", tieCount1, "\tTie Percent: ", round(100*tieCount1/numberOfGames1,2))
	print("Epsilon: ", round(epsilon, 4))
