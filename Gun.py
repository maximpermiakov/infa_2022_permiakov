from random import choice
from random import randint
import pygame
import math

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
ORANGE = (255, 128, 0)
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

v = 10  # скорости объектов
v_2 = 30


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """Конструктор класса ball
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        r - радиус мяча
        color - цвет мяча
        vx - начальная скорость мяча по горизонтали
        vy - начальная скорость мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = RED

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки.
        То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy,
        силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= 2
        self.x += self.vx*dt
        self.y -= self.vy*dt
        if self.y+self.r >= HEIGHT:
            self.vx = self.vx/2
            self.vy = -self.vy/2
        if self.y-self.r <= 0:
            self.vy = -self.vy
        if self.x-self.r <= 0 or self.x+self.r >= WIDTH:
            self.vx = -self.vx

    def draw(self):
        """Рисует шарик"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет, сталкивается ли данный объект с целью,
        описываемой в объекте obj.
        Args:
            obj: Объект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели.
            В противном случае возвращает False.
        """
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5 <= self.r + obj.r:
            return True
        return False


class Gun:
    def __init__(self, screen):
        """Конструктор класса gun
        Args:
        x - начальное положение пушки по горизонтали
        y - начальное положение пушки по вертикали
        """
        self.x = 20
        self.y = 450
        self.screen = screen
        self.f2_power = 10
        self.f2_on = False
        self.an = 0
        self.color = BLACK

    def fire2_start(self):
        self.f2_on = True

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2(event.pos[1]-new_ball.y, event.pos[0]-new_ball.x)
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Рисует пушку"""
        pygame.draw.polygon(
            self.screen,
            self.color,
            [[self.x, self.y], [self.x - 8 * math.sin(self.an), self.y + 8 * math.cos(self.an)],
             [self.x - 8 * math.sin(self.an) + max(self.f2_power, 20) * math.cos(self.an),
              self.y + 8 * math.cos(self.an) + max(self.f2_power, 20) * math.sin(self.an)],
             [self.x + max(self.f2_power, 20) * math.cos(self.an),
              self.y + max(self.f2_power, 20) * math.sin(self.an)]])

    def power_up(self):
        """Увеличивает силу выстрела до максимального значения"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        """Конструктор класса target
        Args:
        live - количество жизней у цели
        """
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """Инициализация новой цели"""
        self.r = randint(2, 50)
        self.x = randint(0, WIDTH-self.r)
        self.y = randint(0, HEIGHT-self.r)
        self.vx = randint(-v, v)
        self.vy = randint(-v, v)
        self.live = 1
        self.color = choice(GAME_COLORS)

    def hit(self, points=1):
        """Попадание шарика в цель"""
        self.points += points

    def draw(self):
        """Рисует цель"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def move(self):
        """Переместить цель по прошествии единицы времени.
        Метод описывает перемещение цели за один кадр перерисовки.
        То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy,
        с учетом стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx*dt
        self.y += self.vy*dt
        if self.y+self.r >= HEIGHT or self.y-self.r <= 0:
            self.vy = -self.vy
        if self.x-self.r <= 0 or self.x+self.r >= WIDTH:
            self.vx = -self.vx


class Target2(Target):
    def move(self):
        """Переместить необычную цель по прошествии единицы времени.
        Метод описывает перемещение странной цели за один кадр перерисовки.
        То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy,
        с учетом стен по краям окна (размер окна 800х600),
        каждый кадр изменяет скорость мяча
        """
        self.vx = randint(-v_2, v_2)
        self.vy = randint(-v_2, v_2)
        if (self.y + self.r >= HEIGHT and self.vy >= 0) or (self.y - self.r <= 0 and self.vy <= 0):
            self.vy = -self.vy
        if (self.x - self.r <= 0 and self.vx <= 0) or (self.x + self.r >= WIDTH and self.vx >= 0):
            self.vx = -self.vx
        self.x += self.vx*dt
        self.y += self.vy*dt

    def draw(self):
        """Рисует необычный шарик"""
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r
        )

    def hit(self, points=5):
        """Попадание шарика в цель"""
        self.points += points


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
target2 = Target2(screen)
targets = [target, target2]
quit = False
f = pygame.font.Font(None, 24)

while not quit:
    dt = clock.tick(FPS)/FPS
    screen.fill(WHITE)
    for elem in targets:
        elem.draw()
        elem.move()
    gun.draw()
    for b in balls:
        b.draw()
    text1 = 'Score ' + str(target.points + target2.points)
    text2 = 'Bullets ' + str(bullet)
    screen.blit(f.render(text1, True, BLACK), (10, 10))
    screen.blit(f.render(text2, True, BLACK), (10, 30))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        for elem in targets:
            if b.hittest(elem) and elem.live:
                elem.hit()
                elem.new_target()
    gun.power_up()
pygame.quit()
