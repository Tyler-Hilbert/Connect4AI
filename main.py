import numpy as np
from random import *


# Places piece
# 0 means piece could not be placed
def Place(turn, col, grid):
	for r in range (5, -1, -1):
		if grid[r,col] == '*':
			grid[r,col] = turn
			return 1

		if r == 0:
			print ("Row full")
			return 0


# Checks if the game is won..... a 0 means game has been won, 1 means keep playing
# TODO - check if all positions are being checked correctly... it's likely one of the edge positions isn't being checked
def CheckGrid(grid):
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
				print("Red wins vertical");
				return 0
			elif yCount==4:
				print("Yellow wins vertical")
				return 0

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
				print("Red wins horizontal");
				return 0
			elif yCount==4:
				print("Yellow wins horizontal")
				return 0

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
				print("Red wins diagonal (down right)")
				return 0
			elif yCount==4:
				print("Yellow wins diagonal (down right)")
				return 0

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
				print("Red wins diagonal (up left)");
				return 0
			elif yCount==4:
				print("Yellow wins diagonal (up left)")
				return 0


	return 1





# TODO - init function
# Create Grid
grid = np.repeat('*', 7*6).reshape(6, 7)

# Play game
turn = 'R'
print(grid, '\n')
while (CheckGrid(grid) == 1):
	while(Place(turn, randint(0,6), grid) == 0):
		pass

	print(grid, '\n')

	if turn == 'R':
		turn = 'Y'
	else:
		turn = 'R'
