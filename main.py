import pygame
import random
import sys
import math

pygame.init()


#screen set up
WIDTH = 1500
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boid Simulation")
icon = pygame.image.load('boid.png')
pygame.display.set_icon(icon)

#clock
clock = pygame.time.Clock()
FPS = 120


def main():
    max_velocity = 7
    min_distance = 20


    class Boid():


        def __init__(self, x, y, r, dx, dy, perception, color):
            self.x = x
            self.y = y
            self.r = r
            self.dx = dx
            self.dy = dy
            self.perception = perception
            self.color = color


        def draw_to_screen(self):
            thetaA = math.atan(self.dy / self.dx)

            if self.dx > 0 and self.dy > 0:
                thetaA = thetaA
                thetaB = thetaA + math.pi*5/6
                thetaC = thetaA + math.pi*7/6
                if thetaB > math.pi * 2:
                    thetaB -= 2*math.pi
                if thetaC > math.pi * 2:
                    thetaC -= 2*math.pi
            elif self.dx < 0 and self.dy > 0:
                thetaA = math.pi + thetaA
                thetaB = thetaA + math.pi*5/6
                thetaC = thetaA + math.pi*7/6
                if thetaB > math.pi * 2:
                    thetaB -= 2*math.pi
                if thetaC > math.pi * 2:
                    thetaC -= 2*math.pi
            elif self.dx < 0 and self.dy < 0:
                thetaA = math.pi + thetaA
                thetaB = thetaA + math.pi*5/6
                thetaC = thetaA + math.pi*7/6
                if thetaB > math.pi * 2:
                    thetaB -= 2*math.pi
                if thetaC > math.pi * 2:
                    thetaC -= 2*math.pi
            elif self.dx > 0 and self.dy < 0:
                thetaA = 2*math.pi + thetaA
                thetaB = thetaA + math.pi*5/6
                thetaC = thetaA + math.pi*7/6
                if thetaB > math.pi * 2:
                    thetaB -= 2*math.pi
                if thetaC > math.pi * 2:
                    thetaC -= 2*math.pi
            
            a = (self.x + math.cos(thetaA)*self.r, self.y + math.sin(thetaA)*self.r)
            b = (self.x + math.cos(thetaB)*self.r, self.y + math.sin(thetaB)*self.r)
            c = (self.x + math.cos(thetaC)*self.r, self.y + math.sin(thetaC)*self.r)
            pygame.draw.polygon(screen, self.color, [a, b, c])


        def alignment(self, boids):
            sumdx = 0
            sumdy = 0
            avgdx = 0
            avgdy = 0
            boids_in_range = 0
            for boid in boids:
                distance = math.sqrt(pow(self.x - boid.x, 2) + pow(self.y - boid.y, 2))
                if distance < self.perception and boid != self:
                    sumdx += boid.dx
                    sumdy += boid.dy
                    boids_in_range += 1
            if boids_in_range > 0:
                avgdx = (sumdx / boids_in_range) - self.dx
                avgdy = (sumdy / boids_in_range) - self.dy
            self.dx += (avgdx / 10)
            self.dy += (avgdy / 10)


        def cohesion(self, boids):
            sumx = 0
            sumy = 0
            avgx = 0
            avgy = 0
            boids_in_range = 0
            for boid in boids:
                distance = math.sqrt(pow(self.x - boid.x, 2) + pow(self.y - boid.y, 2))
                if distance < self.perception and boid != self:
                    sumx += (self.x - boid.x)
                    sumy += (self.y - boid.y)
                    boids_in_range += 1
            if boids_in_range > 0:
                avgx = (sumx / boids_in_range)
                avgy = (sumy / boids_in_range)

            self.dx -= (avgx / 100)
            self.dy -= (avgy / 100)


        def seperation(self, boids):
            boids_in_range = 0

            for boid in boids:
                distance = math.sqrt(pow(self.x - boid.x, 2) + pow(self.y - boid.y, 2))
                if distance < min_distance:
                    boids_in_range += 1
                    distx = (self.x - boid.x)
                    disty = (self.y - boid.y)

                    if distx > 0:
                        self.dx += 1
                    elif distx < 0:
                        self.dx -= 1
                    
                    if disty > 0:
                        self.dy += 1
                    elif disty < 0:
                        self.dy -= 1


        def move(self):
            if abs(self.dx) > max_velocity or abs(self.dy) > max_velocity:
                scale = max_velocity / max(abs(self.dx), abs(self.dy))
                self.dx *= scale
                self.dy *= scale
            
            self.x += self.dx
            self.y += self.dy


        def explenation(self, boids):
            # transparent observing circle
            surf1 = pygame.Surface((self.x + self.perception, self.y + self.perception), pygame.SRCALPHA)
            alpha_surf1 = pygame.Surface(surf1.get_size(), pygame.SRCALPHA)
            alpha_surf1.fill((0, 0, 0, 100))
            rect1 = surf1.get_rect()
            pygame.draw.circle(surf1, (0, 0, 0, 50), (int(self.x), int(self.y)), self.perception)
            screen.blit(surf1, rect1)
            # change color of observed
            self.color = (255, 0, 0)
            # transparent minimum circle
            surf2 = pygame.Surface((self.x + min_distance, self.y + min_distance), pygame.SRCALPHA)
            alpha_surf2 = pygame.Surface(surf2.get_size(), pygame.SRCALPHA)
            alpha_surf2.fill((0, 0, 0, 100))
            rect2 = surf1.get_rect()
            pygame.draw.circle(surf1, (0, 0, 0, 100), (int(self.x), int(self.y)), min_distance)
            screen.blit(surf1, rect2)
            # add in range lines
            boisd_in_range = 0
            for boid in boids:
                distance = math.sqrt(pow(self.x - boid.x, 2) + pow(self.y - boid.y, 2))
                if distance < min_distance and boid != self:
                    pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (boid.x, boid.y))


    boids = []
    amount_boids = 100

    for i in range(amount_boids):
        r = 8
        x = random.randrange(r, WIDTH - r)
        y = random.randrange(r, HEIGHT - r)
        angle = random.uniform(0, 2 * math.pi)
        dx = max_velocity * math.cos(angle)
        dy = max_velocity * math.sin(angle)
        perception = 70
        color = (0, 0, 0)
        boids.append(Boid(x, y, r, dx, dy, perception, color))     

    
    def update():
        screen.fill((255, 255, 255))

    running = True
    while running:
        clock.tick(FPS)
        update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    sys.exit()

        #boid movement and drawing
        for i in range(amount_boids):

            boids[i].draw_to_screen()

            boids[i].alignment(boids)
            boids[i].cohesion(boids)
            boids[i].seperation(boids)

            boids[i].move()

            #boundaries
            if boids[i].x < 0:
                boids[i].x = WIDTH
            elif boids[i].x > WIDTH:
                boids[i].x = 0
            if boids[i].y < 0:
                boids[i].y = HEIGHT
            elif boids[i].y > HEIGHT:
                boids[i].y = 0
            
        boids[1].explenation(boids)

        pygame.display.update()
    
main()