import pygame  # for visualizing the path
import math
from queue import PriorityQueue
# For the algorithm , will works as an auto-ordering list which is important when we want to decide which node we want to move to.

# Setting up the display, giving 800  and creating a square window by giving win=width,width
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
# pygame caption function, this will add a name in the top of the window
pygame.display.set_caption("A* Path Finding Algorithm")

# Initialising Different colours that will be used
# Using ALLCAPs as constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Creating a class for the spot


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        # x and y are the coordinates of the top left corner of the square
        self.color = WHITE  # default color
        self.neighbors = []  # list of neighbors
        self.width = width  # width of the square
        self.total_rows = total_rows

    # Indexing spots with rows and coloums
    def get_pos(self):
        return self.row, self.col
    # assigning the already looked at values

    def is_closed(self):
        return self.color == RED
    # assigning the open values

    def is_open(self):
        return self.color == GREEN
    # assigning the the closed values

    def is_barrier(self):
        return self.color == BLACK
    # assigning the start point

    def is_start(self):
        return self.color == ORANGE
    # assigning the end point

    def is_end(self):
        return self.color == TURQUOISE

    # assigning the reset task values
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    # assigning the make path values
    def make_path(self):
        self.color = PURPLE

    # creating our draw function
    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.width))

    # Making a function to find the neighbors of the spot
    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):  # basically a lessthan operator to make sure our values are always in the positive
        return False

# Defining the heuristic function of our algorithm


def h(p1, p2):
    # since we are using manhattan distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)  # abs is for absolute

# defining our path construction


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# defining our algorithm


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()  # keeping track our values
    open_set.put((0, count, start))
    came_from = {}  # keep track of our previous path
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0  # tracking our gscore
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())  # tracking our fscore

    # checking if values are in priority queue
    open_set_hash = {start}

    # Allowing the user to quit the mid pathfinding process
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # basically since at the end the algorithm is taking over the program with its own loop, we want a way to quit the program in between the algorithm. This will allow us to do that.

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)  # make path
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())

                # checking if there is another shoter path to the end
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    # choosing the new set of values with a shorter length

        draw()

        if current != start:
            # if current is not the start node make it close.
            current.make_closed()

            # if we are not able to find a path, then we will return false.
    return False

# making our grid


def make_grid(rows, width):
    grid = []  # basically its going to be alot of lists inside alot of lists
    gap = width // rows  # define the width of each spot / cube that we will work on
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

# Grid Lines


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap),
                         (width, i * gap))  # Horizontal Lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0),
                             (j * gap, width))  # Vertical Lines

# Main draw function of our grid


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

# Making the spot clickable


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# Creating our main event


def main(win, width):  # checking if everthing is set
    ROWS = 40  # can be changed
    grid = make_grid(ROWS, width)  # generate grid

    start = None
    end = None  # user defined

    run = True  # main loop
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # Allowing to quit mid program when clicked "X"

            # Making barriers, start and end points
            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]  # index of our rows and coloumn
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:  # start and end are not the same
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            # Removing barriers, start and end points
            elif pygame.mouse.get_pressed()[2]:  # right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:  # start
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    # start algo.
                    algorithm(lambda: draw(win, grid, ROWS, width),
                              grid, start, end)

                if event.key == pygame.K_c:  # reset
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)  # reset prog.

    pygame.quit()


main(WIN, WIDTH)
