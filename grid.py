import pygame

class DebugCell:
    def __init__(self, x : int, y : int, cell_size : int = 50, origin : tuple = (0,0)) -> None:
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.font = pygame.font.SysFont('Arial', 16)
        self.origin = origin

    def draw_cell(self, screen, value) -> None:
        pos_x = self.x * self.cell_size + self.origin[0]
        pos_y = self.y * self.cell_size + self.origin[1]
        rect = pygame.Rect(pos_x, pos_y, self.cell_size, self.cell_size)  # init rect
        pygame.draw.rect(screen, (200, 200, 200), rect)  # draw bg of rect
        pygame.draw.rect(screen, (10, 10, 10), rect, 1, 1)  # draw outline of rect
        text = self.font.render(str(value), True, (10, 10, 10))
        text_rect = text.get_rect(center=(pos_x + self.cell_size // 2, pos_y + self.cell_size // 2))
        screen.blit(text, text_rect)


class Grid:
    def __init__(self, width :int, height: int, cell_size : int = 50, origin : tuple = (0,0)) -> None:
        self.width = width
        self.height = height
        self.grid_list : [[int]] = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.cell_list : [[DebugCell]] = [[DebugCell(x,y, origin = origin) for y in range(self.width)] for x in range(self.height)]
        self.cell_size = cell_size
        self.origin = origin

    def get_cell_world_position(self, x :int, y :int) -> tuple:
        return (x * self.cell_size + self.origin[0], y * self.cell_size + self.origin[1])

    def __set_cell_value(self, pos : tuple, value :int) -> None:
        if pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.width and pos[1] < self.height:
            self.grid_list[pos[0]][pos[1]] = value

    def __get_cell(self, pos : tuple) -> tuple[int, int]:
        return (pos[0] // self.cell_size,pos[1] // self.cell_size)

    def draw_grid(self, screen) -> None:
        for x in range(self.width):
            for y in  range(self.height):
                self.cell_list[x][y].draw_cell(screen, self.grid_list[x][y])

    def set_cell_value(self, pos : tuple, value : int) -> None:
        self.__set_cell_value(self.__get_cell((pos[0] - self.origin[0], pos[1] - self.origin[1])), value)

    def get_cell_value(self, pos : tuple) -> int:
        x,y = pos
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return self.grid_list[x][y]
        return 0

    def get_cell_value_world(self, pos) -> int:
        x,y = self.__get_cell((pos[0] - self.origin[0], pos[1] - self.origin[1]))
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            return self.grid_list[x][y]
        return 0

def debug_grid():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Pygame Grid')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((20, 20, 20))

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Create the grid
    grid = Grid(8, 8, cell_size=50, origin=(100,150))
    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # mouse input
        if pygame.mouse.get_just_pressed()[0]:
            grid.set_cell_value(pygame.mouse.get_pos(), 1)
        if pygame.mouse.get_just_pressed()[2]:
            print(grid.get_cell_value_world(pygame.mouse.get_pos()))

        # draw the grid
        screen.blit(background, (0, 0))
        grid.draw_grid(screen)

        pygame.display.flip()

if __name__ == '__main__':
    debug_grid()