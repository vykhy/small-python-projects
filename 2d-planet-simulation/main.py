import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1200, 728
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont('comicsans', 16)

pygame.display.set_caption('SOLAR SYSTEM SIMULATION')

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 235)
RED = (188, 39, 50)
DARK_GRAY = (80, 71, 81)

class Planet:
    AU = 149000000000       #149 BILLION METRES
    G = 6.67428e-11
    SCALE = 200/ AU         # 1 au = 100px
    TIMESTEP = 3600*24      # 1 day worth of seconds

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius/5      
        self.color = color
        self.mass = mass
        self.x_velocity = 0
        self.y_velocity = 0
        self.sun = False
        self.distance = 0
        self.orbit = []

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        # if len(self.orbit) > 2:
        #     # to draw orbit
        #     updated_points = []
        #     for point in self.orbit:
        #         x, y = point
        #         x = x * self.SCALE + WIDTH / 2
        #         y = y * self.SCALE + HEIGHT / 2
        #         updated_points.append((x, y))
            
            # pygame.draw.lines(WIN, self.color, False, updated_points, 1)
        pygame.draw.line(WIN, self.color, (x, y), (WIDTH/2, HEIGHT/2))

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance/1000, 1)}km", 1, WHITE)
            WIN.blit(distance_text, (x,y))
#  - distance_text.get_width()/2 -distance_text.get_height()/2
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x = other.x
        other_y = other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x **2 + distance_y**2)
        
        if other.sun:
            self.distance = distance
        
        force = self.G*self.mass*other.mass/distance**2     #total force
        theta = math.atan2(distance_y, distance_x)          #angle of force
        force_x = math.cos(theta) * force                   #force on x axis
        force_y = math.sin(theta) * force                   #force on y axis
        return force_x, force_y

    def update_position(self, planets):
        # i dont want the sun to move when playing with the values
        if self.sun:
            return

        total_fx = total_fy = 0             #force from all other objects
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)        #force from this planet
            total_fx += fx
            total_fy += fy

        # _ velocity is equal to _ velocity added by the effect of total force from all objects
        # on its mass, multiplied by timestep because each frame is set as a day(or whatever TIMESTEP is)
        self.x_velocity += total_fx / self.mass * self.TIMESTEP
        self.y_velocity += total_fy / self.mass * self.TIMESTEP

        # finally update the position of the planet
        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP

        # save this point on the orbit
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    mercury = Planet(0.387*Planet.AU, 0, 8, DARK_GRAY, 0.330*10**23)
    mercury.y_velocity = -47400
    venus = Planet(0.723*Planet.AU, 0, 14, WHITE, 4.8685*10**24)
    venus.y_velocity = -35.02*1000
    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_velocity = 29783
    mars = Planet(-1.524*Planet.AU,0, 12, RED, 6.39*10**23)
    mars.y_velocity = 24077
    venus2 = Planet(2.223*Planet.AU, 0, 14, WHITE, 4.8685*10**24)
    venus2.y_velocity = -35.02*1000/3

    planets = [sun, mercury, venus, earth, mars, venus2]

    while run:

        clock.tick(60)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        for index, planet in enumerate(planets):
            distance_text = FONT.render(f"{round(planet.distance/1000000000, 1)}million km", 1, WHITE)
            WIN.blit(distance_text, (0,index * 20))

        pygame.display.update()

    pygame.quit()

main()
