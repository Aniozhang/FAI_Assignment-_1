import pygame
import numpy as np

# Constants
gridSize = 6
cellSize = 40
screenSize = gridSize * cellSize
fps = 60

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Colors for the shapes
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Red, Green, Blue, Yellow

# Shapes
shapes = [
    np.array([[1]]),  # 1x1 square
    np.array([[1, 0], [0, 1]]),  # 2x2 square with holes
    np.array([[0, 1], [1, 0]]),  # 2x2 square with holes
    np.array([[1, 0], [0, 1], [1, 0], [0, 1]]),  # 2x4 rectangle with holes
    np.array([[0, 1], [1, 0], [0, 1], [1, 0]]),  # 2x4 rectangles with holes
    np.array([[1, 0, 1, 0], [0, 1, 0, 1]]),  # 4x2 rectangle with holes
    np.array([[0, 1, 0, 1], [1, 0, 1, 0]]),  # 4x2 rectangles with holes
    np.array([[0, 1, 0], [1, 0, 1]]),  # T shape with holes
    np.array([[1, 0, 1], [0, 1, 0]])  # T shape with holes
]

# Global variables
screen = None
clock = None
grid = None
currentShapeIndex = None
currentColorIndex = None
shapePos = None
placedShapes = None


def drawGrid(screen):
    for x in range(0, screenSize, cellSize):
        for y in range(0, screenSize, cellSize):
            rect = pygame.Rect(x, y, cellSize, cellSize)
            pygame.draw.rect(screen, black, rect, 1)


def drawShape(screen, shape, color, pos):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                rect = pygame.Rect((pos[0] + j) * cellSize, (pos[1] + i) * cellSize, cellSize, cellSize)
                pygame.draw.rect(screen, color, rect)


def canPlace(grid, shape, pos):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                if pos[0] + j >= gridSize or pos[1] + i >= gridSize:
                    return False
                if grid[pos[1] + i, pos[0] + j] != -1:
                    return False
    return True


def placeShape(grid, shape, pos, colorIndex):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                grid[pos[1] + i, pos[0] + j] = colorIndex


def removeShape(grid, shape, pos):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                grid[pos[1] + i, pos[0] + j] = -1


def checkGrid(grid):
    if -1 in grid:
        return False

    for i in range(gridSize):
        for j in range(gridSize):
            color = grid[i, j]
            if i > 0 and grid[i - 1, j] == color:
                return False
            if i < gridSize - 1 and grid[i + 1, j] == color:
                return False
            if j > 0 and grid[i, j - 1] == color:
                return False
            if j < gridSize - 1 and grid[i, j + 1] == color:
                return False
    return True


def exportGridState(grid):
    return grid
    # return ''.join(chr(cell + 65) for row in grid for cell in row)


def importGridState(gridState):
    grid = np.array([ord(char) - 65 for char in gridState]).reshape((gridSize, gridSize))
    return grid


def setup(GUI=True):
    global screen, clock, grid, currentShapeIndex, currentColorIndex, shapePos, placedShapes

    if GUI:
        pygame.init()
        screen = pygame.display.set_mode((screenSize, screenSize))
        pygame.display.set_caption("Shape Placement Grid")
        clock = pygame.time.Clock()

    grid = np.full((gridSize, gridSize), -1)
    currentShapeIndex = 0
    currentColorIndex = 0
    shapePos = [0, 0]
    placedShapes = []


def loop_gui():
    global currentShapeIndex, currentColorIndex, shapePos, grid, placedShapes

    running = True
    while running:
        screen.fill(white)
        drawGrid(screen)
        drawShape(screen, shapes[currentShapeIndex], colors[currentColorIndex], shapePos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    shapePos[1] = max(0, shapePos[1] - 1)
                elif event.key == pygame.K_DOWN:
                    shapePos[1] = min(gridSize - len(shapes[currentShapeIndex]), shapePos[1] + 1)
                elif event.key == pygame.K_LEFT:
                    shapePos[0] = max(0, shapePos[0] - 1)
                elif event.key == pygame.K_RIGHT:
                    shapePos[0] = min(gridSize - len(shapes[currentShapeIndex][0]), shapePos[0] + 1)
                elif event.key == pygame.K_RETURN:
                    if canPlace(grid, shapes[currentShapeIndex], shapePos):
                        placeShape(grid, shapes[currentShapeIndex], shapePos, currentColorIndex)
                        placedShapes.append((currentShapeIndex, shapePos.copy(), currentColorIndex))
                        if checkGrid(grid):
                            print("All cells are covered with no overlaps and no adjacent same colors!")
                        else:
                            print("Grid conditions not met!")
                elif event.key == pygame.K_w:
                    currentShapeIndex = (currentShapeIndex + 1) % len(shapes)
                elif event.key == pygame.K_s:
                    currentColorIndex = (currentColorIndex + 1) % len(colors)
                elif event.key == pygame.K_u:  # Undo the last placed shape
                    if placedShapes:
                        lastShapeIndex, lastShapePos, lastColorIndex = placedShapes.pop()
                        removeShape(grid, shapes[lastShapeIndex], lastShapePos)
                elif event.key == pygame.K_e:  # Export the grid state
                    gridState = exportGridState(grid)
                    print("Exported Grid State:", gridState)
                elif event.key == pygame.K_i:  # Import the grid state, not needed for us.
                    # Dummy grid state for testing
                    dummyGridState = exportGridState(np.random.randint(-1, 4, size=(gridSize, gridSize)))
                    grid = importGridState(dummyGridState)
                    placedShapes.clear()  # Clear history since we are importing a new state

        # Draw already placed shapes
        for i in range(gridSize):
            for j in range(gridSize):
                if grid[i, j] != -1:
                    rect = pygame.Rect(j * cellSize, i * cellSize, cellSize, cellSize)
                    pygame.draw.rect(screen, colors[grid[i, j]], rect)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


def loop_terminal():
    global currentShapeIndex, currentColorIndex, shapePos, grid, placedShapes

    print("Enter commands (W/A/S/D to move, E to place, Q to quit, U to undo, C to change shape, K to change color):")
    running = True
    while running:
        command = input("Command: ").strip().upper()
        if command == 'Q':
            running = False
        elif command == 'W':
            shapePos[1] = max(0, shapePos[1] - 1)
        elif command == 'S':
            shapePos[1] = min(gridSize - len(shapes[currentShapeIndex]), shapePos[1] + 1)
        elif command == 'A':
            shapePos[0] = max(0, shapePos[0] - 1)
        elif command == 'D':
            shapePos[0] = min(gridSize - len(shapes[currentShapeIndex][0]), shapePos[0] + 1)
        elif command == 'E':
            if canPlace(grid, shapes[currentShapeIndex], shapePos):
                placeShape(grid, shapes[currentShapeIndex], shapePos, currentColorIndex)
                placedShapes.append((currentShapeIndex, shapePos.copy(), currentColorIndex))
                if checkGrid(grid):
                    print("All cells are covered with no overlaps and no adjacent same colors!")
                else:
                    print("Grid conditions not met!")
        elif command == 'C':
            currentShapeIndex = (currentShapeIndex + 1) % len(shapes)
        elif command == 'K':
            currentColorIndex = (currentColorIndex + 1) % len(colors)
        elif command == 'U':  # Undo the last placed shape
            if placedShapes:
                lastShapeIndex, lastShapePos, lastColorIndex = placedShapes.pop()
                removeShape(grid, shapes[lastShapeIndex], lastShapePos)

        # Display grid state
        printGridState(grid)


def printGridState(grid):
    for row in grid:
        print(' '.join(f'{cell:2}' for cell in row))
    print()


def main():
    print("Select mode: 1 for GUI, 2 for Terminal")
    mode = input("Mode: ").strip()
    setup(True if mode == '1' else False)
    if mode == '1':
        loop_gui()
    elif mode == '2':
        loop_terminal()


def printControls():
    print("Use arrows to move the shapes in GUI mode.")
    print("Use W/A/S/D to move the shapes in Terminal mode.")
    print("Use W/C to change the shape.")
    print("Use S/K to change the color.")
    print("Press Enter/E to place the shape.")
    print("Press U to undo the last placed shape.")
    print("Press E to export the grid state.")
    print("Press I to import a dummy grid state.")
    print("Press Q to quit.")
    print("Press any key to continue")

if __name__ == "__main__":
    printControls()
    main()
