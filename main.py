import numpy as np

# Checks if the game is won..... a 0 means game has been won, 1 means keep playing
def CheckGrid(grid):
	# Check vertical
	for c in range (0, 5):
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
		for c in range (0, 5):
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

grid = np.repeat(' ', 7*6).reshape(6, 7)
grid[5,0] = 'R'
grid[4,1] = 'Y'
grid[4,2] = 'R'
grid[2,3] = 'Y'
grid[4,0] = 'R'
grid[4,3] = 'R'
grid[0,6] = 'Y'
grid[1,5] = 'Y'
grid[2,4] = 'Y'
grid[3,3] = 'Y'
print(grid)

CheckGrid(grid)


