import sys, pygame, random, math, time
pygame.init()

size = width, height = 800,800
black = 0, 0, 0

dots = []

def convertToRadian(num):
    return num / 57.2958

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, size):
        self.size = size
        self.speed = [1,1]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("asteroid.png")
        self.rect = self.image.get_rect()

        self.centerX = self.rect[0] + self.rect.width / 2
        self.centerY = self.rect[1] + self.rect.height / 2

        self.rect[0] = random.randint(0,width - self.rect.width)
        self.rect[1] = random.randint(0,height - self.rect.height)
    def update(self):
        self.centerX = self.rect[0] + self.rect.width / 2
        self.centerY = self.rect[1] + self.rect.height / 2
        
        if self.rect[0] < 0 or self.rect[0] > width - self.rect.width:
            self.speed[0] = -self.speed[0]
            pygame.mixer.Sound.play(collision_sound)
        if self.rect[1] < 0 or self.rect[1] > height - self.rect.height:
            self.speed[1] = -self.speed[1]
            pygame.mixer.Sound.play(collision_sound)

        self.rect = self.rect.move(self.speed)

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ship.png")
        self.rect = self.image.get_rect()
        self.rect[0] = width / 2 - self.rect.width / 2
        self.rect[1] = height / 2 - self.rect.height / 2
        self.move = 0
        self.speed = 0
        self.rotationSpeed = 0
        self.rotate = 0
        self.angle = 90
        self.centerX = self.rect[0] + self.rect.width / 2
        self.centerY = self.rect[1] + self.rect.height / 2
    def update(self):
        self.centerX = self.rect[0] + self.rect.width / 2
        self.centerY = self.rect[1] + self.rect.height / 2

        print(f"angle: {self.angle} rotationSpeed: {self.rotationSpeed}")
        self.rect = self.rect.move(int(math.cos(convertToRadian(self.angle)) * self.speed),-int(math.sin(convertToRadian(self.angle)) * self.speed))

        if self.rotate == 1 and self.rotationSpeed < 20:
            self.rotationSpeed += 0.1
        elif self.rotationSpeed > 0:
            self.rotationSpeed -= 0.1
        if self.rotate == -1 and self.rotationSpeed > -20:
            self.rotationSpeed -= 0.1
        elif self.rotationSpeed < 0:
            self.rotationSpeed += 0.1

        if self.rotationSpeed < 0.1 and self.rotationSpeed > -0.1:
            self.rotationSpeed = 0

        if self.move == 1 and self.speed < 20:
            self.speed += 0.1
        elif self.speed > 0:
            self.speed -= 0.1

        self.angle += self.rotationSpeed
        if self.angle > 360:
            self.angle -= 360
        if self.angle < -360:
            self.angle += 360

        dots.append((self.rect[0] + self.rect.width / 2, self.rect[1] + self.rect.height / 2))


screen = pygame.display.set_mode(size)
pygame.display.set_caption("ASTEROIDS")

collision_sound = pygame.mixer.Sound("collision.wav")

asteroids = pygame.sprite.Group(Asteroid(3),Asteroid(3),Asteroid(3))
ship = Ship()
shipGroup = pygame.sprite.Group(ship)

#not working
def checkCollision(asteroids, ship):
    for asteroid in asteroids:
        if abs(math.tan((ship.centerY - asteroid.centerY) / (ship.centerX - asteroid.centerX))) < ship.rect.width / 2 + asteroid.rect.width / 2:
            print("GAME OVER")
            time.sleep(100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ship.move = 1
            if event.key == pygame.K_LEFT:
                ship.rotate = 1
            if event.key == pygame.K_RIGHT:
                ship.rotate = -1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                ship.move = -1
            if event.key == pygame.K_LEFT:
                ship.rotate = 0
            if event.key == pygame.K_RIGHT:
                ship.rotate = 0

    screen.fill(black)

    if len(dots) > 100:
        dots.pop(0)
    for dot in dots:
        screen.fill((255,255,255), (dot, (1, 1)))
    
    asteroids.update()
    asteroids.draw(screen)

    shipGroup.update()
    shipGroup.draw(screen)
    lineLength = 25
    pygame.draw.line(screen,(255,255,255), (ship.centerX, ship.centerY), (ship.centerX + math.cos(convertToRadian(ship.angle)) * lineLength, ship.centerY + math.sin(convertToRadian(ship.angle)) * lineLength))

    pygame.display.flip()

    time.sleep(0.01)

    #not working: checkCollision(asteroids, ship)