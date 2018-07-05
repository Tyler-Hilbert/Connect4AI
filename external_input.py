import numpy as np

# return the column number that should be guessed
def ExternalInput(grid):
	# Create grids
	playerGrid = np.zeros((6, 7))
	cpuGrid = np.zeros((6, 7))
	emptyGrid = np.zeros((6, 7))
	# Fill grid with what pieces are taken
	for c in range (0, 7):
		for r in range (0, 6):
			if grid[r, c] == 'Y':
				playerGrid[r, c] = 1 
			elif grid[r, c] == 'R':
				cpuGrid[r, c] = 1
			else:
				emptyGrid[r, c] = 1
	
	# At this point playerGrid, cpuGrid and emptyGrid will be set
	# playerGrid will be a 1 for any positions the player -- 'Y' -- has a piece
	# cpuGrid will be a 1 for any positions the cpu -- 'R' -- has a piece
	# emptyGrid will be a 1 for any positions that neither player has a piece


	# Return the column number (0 to 6 inclusive) that the cpu should play
	return 1