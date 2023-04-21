#importing pygame library to my project
import pygame, sys
from pygame.locals import QUIT
import math
import random


class Object:
    #constructor class
    def __init__(self, position, velocity, acceleration, radius, color,simulator):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.radius = radius
        self.color = color
        self.simulator = simulator

    def gravity(self):
        #adds acceleration to y component of velocity
        self.velocity[1] += self.acceleration

    def update(self):
        # update x component of velocity
        self.position[0] += self.velocity[0]
        #update y component of velocity
        self.position[1] += self.velocity[1]

    #bounce method accepts two parametrs screen width and height
    def bounce(self, screen_width, screen_height):
        #checks over all instances apart from the object which this method belongs to
        for other in self.simulator.particles:
            if other != self:
                #it then calls the collide function with the other object
                self.collide(other)
        #checks if the sphere is overlapping with border
        if self.position[0] - self.radius < 0:
            # sets the velocity in the other direction and  multiplys by bounce damping
            self.velocity[0] = abs(self.velocity[0]) * Simulator.bounce_damping
            #sets position so it is just on the edge and not over the edge
            self.position[0] = self.radius

        #repeats 4 times for 4 differant walls varying slightly
        elif self.position[0] + self.radius > screen_width:
            self.velocity[0] = -abs(
                self.velocity[0]) * self.simulator.bounce_damping
            self.position[0] = screen_width - self.radius

        if self.position[1] - self.radius < 0:
            self.velocity[1] = abs(self.velocity[1]) * self.simulator.bounce_damping
            self.position[1] = self.radius

        elif self.position[1] + self.radius > screen_height:
            self.velocity[1] = -abs(
                self.velocity[1]) * self.simulator.bounce_damping
            self.position[1] = screen_height - self.radius

    def collide(self, other):
        dx = other.position[0] - self.position[0]
        dy = other.position[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance < self.radius + other.radius:

            # Objects are colliding, adjust position
            overlap = (self.radius + other.radius - distance) / 2
            angle = math.atan2(dy, dx)

            self.position[0] -= overlap * math.cos(angle)
            self.position[1] -= overlap * math.sin(angle)
            other.position[0] += overlap * math.cos(angle)
            other.position[1] += overlap * math.sin(angle)

            # Calculate final velocities using elastic collision formula
            # note this is the result of solving multiple equations and reducing it to its simplist form
            v1f_x = ((self.velocity[0] * (self.radius - other.radius)) +
                     (2 * other.radius * other.velocity[0])) / (self.radius +
                                                                other.radius)
            v1f_y = ((self.velocity[1] * (self.radius - other.radius)) +
                     (2 * other.radius * other.velocity[1])) / (self.radius +
                                                                other.radius)
            v2f_x = ((other.velocity[0] * (other.radius - self.radius)) +
                     (2 * self.radius * self.velocity[0])) / (self.radius +
                                                              other.radius)
            v2f_y = ((other.velocity[1] * (other.radius - self.radius)) +
                     (2 * self.radius * self.velocity[1])) / (self.radius +
                                                              other.radius)

            # Update velocities of colliding objects
            self.velocity[0] = v1f_x
            self.velocity[1] = v1f_y
            other.velocity[0] = v2f_x
            other.velocity[1] = v2f_y


class Simulator:

    def __init__(self, acceleration):

        pygame.init()
        pygame.font.init()

        self.screen_width = 1000
        self.screen_height = 600
        self.acceleration = acceleration
        self.particles = []
        self.font = pygame.font.SysFont(None, 24)
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.velocity = 10
        self.angle = 45
        self.mouse_pos = [200, self.screen_height - 200]
        self.border = 300
        self.bounce_damping = 0.8
        self.constant = 0.1

        #setting a caption for the window
        pygame.display.set_caption('Simulator')

    def drawGui(self):
        #labels white line
        text_surface = self.font.render(str(int(self.velocity)), True,
                                        (255, 255, 255))
        #displaying text surface to screen
        self.screen.blit(text_surface,
                         (self.mouse_pos[0] + 20, self.mouse_pos[1] + 20))

        #labels angle
        text_surface = self.font.render(str(int(self.angle * (180 / 3.14159))),
                                        True, (255, 255, 255))
        self.screen.blit(text_surface, (20, self.screen_height - 20))

        #draws a white line resultant component of velocity
        pygame.draw.line(self.screen, (255, 255, 255), (0, self.screen_height),
                         (self.mouse_pos[0], self.mouse_pos[1]), 3)

        #draws a red line x component of velocity
        pygame.draw.line(self.screen, (255, 0, 0), (0, self.screen_height),
                         (self.mouse_pos[0], self.screen_height), 3)

        #labels red line with x component of velocity
        text_surface = self.font.render(
            str(int(self.velocity * math.cos(self.angle))), True, (255, 0, 0))
        self.screen.blit(text_surface,
                         (self.mouse_pos[0] // 2, self.screen_height - 24))

        #draws a blue line y component of velocity
        pygame.draw.line(self.screen, (0, 0, 255),
                         (self.mouse_pos[0], self.screen_height),
                         (self.mouse_pos[0], self.mouse_pos[1]), 3)

        #labels a blue line with y component of velocit
        text_surface = self.font.render(
            str(int(self.velocity * math.sin(self.angle))), True, (0, 0, 255))
        self.screen.blit(text_surface,
                         (self.mouse_pos[0] + 12, self.screen_height -
                          (self.screen_height - self.mouse_pos[1]) // 2))

        #draws an arc between circle and projection line
        pygame.draw.arc(self.screen, (255, 255, 255),
                        [-50, self.screen_height - 50, 100, 100], 0,
                        self.angle, 3)

    def run(self):
        while True:

            self.clock.tick(30)

            ## returns a array with mouse x and y position
            mouse = list(pygame.mouse.get_pos())

            if math.sqrt(mouse[0]**2 +
                         (self.screen_height - mouse[1])**2) < self.border:
                self.mouse_pos = mouse
                self.angle = math.atan(
                    (self.screen_height - self.mouse_pos[1]) /
                    self.mouse_pos[0])

            # validity
            if self.mouse_pos[0] != None:
                #calculating angle
                if self.mouse_pos[0] > 0:
                    angle = math.atan(
                        (self.screen_height - self.mouse_pos[1]) /
                        self.mouse_pos[0])

                    #calculating velocity
                    velocity = self.constant * math.sqrt(
                        ((self.mouse_pos[0])**2 +
                         (self.screen_height - self.mouse_pos[1])**2))

            #checking for key/button presses
            for event in pygame.event.get():
                if event.type == QUIT:
                    #uninitializing pygame
                    pygame.quit()
                    #using system module to close the window
                    sys.exit()

                #checks for input
                elif event.type == pygame.MOUSEBUTTONUP and math.sqrt(
                        mouse[0]**2 +
                    (self.screen_height - mouse[1])**2) < self.border:
                    #instantiates object and adds it to a list
                    color = (random.randint(50, 200), random.randint(50, 200),
                             random.randint(50, 200))
                    self.particles.append(
                        Object([0, self.screen_height // 2], [
                            velocity * math.cos(angle),
                            -velocity * math.sin(angle)
                        ], 1, 9, color,self))

            #updating display every time the loop repeats

            #updates game state
            #iterates through all particles in projectiles
            for particle in self.particles:
                #applies gravity
                particle.gravity()
                #updates position
                particle.update()
                particle.bounce(self.screen_width, self.screen_height)

            #effectively clears the screen
            self.screen.fill((26, 26, 26))

            #display touch border
            pygame.draw.circle(self.screen, (75, 75, 75),
                               (0, self.screen_height), self.border)

            #loops over all balls
            for particle in self.particles:
                #drawing particle
                pygame.draw.circle(
                    self.screen, (particle.color),
                    (particle.position[0], particle.position[1]),
                    particle.radius)

            #draws the gui to the screen
            self.drawGui()

            #passed updates to screen
            pygame.display.update()


Sim1 = Simulator(0)
Sim2 = Simulator(1)
Sim1.run()
Sim2.run()
