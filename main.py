import time
import pygame
import numpy as np

COLOR_B = (0, 0, 0)
COLOR_G = (40, 40, 40)
COLOR_D = (0, 0, 0)
COLOR_A = (255, 117, 20)

steps = 10


def interpolate_color(color1, color2, t):
    r = int(color1[0] * (1 - t) + color2[0] * t)
    g = int(color1[1] * (1 - t) + color2[1] * t)
    b = int(color1[2] * (1 - t) + color2[2] * t)
    return r, g, b


def gradient_color(color1, color2, steps):
    gradient = []
    for i in range(steps):
        t = i / (steps - 1)
        interpolated_color = interpolate_color(color1, color2, t)
        gradient.append(interpolated_color)
    return gradient


def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    gradient = gradient_color(COLOR_D, COLOR_A, steps)
    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2])-cells[row, col]
        color = COLOR_B if cells[row, col] == 0 else gradient
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = gradient
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = gradient
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = gradient
        if cells[row, col] == 0:
            color_index = min(int(alive), steps - 1)
            color = gradient[color_index]
        else:
            color = gradient[-1]
        pygame.draw.rect(screen, color, (col*size, row*size, size-1, size-1))
    return updated_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60, 80))

    screen.fill(COLOR_G)

    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                elif event.key == pygame.K_ESCAPE:
                    update(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1]//10, pos[0]//10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_G)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)


if __name__ == '__main__':
    main()
