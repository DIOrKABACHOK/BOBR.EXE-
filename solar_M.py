import tkinter as tk
import math

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2
STAR_RADIUS = 10
PLANET_RADIUS = 5
SATELLITE_RADIUS = 2
ORBIT_SPACING = 30


# Класс для звезды
class Star:
    def __init__(self, canvas, x, y, num_planets):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.num_planets = num_planets
        self.planets = []
        self.draw_star()
        self.create_planets()

    def draw_star(self):
        self.canvas.create_oval(self.x - STAR_RADIUS, self.y - STAR_RADIUS,
                                self.x + STAR_RADIUS, self.y + STAR_RADIUS,
                                fill="yellow")

    def create_planets(self):
        for i in range(self.num_planets):
            angle = i * (360 / self.num_planets)
            orbit_radius = ORBIT_SPACING * (i // 4 + 1)
            clockwise = (i % 2 == 0)
            planet = Planet(self.canvas, self.x, self.y, orbit_radius, angle, clockwise)
            self.planets.append(planet)


# Класс для планеты
class Planet:
    def __init__(self, canvas, star_x, star_y, orbit_radius, angle, clockwise):
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

    def create_planet(self):
        x = self.star_x + self.orbit_radius * math.cos(math.radians(self.angle))
        y = self.star_y + self.orbit_radius * math.sin(math.radians(self.angle))
        self.planet = self.canvas.create_oval(x - PLANET_RADIUS, y - PLANET_RADIUS,
                                              x + PLANET_RADIUS, y + PLANET_RADIUS,
                                              fill="blue")
        if self.orbit_radius // ORBIT_SPACING % 2 != 0:
            self.satellite = Satellite(self.canvas, x, y, SATELLITE_RADIUS)

    def create_orbit(self):
        self.orbit = self.canvas.create_oval(self.star_x - self.orbit_radius, self.star_y - self.orbit_radius,
                                             self.star_x + self.orbit_radius, self.star_y + self.orbit_radius,
                                             outline="white")

    def move(self):
        if self.clockwise:
            self.angle -= 1
        else:
            self.angle += 1

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
                                                 fill="grey")

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
        self.stars = []
        self.create_stars()
        self.animate()

    def create_stars(self):
        self.stars.append(Star(self.canvas, CENTER_X - 200, CENTER_Y, 10))
        self.stars.append(Star(self.canvas, CENTER_X, CENTER_Y, 20))
        self.stars.append(Star(self.canvas, CENTER_X + 200, CENTER_Y, 10))

    def animate(self):
        for star in self.stars:
            for planet in star.planets:
                planet.move()
        self.root.after(50, self.animate)
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
        self.stars.append(Star(self.canvas, CENTER_X - 200, CENTER_Y, 10))
        self.stars.append(Star(self.canvas, CENTER_X, CENTER_Y, 20))
        self.stars.append(Star(self.canvas, CENTER_X + 200, CENTER_Y, 10))

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

