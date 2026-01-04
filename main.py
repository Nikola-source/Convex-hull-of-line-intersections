import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 180, 0)
PURPLE = (180, 0, 180)
ORANGE = (255, 165, 0)

ORIGIN_X = WIDTH // 2
ORIGIN_Y = HEIGHT // 2
SCALE = 40
GRID_SIZE = 20

points = []
draw_lines = []
lines = []
critical_points = []
draw_critical_points_arr = []
poligon = []
draw_poligon_arr = []
temp_point = None
crtanje = True
button_rect = pygame.Rect(100, 700, 150, 50)
alghorithm_button = pygame.Rect(100, 700, 150, 50)
index_points = 0
index_poligon = 0

font = pygame.font.SysFont('Arial', 16)
large_font = pygame.font.SysFont('Arial', 24, bold=True)

def draw_grid():
    for x in range(ORIGIN_X, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT), 1)
    for x in range(ORIGIN_X, 0, -GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT), 1)

    for y in range(ORIGIN_Y, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y), 1)
    for y in range(ORIGIN_Y, 0, -GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y), 1)

def draw_axes():
    pygame.draw.line(screen, RED, (0, ORIGIN_Y), (WIDTH, ORIGIN_Y), 2)
    pygame.draw.line(screen, BLUE, (ORIGIN_X, 0), (ORIGIN_X, HEIGHT), 2)

    x_text = font.render("X", True, RED)
    y_text = font.render("Y", True, BLUE)
    screen.blit(x_text, (WIDTH - 20, ORIGIN_Y - 20))
    screen.blit(y_text, (ORIGIN_X + 10, 10))

def draw_points():
    for i, (x, y) in enumerate(points):
        pygame.draw.circle(screen, GREEN, (x, y), 8)
        pygame.draw.circle(screen, BLACK, (x, y), 8, 2)

        math_x = (x - ORIGIN_X) / SCALE
        math_y = -(y - ORIGIN_Y) / SCALE
        coord_text = font.render(f"({math_x:.1f}, {math_y:.1f})", True, BLACK)

        text_x = x + 15
        text_y = y - 20

        if text_x + coord_text.get_width() > WIDTH:
            text_x = x - coord_text.get_width() - 15
        if text_y < 10:
            text_y = y + 10

        screen.blit(coord_text, (text_x, text_y))

def draw_all_lines_from_equations():
    for line in draw_lines:

        if line[1] is None:
            x = line[0]
            draw_vertical_line(x)
        else:
            k, n = line
            draw_line_kn(k,n)

def draw_line_kn(k, n):
    x1 = 0
    y1 = k * x1 + n

    x2 = WIDTH
    y2 = k * x2 + n

    pygame.draw.line(screen, BLACK, (x1, y1), (x2, y2), 2)

def draw_vertical_line(x):
    h = HEIGHT
    pygame.draw.line(screen, BLACK, (x, 0), (x, h), 2)

def draw_button():
    mouse_pos = pygame.mouse.get_pos()
    if len(draw_lines) <=1:
        color = GRAY
        text_color = BLACK
    elif button_rect.collidepoint(mouse_pos):
        color = GREEN
        text_color = WHITE
    else:
        color = BLUE
        text_color = WHITE
    pygame.draw.rect(screen, color, button_rect, border_radius=15)
    pygame.draw.rect(screen, BLACK, button_rect, 3, border_radius=15)

    text = font.render("zapocni algoritam", True, text_color)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def draw_algorithm_button():
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        color = GREEN
        text_color = WHITE
    else:
        color = BLUE
        text_color = WHITE

    pygame.draw.rect(screen, color, alghorithm_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, alghorithm_button, 3, border_radius=15)

    text = font.render("sledeci korak", True, text_color)
    text_rect = text.get_rect(center=alghorithm_button.center)
    screen.blit(text, text_rect)

def handle_button_click():
    global crtanje,index_poligon,index_points

    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos) and len(draw_lines)>=2:
        if crtanje:
            index_points = 0
            index_poligon = 0
            crtanje = False
            return True
    return False

def presek(line1,line2):
    (k1,n1) = line1
    (k2,n2) = line2

    if k1 is None and k2 is None:
        return None

    if n1 is None:
        x = k1
        y = k2 * x + n2
        return (x, y)

    if n2 is None:
        x = k2
        y = k1 * x + n1
        return (x, y)

    x = (n2 - n1) / (k1 - k2)
    y = k1 * x + n1

    return (x, y)

def sortiraj_po_uglu_sa_x_osom(prave):

    def ugao_za_sortiranje(prava):
        if prava[1] is None:
            return 90.0

        k = prava[0]

        if k == 0:
            return 0.0

        ugao = math.degrees(math.atan(abs(k)))

        if k > 0:
            return ugao
        else:
            return 180.0 - ugao

    return sorted(prave, key=ugao_za_sortiranje)

def find_critical_points():
    global lines, critical_points
    lines = sortiraj_po_uglu_sa_x_osom(lines)
    for i in range(len(lines) - 1):
        tacka = presek(lines[i], lines[i + 1])
        critical_points.append(tacka)
    critical_points.append(presek(lines[0], lines[len(lines) - 1]))

def handle_algh_button_click():
    global critical_points,draw_critical_points_arr,index_points,draw_poligon_arr,index_poligon
    mouse_pos = pygame.mouse.get_pos()
    if alghorithm_button.collidepoint(mouse_pos):
        if index_points < len(critical_points):
            draw_critical_points_arr.append(critical_points[index_points])
            index_points += 1
        elif len(critical_points) == index_points and index_poligon < len(poligon):
            start = poligon[index_poligon]
            end = poligon[(index_poligon + 1) % len(poligon)]
            draw_poligon_arr.append((start, end))
            index_poligon += 1
        return

def draw_critical_points():
    for i, (x, y) in enumerate(draw_critical_points_arr):
        dx = ORIGIN_X + x * SCALE
        dy = HEIGHT / 2 - y * SCALE
        color = RED
        if dx > WIDTH:
            dx = WIDTH
            color = BLUE
        if dx < 0:
            dx = 0
            color = BLUE
        if dy > HEIGHT:
            dy = HEIGHT
            color = BLUE
        if dy < 0:
            dy = 0
            color = BLUE
        pygame.draw.circle(screen, color, (dx, dy), 8)
        pygame.draw.circle(screen, BLACK, (dx, dy), 8, 2)

def find_pivot():
    global critical_points
    pivot = critical_points[0]
    for p in critical_points[1:]:
        if p[1] == pivot[1]:
            if p[0] < pivot[0]:
                pivot = p
        elif p[1] < pivot[1]:
            pivot = p

    return pivot

def distance_sq(p1, p2):
    return (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2

def rotacija(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def graham():
    global critical_points, poligon
    if len(critical_points) <= 3:
        poligon = critical_points.copy()
        return
    pivot = find_pivot()

    def angle_comparison(p):
        angle = math.atan2(p[1] - pivot[1], p[0] - pivot[0])
        if angle < 0:
            angle += 2 * math.pi
        return angle, distance_sq(pivot, p)

    sorted_points = sorted([p for p in critical_points if not (p[0] == pivot[0] and p[1] == pivot[1])], key=angle_comparison)
    poligon = [pivot]

    for point in sorted_points:
        while len(poligon)>=2 and rotacija(poligon[-2],poligon[-1],point) <0:
            poligon.pop()
        poligon.append(point)

def draw_poligon():
    global draw_poligon_arr

    for start, end in draw_poligon_arr:
        x1 = start[0] * SCALE + ORIGIN_X
        y1 = HEIGHT / 2 - start[1] * SCALE
        x2 = end[0] * SCALE + ORIGIN_X
        y2 = HEIGHT / 2 - end[1] * SCALE
        pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 5)


clock = pygame.time.Clock()
running = True
mode = "add_point"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r and crtanje:
                draw_lines.clear()
                lines.clear()
                points.clear()
                poligon.clear()
                draw_poligon_arr.clear()
                draw_critical_points_arr.clear()
                mode = "add_point"
            if event.key == pygame.K_SPACE and not crtanje:
                draw_poligon_arr.clear()
                draw_critical_points_arr.clear()
                poligon.clear()
                critical_points.clear()
                crtanje = 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and crtanje:
                mouse_pos = event.pos
                if not button_rect.collidepoint(mouse_pos):
                    if mode == "add_point":
                        points.append(mouse_pos)
                        mode = "draw_line"
                        temp_point = mouse_pos
                    elif mode == "draw_line":
                        p2 = mouse_pos
                        x2 = (p2[0]-ORIGIN_X)/SCALE
                        y2 = (HEIGHT/2 - p2[1]) / SCALE
                        p1 = points.pop(0)
                        x1 = (p1[0] - ORIGIN_X) / SCALE
                        y1 = (HEIGHT/2 - p1[1]) / SCALE
                        if x1-x2 == 0:
                            draw_lines.append((p1[0], None))
                            lines.append((x1, None))
                        else:
                            dk=(p2[1]-p1[1])/(p2[0]-p1[0])
                            dn = p1[1] - dk*p1[0]
                            draw_lines.append((dk, dn))
                            k = (y2-y1)/(x2-x1)
                            n = y1 - k*x1
                            lines.append((k, n))
                        mode = "add_point"
                if handle_button_click():
                    find_critical_points()
                    graham()
            elif event.button == 1 and not crtanje:
                handle_algh_button_click()

    screen.fill(WHITE)
    draw_grid()
    draw_axes()
    draw_points()
    draw_all_lines_from_equations()
    if crtanje : draw_button()
    else:
        draw_algorithm_button()
        draw_critical_points()
        draw_poligon()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()