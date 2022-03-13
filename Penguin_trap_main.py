import pygame
from Penguin import *
from time import sleep
pygame.font.init()

width, height = 1536, 800
center_x, center_y = 680, 350
mouse_center_x, mouse_center_y = 742, 415
step_x, step_y = 88, 50
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("DON`T LET PENGUIN FALL!!!")
fps = 60
ice1 = pygame.image.load("images/hexagon_1.png")
ice2 = pygame.image.load("images/hexagon_2.png")
ice3 = pygame.image.load("images/hexagon_3.png")
leha = pygame.image.load("images/penguin.png")
leha2 = pygame.image.load("images/penguin_fall.jpg")
f1 = pygame.font.SysFont("serif", 80)
text = f1.render("YOU LOSE!", True, (180, 0, 0))


def to_coordinate(h: Ice) -> tuple:
    return center_x + (h.y - h.x)*step_x, center_y + (2*h.z - h.x - h.y)*step_y


def to_mouse_coord(h: Ice) -> tuple:
    return mouse_center_x + (h.y - h.x) * step_x, mouse_center_y + (2 * h.z - h.x - h.y) * step_y


def dist(t1: tuple, t2: tuple) -> float:
    return (t1[0] - t2[0]) ** 2 + (t1[1] - t2[1]) ** 2


def closest(t: tuple) -> tuple:
    m = 100000000
    ans: tuple = ()
    for t0 in Click_to_ice.keys():
        if dist(t, t0) < m:
            m = dist(t, t0)
            ans = t0
    if not ans:
        raise CustomError("There are no hexagons!")
    return ans


def draw_window():
    win.fill((255, 228, 225))
    for c in Field:
        win.blit(ice1, to_coordinate(c))
    for c in All - Field:
        win.blit(ice3, to_coordinate(c))
    win.blit(leha, (center_x + 23, center_y + 23))
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                t = closest(pygame.mouse.get_pos())
                h = Click_to_ice[t]
                Field.remove(h)
                All.remove(h)
                del Click_to_ice[t]
                win.blit(ice2, to_coordinate(h))
                pygame.display.update()
                sleep(0.5)
                set_h = {Ice(0, 0, 0)}
                fall: Set[Ice] = set()
                while set_h:
                    set_h = set()
                    for a in Field:
                        inter = (len(a.nx & All), len(a.ny & All), len(a.nz & All))
                        if 2 not in inter and inter != (1, 1, 1):
                            set_h.add(a)
                    Field.difference_update(set_h)
                    All.difference_update(set_h)
                    fall.update(set_h)
                    for c in fall:
                        win.blit(ice2, to_coordinate(c))
                    pygame.display.update()
                    sleep(0.3)
                for c in fall:
                    del Click_to_ice[to_mouse_coord(c)]
                if Ice(0, 0, 0) not in Field:
                    win.fill((255, 228, 225))
                    for c in Field:
                        win.blit(ice1, to_coordinate(c))
                    for c in All - Field:
                        win.blit(ice3, to_coordinate(c))
                    win.blit(leha2, (center_x - 25, center_y - 25))
                    win.blit(text, (width // 2 - 200, height // 2 - 200))
                    pygame.display.update()
                    sleep(2.5)
                    run = False
        draw_window()
    pygame.quit()


Click_to_ice = {to_mouse_coord(h): h for h in Field}
main()
