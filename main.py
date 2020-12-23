import math
import time
import pygame

cell_number_width = 30
cell_color_height = 30
cell_width = 60
cell_height = 50
cell_border = 1
cell_clear_width = 50
cell_clear_height = 30
cell_clear_upper_margin = 10
cell_clear_lower_margin = 10
cell_clear_right_margin = 10


def draw_background(game_display):
    game_display.fill((255, 255, 255))
    # horizontal
    for i in range(9):
        rect = (0, cell_color_height + i * (cell_height + cell_border),
                cell_number_width + 3 * (cell_width + cell_border), cell_border)
        pygame.draw.rect(game_display, (0, 0, 0), rect, 0)

    # vertical
    for i in range(3):
        rect = (cell_number_width + i * (cell_width + cell_border), 0,
                cell_border, cell_color_height + 8 * (cell_height + cell_border))
        pygame.draw.rect(game_display, (0, 0, 0), rect, 0)

    # numbers
    font = pygame.font.SysFont("Arial", 24)
    for i in range(1, 9):
        size = font.size(str(i))
        num = font.render(str(i), 1, (0, 0, 0), (255, 255, 255))
        game_display.blit(num, ((cell_number_width - size[0]) / 2,
                                cell_color_height + cell_border + (i - 1) * (cell_height + cell_border) + (
                                        cell_height - size[1]) / 2))

    # colors
    font = pygame.font.SysFont("Arial", 12)
    for i, color in enumerate(("Niebieski", "Czerwony", "Żółty")):
        size = font.size(color)
        col = font.render(color, 1, (0, 0, 0), (255, 255, 255))
        game_display.blit(col, (
            cell_number_width + cell_border + i * (cell_width + cell_border) + (cell_width - size[0]) / 2,
            (cell_color_height - size[1]) / 2))

    # clear button
    rect = (cell_number_width + 3 * (cell_width + cell_border) - cell_clear_right_margin - cell_clear_width,
            cell_color_height + 8 * (cell_height + cell_border) + cell_border + cell_clear_upper_margin,
            cell_clear_width,
            cell_clear_height)
    pygame.draw.rect(game_display, (0, 0, 0), rect, cell_border)

    font = pygame.font.SysFont("Arial", 12)
    size = font.size("Wyczyść")
    clear = font.render("Wyczyść", 1, (0, 0, 0), (255, 255, 255))
    game_display.blit(clear, (
        cell_number_width + 3 * (cell_width + cell_border) - cell_clear_right_margin - cell_clear_width + (
                cell_clear_width - size[0]) / 2,
        cell_color_height + 8 * (cell_height + cell_border) + cell_border + cell_clear_upper_margin + (
                cell_clear_height - size[1]) / 2))

    pygame.display.update()


def clear_cells(game_display):
    for i in range(3):
        color = [(0, 0, 255), (255, 0, 0), (255, 242, 0)][i]
        for j in range(8):
            rect = (cell_number_width + i * (cell_width + cell_border) + cell_border,
                    cell_color_height + j * (cell_height + cell_border) + cell_border,
                    cell_width,
                    cell_height)
            pygame.draw.rect(game_display, color, rect, 0)
    pygame.display.update()


def update_cell(tile_x, tile_y, cell, game_display):
    rect = (cell_number_width + tile_x * (cell_width + cell_border) + cell_border,
            cell_color_height + tile_y * (cell_height + cell_border) + cell_border,
            cell_width,
            cell_height)
    color = [(0, 0, 255), (255, 0, 0), (255, 242, 0)][tile_x]
    pygame.draw.rect(game_display, color, rect, 0)

    if cell == 1:
        # draw X
        size = int(0.6 * min(cell_width, cell_height))
        up = cell_color_height + tile_y * (cell_height + cell_border) + cell_border + (cell_height - size) / 2
        down = cell_color_height + tile_y * (cell_height + cell_border) + cell_border + (cell_height + size) / 2
        left = cell_number_width + tile_x * (cell_width + cell_border) + cell_border + (cell_width - size) / 2
        right = cell_number_width + tile_x * (cell_width + cell_border) + cell_border + (cell_width + size) / 2

        pygame.draw.line(game_display, (0, 0, 0), (left, up), (right, down), 4)
        pygame.draw.line(game_display, (0, 0, 0), (left, down), (right, up), 4)

    elif cell == 2:
        # draw O
        radius = int(0.3 * min(cell_width, cell_height))
        x = cell_number_width + tile_x * (cell_width + cell_border) + cell_border + int(cell_width / 2)
        y = cell_color_height + tile_y * (cell_height + cell_border) + cell_border + int(cell_height / 2)
        pygame.draw.circle(game_display, (0, 0, 0), (x, y), radius, 4)

    pygame.display.update()


def key_pressed(i, position, cells, game_display):
    tile_x = math.floor((position[0] - cell_number_width) / cell_width)
    tile_y = math.floor((position[1] - cell_color_height) / cell_height)

    if 0 <= tile_x <= 2 and 0 <= tile_y <= 7:
        if cells[tile_x][tile_y] == i + 1:
            cells[tile_x][tile_y] = 0
        else:
            cells[tile_x][tile_y] = i + 1
        update_cell(tile_x, tile_y, cells[tile_x][tile_y], game_display)
        print("x:{0}\ty:{1}".format(tile_x, tile_y))

    else:
        if cell_number_width + 3 * (cell_width + cell_border) - cell_clear_right_margin - cell_clear_width <= position[0] <= \
                cell_number_width + 3 * (cell_width + cell_border) - cell_clear_right_margin and \
                cell_color_height + 8 * (cell_height + cell_border) + cell_border + cell_clear_upper_margin <= position[1] <= \
                cell_color_height + 8 * (cell_height + cell_border) + cell_border + cell_clear_upper_margin + cell_clear_height:
            for i in range(3):
                for j in range(8):
                    cells[i][j] = 0
            clear_cells(game_display)
            print("clear")


def get_input(buttons_pressed, cells, game_display):
    mouse_keys = pygame.mouse.get_pressed()[::2]
    for i in range(2):
        if mouse_keys[i]:
            if not buttons_pressed[i]:
                key_pressed(i, pygame.mouse.get_pos(), cells, game_display)
                # print("{0} pressed".format(["lmb", "rmb"][i]))
                buttons_pressed[i] = True
        else:
            buttons_pressed[i] = False
    return buttons_pressed


if __name__ == "__main__":
    pygame.init()
    game_display = pygame.display.set_mode((cell_number_width + 3 * (cell_width + cell_border),
                                            cell_color_height + 8 * (
                                                    cell_height + cell_border) + cell_border + cell_clear_upper_margin + cell_clear_height + cell_clear_lower_margin))
    draw_background(game_display)
    clear_cells(game_display)

    cells = [[0 for _ in range(8)] for _ in range(3)]
    buttons_pressed = [False, False]
    run = True
    target_fps = 60
    prev_time = time.time()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        buttons_pressed = get_input(buttons_pressed, cells, game_display)

        # Handle time
        curr_time = time.time()
        diff = curr_time - prev_time
        delay = max(1.0 / target_fps - diff, 0)
        time.sleep(delay)
        fps = 1.0 / (delay + diff)
        prev_time = curr_time

    pygame.quit()
    quit()
