import numpy as np

import pygame
import pygame.freetype

from ghd_rref import rref  # Row reduced echelon form


### Globals ###
pygame.init()
GAME_FONT = pygame.freetype.Font("fonts/segoeui.ttf", 22)

adj = [[0, 0], [0, -1], [-1, 0], [0, 1], [1, 0]]

# Ok 5x5
cells = np.array([
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1]
])

# cells = np.array([
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 1, 0, 1, 0]
# ])

# # OK 3x3
# cells = np.array([
#     [0, 1, 0],
#     [1, 0, 1],
#     [0, 1, 0]
# ])

# # OK 3x3
# cells = np.array([
#     [0, 0, 0],
#     [0, 0, 0],
#     [1, 0, 0]
# ])

# # No solution
# cells = np.array([
#     [1, 1, 0, 0, 1],
#     [1, 1, 1, 1, 0],
#     [1, 0, 0, 0, 1],
#     [1, 0, 0, 1, 1],
#     [1, 0, 0, 1, 0]]
# )

# cells = np.ones((10,10))

### CONSTANTS ###
SIDE_BAR_WIDTH = 200
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
TILE_HEIGHT = 500/len(cells)
TILE_WIDTH = 500/len(cells)
MARGIN = 2

### COLORS ###
GHD_GREEN = (24, 240, 141)  # rgb(24, 240, 141)
GHD_DARK_BLUE = (17, 32, 44)  # rgb(17, 32, 44)
GHD_LIGHT_GRAY = (50, 69, 83)  # rgb(50, 69, 83)
GHD_RED = (226, 23, 88)  # rgb(226, 23, 88)

### Game class ###
class Game:
    def __init__(self, cells):
        self.cells = cells
        self.clear()
        self.load_level()
        self.has_solution = True
        self.rank = np.linalg.matrix_rank(cells)
        self.show_hints = False
        self.solved_yet = False

    def clear(self):
        self.grid = np.zeros_like(self.cells)
        self.hint = np.zeros_like(self.cells)

    def load_level(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                self.grid[x][y] = int(self.cells[y][x])

    def draw_ui(self):
        # Rank UI
        GAME_FONT.render_to(screen, (SCREEN_WIDTH+55, 45),
                            "Rank:  ", GHD_DARK_BLUE)
        GAME_FONT.render_to(screen, (SCREEN_WIDTH+115, 47),
                            f"{self.rank}", GHD_GREEN)

        # Has solution UI
        GAME_FONT.render_to(screen, (SCREEN_WIDTH+12, 90),
                            "Has Solution:      ", GHD_DARK_BLUE)
        if self.solved_yet:
            if self.has_solution:
                GAME_FONT.render_to(
                    screen, (SCREEN_WIDTH+140, 91), "True ", GHD_GREEN)
            else:
                GAME_FONT.render_to(
                    screen, (SCREEN_WIDTH+140, 91), "False", GHD_RED)
        else:
            GAME_FONT.render_to(
                screen, (SCREEN_WIDTH+140, 100), "...", GHD_DARK_BLUE)

        # Solve Button UI
        AAfilledRoundedRect(screen, [SCREEN_WIDTH+3*MARGIN, SCREEN_HEIGHT -
                            120+MARGIN, 200-8*MARGIN, 100-4*MARGIN], GHD_GREEN, radius=0.2)
        GAME_FONT.render_to(screen, (SCREEN_WIDTH+3*MARGIN+60,
                            SCREEN_HEIGHT-120+MARGIN+40), "SOLVE", GHD_DARK_BLUE)

    def draw_hint(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells)):
                h = 20
                w = h
                i = x * TILE_WIDTH + TILE_WIDTH//2 - w//2
                j = y * TILE_HEIGHT + TILE_HEIGHT//2 - h//2
                if self.hint[y][x] == 1:
                    AAfilledRoundedRect(
                        screen, [i, j, w, h], (255, 255, 255, 170), radius=0.99)

    def draw_grid(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells)):
                i = x * TILE_WIDTH + MARGIN
                j = y * TILE_HEIGHT + MARGIN
                h = TILE_HEIGHT - (2 * MARGIN)
                w = TILE_WIDTH - (2 * MARGIN)
                if self.grid[y][x] == 1:
                    AAfilledRoundedRect(
                        screen, [i, j, w, h], GHD_GREEN, radius=0.2)
                else:
                    AAfilledRoundedRect(
                        screen, [i, j, w, h], GHD_DARK_BLUE, radius=0.2)

    def draw(self):
        # 1. Draw the Grid
        self.draw_grid()

        # 2. Draw the UI
        self.draw_ui()

        # 3. Draw hints if the solve button has been clicked
        if self.show_hints:
            self.draw_hint()

    def get_adjacent(self, x, y):
        adjs = []
        for i, j in adj:
            if (0 <= i + x < len(self.cells)) and (0 <= j + y < len(self.cells)):
                adjs += [[i + x, j + y]]
        return adjs

    def click(self, pos):
        # Check if the user has clicked inside of the grid boundary
        if pos[0] <= SCREEN_WIDTH:
            # Handle Gameplay clicks
            x = int(pos[0] / TILE_WIDTH)
            y = int(pos[1] / TILE_HEIGHT)
            adjs = self.get_adjacent(x, y)
            for i, j in adjs:
                self.grid[j][i] = (self.grid[j][i] + 1) % 2

            self.cells = self.grid.T
            self.rank = np.linalg.matrix_rank(self.cells)
        else:
            # Handle Menu UI
            if SCREEN_WIDTH+3*MARGIN <= pos[0] <= SCREEN_WIDTH+3*MARGIN+200-8*MARGIN and SCREEN_HEIGHT-120+MARGIN <= pos[1] <= SCREEN_HEIGHT-120+MARGIN+100-4*MARGIN:
                self.show_hints = True
                self.solve()
            else:
                print("Clicked out of bounds!", pos)

    def solve(self):
        n = self.cells.shape[0]
        A = np.zeros((n**2, n**2), dtype=np.float64)
        for i in range(n**2):
            x = i//n
            y = i % n
            adjacents = self.get_adjacent(x, y)
            for adjacent in adjacents:
                A[i][adjacent[0]*n+adjacent[1]] = 1

        print("\n1. Adjacency Matrix (A):")
        print(A.astype(np.uint))
        print()

        state_vector = self.cells.flatten().reshape(-1, 1)
        print("2.1 State vector (state_vector):")
        print(state_vector.astype(np.uint))
        print()

        Aug_A = np.hstack((A, state_vector))
        print("2.2 Augmented Matrix (A | state_vector):")
        print(Aug_A.astype(np.uint))
        print()

        print("3. Row Reduction (rrefed_Aug_A):")
        rrefed_Aug_A = rref(Aug_A)
        print(rrefed_Aug_A.astype(np.uint))
        print()

        print("Answer:")
        answer = rrefed_Aug_A[:, -1].reshape(-1, 1)
        print(answer.reshape(n, n).astype(np.uint).T)

        # Check if there is a 00000|b row: no answer
        is_consistent = True
        for row in rrefed_Aug_A:
            if np.all(row[:-1] == 0) and row[-1] != 0:
                is_consistent = False

        if is_consistent:
            self.has_solution = True
            self.show_hints = True
            self.hint = answer.reshape(n, n).T
        else:
            print("No solution!")
            self.has_solution = False
            self.show_hints = False

        self.solved_yet = True
        print("Done")


def AAfilledRoundedRect(surface, rect, color, radius=0.4):
    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(
        circle, [int(min(rect.size)*radius)]*2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


### Main ###
if __name__ == "__main__":

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH + SIDE_BAR_WIDTH, SCREEN_HEIGHT))
    screen.fill(GHD_LIGHT_GRAY)
    pygame.display.set_caption("Lights Out Puzzle")

    game = Game(cells.T)
    game.draw()

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        screen.fill(GHD_LIGHT_GRAY)
        game.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.click(pos)
        pygame.display.flip()
    pygame.quit()
