import pygame
import sys
import math

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600

# Colores
white = (255, 255, 255)
black = (0, 0, 0)

# Crear la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Triángulo Móvil")

# Triángulo
triangle_size = 30
triangle_x = screen_width // 2
triangle_y = screen_height // 2
triangle_speed = 0  # Aceleración inicial
triangle_max_speed = 5  # Máxima aceleración
triangle_angle = 0

# Lista de balas
bullets = []

# Disparo
bullet_speed = 10  # Velocidad de la bala
bullet_radius = 5

def draw_triangle(x, y, angle):
    # Definir los vértices del triángulo
    p1 = (x, y - triangle_size // 2)
    p2 = (x - triangle_size // 2, y + triangle_size // 2)
    p3 = (x + triangle_size // 2, y + triangle_size // 2)

    # Rotar los vértices
    angle_rad = math.radians(angle)
    p1 = (
        x + (p1[0] - x) * math.cos(angle_rad) - (p1[1] - y) * math.sin(angle_rad),
        y + (p1[0] - x) * math.sin(angle_rad) + (p1[1] - y) * math.cos(angle_rad)
    )
    p2 = (
        x + (p2[0] - x) * math.cos(angle_rad) - (p2[1] - y) * math.sin(angle_rad),
        y + (p2[0] - x) * math.sin(angle_rad) + (p2[1] - y) * math.cos(angle_rad)
    )
    p3 = (
        x + (p3[0] - x) * math.cos(angle_rad) - (p3[1] - y) * math.sin(angle_rad),
        y + (p3[0] - x) * math.sin(angle_rad) + (p3[1] - y) * math.cos(angle_rad)
    )

    pygame.draw.polygon(screen, white, [p1, p2, p3])

def draw_bullet(x, y):
    pygame.draw.circle(screen, white, (int(x), int(y)), bullet_radius)

# Bucle principal
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    # Control de movimiento y rotación
    if keys[pygame.K_UP]:
        # Aumentar gradualmente la aceleración
        if triangle_speed < triangle_max_speed:
            triangle_speed += 0.1
    if keys[pygame.K_DOWN]:
        # Disminuir gradualmente la aceleración
        if triangle_speed > 0:
            triangle_speed -= 0.1
    if keys[pygame.K_LEFT]:
        triangle_angle -= 5
    if keys[pygame.K_RIGHT]:
        triangle_angle += 5

    # Calcular la aceleración en función del ángulo girado 90 grados a la izquierda
    acceleration_angle = triangle_angle - 90
    acceleration_x = math.cos(math.radians(acceleration_angle)) * triangle_speed
    acceleration_y = math.sin(math.radians(acceleration_angle)) * triangle_speed
    triangle_x += acceleration_x
    triangle_y += acceleration_y

    # Reaparecer en el otro lado de la pantalla
    if triangle_x > screen_width:
        triangle_x = 0
    elif triangle_x < 0:
        triangle_x = screen_width
    if triangle_y > screen_height:
        triangle_y = 0
    elif triangle_y < 0:
        triangle_y = screen_height

    # Disparo
    if keys[pygame.K_SPACE]:
        bullet_x = triangle_x  # Iniciar la bala desde la posición del triángulo
        bullet_y = triangle_y
        bullet_direction = acceleration_angle  # Usar la dirección de la aceleración al disparar
        bullets.append((bullet_x, bullet_y, bullet_direction))

    # Actualizar la dirección de las balas
    for bullet in bullets:
        bullet_x, bullet_y, bullet_direction = bullet
        bullet_x += math.cos(math.radians(bullet_direction)) * bullet_speed
        bullet_y += math.sin(math.radians(bullet_direction)) * bullet_speed
        bullet = (bullet_x, bullet_y, bullet_direction)

    # Eliminar balas que salgan de la pantalla
    bullets = [(x, y, direction) for x, y, direction in bullets if 0 <= x < screen_width and 0 <= y < screen_height]

    screen.fill(black)
    draw_triangle(triangle_x, triangle_y, triangle_angle)
    
    # Dibujar y actualizar las balas
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1])
    
    pygame.display.flip()
    clock.tick(60)
