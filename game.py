from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.lights import DirectionalLight

from algorithm import Grid

app = Ursina()

grid = Grid(mines=20)
grid.new()

player = FirstPersonController()
# player.gravity = 0
player.position = (1, 1, 1)
player.cursor.visible = False

light = DirectionalLight()
light.rotation = Vec3(45, 45, 0)
# light.color = color.rgb(255, 241, 224)

# Floor
for y in range(grid.height):
    for x in range(grid.width):
        Entity(model=f'models/floor{random.randint(0,3)+1}.obj', position=(2*x, 0, 2*y), scale=1, collider='box')

# Fencing
for x in range(grid.width//2):
    fence1 = Entity(model=f'models/fence{random.randint(0,5)+1}.obj', position=(1+4*x, 0.95, -1), scale=1)
    fence1.collider = BoxCollider(fence1, size=(4.1, 6, 0.3))
    fence2 = Entity(model=f'models/fence{random.randint(0,5)+1}.obj', rotation=(0, 180, 0), position=(1+4*x, 0.95, grid.height*2-1), scale=1)
    fence2.collider = BoxCollider(fence2, size=(4.1, 6, 0.3))

for y in range(grid.height//2):
    fence3 = Entity(model=f'models/fence{random.randint(0,5)+1}.obj', rotation=(0, 90, 0), position=(-1, 0.95, 1+4*y), scale=1)
    fence3.collider = BoxCollider(fence3, size=(4.1, 6, 0.3))
    fence4 = Entity(model=f'models/fence{random.randint(0,5)+1}.obj', rotation=(0, 270, 0), position=(grid.width*2-1, 0.95, 1+4*y), scale=1)
    fence4.collider = BoxCollider(fence4, size=(4.1, 6, 0.3))

currentSign = None
def update():
    global currentSign
    start = player.position + Vec3(0, 1.5, 0)
    hit = raycast(start, camera.forward, ignore=[player, ])

    if hit.hit:
        pos = hit.entity.position + Vec3(0, 1, 0)
        if not currentSign or currentSign.position != pos:
            destroy(currentSign)
            currentSign = Entity(model=f'models/sign{random.randint(0,2)+1}.obj', position=pos, scale=1)


app.run()