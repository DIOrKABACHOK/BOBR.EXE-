import tkinter as tk
import math

# Константы
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 810
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2
STAR_RADIUS = 10
PLANET_RADIUS = 5
SATELLITE_RADIUS = 3
ORBIT_SPACING = 79
PLANETS_PER_ORBIT = 4

# Класс для звезды
class Star:
    def __init__(self, canvas, x, y, num_planets, is_second_star=False):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.num_planets = num_planets
        self.planets = []
        self.is_second_star = is_second_star
        self.draw_star()
        self.create_planets()

    def draw_star(self):
        self.canvas.create_oval(self.x - STAR_RADIUS, self.y - STAR_RADIUS,
                                self.x + STAR_RADIUS, self.y + STAR_RADIUS,
                                fill="yellow")

    def create_planets(self):
        num_orbits = (self.num_planets + PLANETS_PER_ORBIT - 1) // PLANETS_PER_ORBIT
        planets_per_orbit = [min(PLANETS_PER_ORBIT, self.num_planets - i * PLANETS_PER_ORBIT) for i in range(num_orbits)]
        for orbit in range(1, num_orbits + 1):
            for i in range(planets_per_orbit[orbit - 1]):
                angle = i * (360 / planets_per_orbit[orbit - 1])
                orbit_radius = ORBIT_SPACING * orbit
                clockwise = (orbit % 2 == 0)  # Планеты на четных орбитах вращаются по часовой стрелке
                has_satellite = self.is_second_star and (orbit % 2 != 0)
                planet = Planet(self.canvas, self.x, self.y, orbit_radius, angle, clockwise, has_satellite)
                self.planets.append(planet)

# Класс для планеты
class Planet:
    def __init__(self, canvas, star_x, star_y, orbit_radius, angle, clockwise, has_satellite=False):
        self.canvas = canvas
        self.star_x = star_x
        self.star_y = star_y
        self.orbit_radius = orbit_radius
        self.angle = angle
        self.clockwise = clockwise
        self.planet = None
        self.orbit = None
        self.satellite = None
        self.create_planet()
        self.create_orbit()
        if has_satellite:
            self.create_satellite()

    def create_planet(self):
        x = self.star_x + self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.star_y + self.orbit_radius * math.sin(math.radians(self.angle))
        self.planet = self.canvas.create_oval(x - PLANET_RADIUS, y - PLANET_RADIUS,
                                              x + PLANET_RADIUS, y + PLANET_RADIUS,
                                              fill="blue")

    def create_orbit(self):
        self.orbit = self.canvas.create_oval(self.star_x - self.orbit_radius, self.star_y - self.orbit_radius,
                                             self.star_x + self.orbit_radius, self.star_y + self.orbit_radius,
                                             outline="white")

    def create_satellite(self):
        x = self.star_x + self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.star_y + self.orbit_radius * math.sin(math.radians(self.angle))
        self.satellite = Satellite(self.canvas, x, y, SATELLITE_RADIUS)

    def move(self):
        if self.clockwise:
            self.angle += 1
        else:
            self.angle -= 1

        x = self.star_x + self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.star_y + self.orbit_radius * math.sin(math.radians(self.angle))
        self.canvas.coords(self.planet, x - PLANET_RADIUS, y - PLANET_RADIUS,
                           x + PLANET_RADIUS, y + PLANET_RADIUS)
        if self.satellite:
            self.satellite.move(x, y)

# Класс для спутника
class Satellite:
    def __init__(self, canvas, planet_x, planet_y, radius):
        self.canvas = canvas
        self.planet_x = planet_x
        self.planet_y = planet_y
        self.radius = radius
        self.angle = 0
        self.create_satellite()

    def create_satellite(self):
        x = self.planet_x + self.radius * 2 * math.cos(math.radians(self.angle))
        y = self.planet_y + self.radius * 2 * math.sin(math.radians(self.angle))
        self.satellite = self.canvas.create_oval(x - SATELLITE_RADIUS, y - SATELLITE_RADIUS,
                                                 x + SATELLITE_RADIUS, y + SATELLITE_RADIUS,
                                                 fill="red")

    def move(self, planet_x, planet_y):
        self.planet_x = planet_x
        self.planet_y = planet_y
        self.angle += 5
        x = self.planet_x + self.radius * 2 * math.cos(math.radians(self.angle))
        y = self.planet_y + self.radius * 2 * math.sin(math.radians(self.angle))
        self.canvas.coords(self.satellite, x - SATELLITE_RADIUS, y - SATELLITE_RADIUS,
                           x + SATELLITE_RADIUS, y + SATELLITE_RADIUS)

# Главный класс для интерфейса и анимации
class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()
        self.show_orbits = tk.BooleanVar()
        self.show_orbits.set(True)
        self.create_ui()
        self.stars = []
        self.create_stars()
        self.animate()

    def create_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()
        orbit_checkbox = tk.Checkbutton(control_frame, text="Show Orbits", variable=self.show_orbits, command=self.toggle_orbits)
        orbit_checkbox.pack(side=tk.LEFT)

    def create_stars(self):
        self.stars.append(Star(self.canvas, CENTER_X - 300, CENTER_Y, 10))
        self.stars.append(Star(self.canvas, CENTER_X, CENTER_Y, 20, is_second_star=True))
        self.stars.append(Star(self.canvas, CENTER_X + 300, CENTER_Y, 10))

    def toggle_orbits(self):
        for star in self.stars:
            for planet in star.planets:
                if self.show_orbits.get():
                    self.canvas.itemconfigure(planet.orbit, state='normal')
                else:
                    self.canvas.itemconfigure(planet.orbit, state='hidden')

    def animate(self):
        for star in self.stars:
            for planet in star.planets:
                planet.move()
        self.root.after(50, self.animate)

def main():
    root = tk.Tk()
    app = SolarSystemApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
