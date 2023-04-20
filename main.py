#importing pygame library to my project
import pygame, sys
from pygame.locals import QUIT
import math
import random


#setting variables
screen_width = 1000
screen_height = 600
projectiles = []
bounce_damping = 0.9
constant = 0.2
border = 300

#initializing pygame with innit function
pygame.init()
#setting up a display surface with dimensions 400*300
screen = pygame.display.set_mode((screen_width, screen_height))
#setting a caption for the window
pygame.display.set_caption('Simulator')

clock = pygame.time.Clock()


#initializing pygame font module
pygame.font.init()
#setting up a default font and size
font = pygame.font.SysFont(None, 24)

class Object:
    #constructor class
    def __init__(self, position, velocity, acceleration, radius,color):
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.radius = radius
        self.color = color

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
        for other in projectiles:
            if other != self:
                #it then calls the collide function with the other object
                self.collide(other)
        #checks if the sphere is overlapping with border
        if self.position[0] - self.radius < 0:
            # sets the velocity in the other direction and  multiplys by bounce damping
            self.velocity[0] = abs(self.velocity[0]) * bounce_damping
            #sets position so it is just on the edge and not over the edge
            self.position[0] = self.radius

        #repeats 4 times for 4 differant walls varying slightly
        elif self.position[0] + self.radius > screen_width:
            self.velocity[0] = -abs(self.velocity[0]) * bounce_damping
            self.position[0] = screen_width - self.radius

        if self.position[1] - self.radius < 0:
            self.velocity[1] = abs(self.velocity[1]) * bounce_damping
            self.position[1] = self.radius

        elif self.position[1] + self.radius > screen_height:
            self.velocity[1] = -abs(self.velocity[1]) * bounce_damping
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
            self.velocity[0] = v1f_x * bounce_damping
            self.velocity[1] = v1f_y* bounce_damping
            other.velocity[0] = v2f_x* bounce_damping
            other.velocity[1] = v2f_y* bounce_damping


##creates an instance of an object from objet class



#default data
velocity = 10
angle = 45
mouse_pos = [200,screen_height-200]

#main simulation loop
while True:

    clock.tick(60)
        
    ## returns a array with mouse x and y position
    mouse = list(pygame.mouse.get_pos())
    if  math.sqrt(mouse[0]**2 + (screen_height-mouse[1])**2) < border:
            mouse_pos = mouse

        
        
    # validity
    if mouse_pos[0] != None:
        #calculating angle
        if mouse_pos[0] > 0:
            angle = math.atan((screen_height - mouse_pos[1]) / mouse_pos[0])
            #calculating velocity
            velocity =  constant * math.sqrt(((mouse_pos[0])**2 + (screen_height - mouse_pos[1])**2)) 

                
    #checking for key/button presses
    for event in pygame.event.get():
        if event.type == QUIT:
            #uninitializing pygame
            pygame.quit()
            #using system module to close the window
            sys.exit()

        #checks for input
        elif event.type == pygame.MOUSEBUTTONUP and math.sqrt(mouse[0]**2 + (screen_height-mouse[1])**2) < border:
            #instantiates object and adds it to a list
            color = (random.randint(50,200),random.randint(50,200),random.randint(50,200))
            projectiles.append(
                Object(
                    [0, screen_height],
                    [velocity * math.cos(angle), -velocity * math.sin(angle)],
                    1,
                    25,
                    color
            ))

    #updating display every time the loop repeats

    #updates game state
    #iterates through all particles in projectiles
    for particle in projectiles:
        #applies gravity
        particle.gravity()
        #updates position
        particle.update()
        particle.bounce(screen_width, screen_height)

    #effectively clears the screen
    screen.fill((26,26,26))

    #display touch border
    pygame.draw.circle(screen, (75,75,75), (0, screen_height),border)
        
    #loops over all balls
    for particle in projectiles:
        #drawing particle
        pygame.draw.circle(screen, (particle.color), (particle.position[0], particle.position[1]), particle.radius)

    #labels white line
    text_surface = font.render(str(int(velocity)), True, (255, 255, 255))
    #displaying text surface to screen
    screen.blit(text_surface, (mouse_pos[0]+20,mouse_pos[1]+20))

    #labels angle
    text_surface = font.render(str(int(angle * (180/3.14159))), True, (255, 255, 255))
    screen.blit(text_surface, (20,screen_height-20))

    #draws a white line resultant component of velocity
    pygame.draw.line(screen, (255,255,255), (0,screen_height), (mouse_pos[0],mouse_pos[1]),3) 

    #draws a red line x component of velocity
    pygame.draw.line(screen, (255,0,0), (0,screen_height), (mouse_pos[0],screen_height),3) 

    #labels red line with x component of velocity
    text_surface = font.render(str(int(velocity * math.cos(angle))), True, (255,0,0))
    screen.blit(text_surface, (mouse_pos[0]//2,screen_height-24))

    #draws a blue line y component of velocity
    pygame.draw.line(screen, (0,0,255), (mouse_pos[0],screen_height), (mouse_pos[0],mouse_pos[1]),3) 

    #labels a blue line with y component of velocit
    text_surface = font.render(str(int(velocity * math.sin(angle))), True, (0,0,255))
    screen.blit(text_surface, (mouse_pos[0]+12,screen_height - (screen_height-mouse_pos[1])//2 ))
        
    #draws an arc between circle and projection line
    pygame.draw.arc(screen, (255,255,255),[-50,screen_height-50,100,100], 0,angle,3)
        
    #passed updates to screen
    pygame.display.update()
