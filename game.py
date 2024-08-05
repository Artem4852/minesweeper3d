from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from algorithm import Grid

app = Ursina()

grid = Grid(mines=20)
grid.new()

player = FirstPersonController()
# player.gravity = 0
player.cursor.visible = False

for y in range(grid.height):
    for x in range(grid.width):
        cell = grid.get_cell(x, y)
        if cell == -1:
            Entity(model="cube", color=color.black, position=(x, 0, y), collider="box")
        elif cell == 1:
            Entity(model="cube", color=color.red, position=(x, 0, y), collider="box")
        elif cell == 2:
            Entity(model="cube", color=color.orange, position=(x, 0, y), collider="box")
        elif cell == 3:
            Entity(model="cube", color=color.yellow, position=(x, 0, y), collider="box")
        elif cell == 4:
            Entity(model="cube", color=color.green, position=(x, 0, y), collider="box")
        else:
            Entity(model="cube", color=color.white, position=(x, 0, y), collider="box")

def update():
    pass

app.run()