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
light.intensity = 2

# Floor
for y in range(grid.height):
    for x in range(grid.width):
        Entity(model=f'models/floor{random.randint(0,3)+1}.glb', position=(2*x, 0, 2*y), scale=1, collider='box')

# Fencing
for x in range(grid.width//2):
    fence1 = Entity(model=f'models/fence{random.randint(0,5)+1}.glb', position=(1+4*x, 0.95, -1), scale=1)
    fence1.collider = BoxCollider(fence1, size=(4.1, 6, 0.3))
    fence2 = Entity(model=f'models/fence{random.randint(0,5)+1}.glb', rotation=(0, 180, 0), position=(1+4*x, 0.95, grid.height*2-1), scale=1)
    fence2.collider = BoxCollider(fence2, size=(4.1, 6, 0.3))

for y in range(grid.height//2):
    fence3 = Entity(model=f'models/fence{random.randint(0,5)+1}.glb', rotation=(0, 90, 0), position=(-1, 0.95, 1+4*y), scale=1)
    fence3.collider = BoxCollider(fence3, size=(4.1, 6, 0.3))
    fence4 = Entity(model=f'models/fence{random.randint(0,5)+1}.glb', rotation=(0, 270, 0), position=(grid.width*2-1, 0.95, 1+4*y), scale=1)
    fence4.collider = BoxCollider(fence4, size=(4.1, 6, 0.3))


sign = 1
currentSign = {"n": None, "entity": None}

def update():
    global currentSign, sign
    start = player.position + Vec3(0, 1.5, 0)
    hit = raycast(start, camera.forward, ignore=[player, ])

    if hit.hit:
        hit_pos = hit.entity.position
        player_grid = grid.player_grid
        if player_grid[int(hit_pos.z // 2)][int(hit_pos.x // 2)] == 0:
            pos = hit.entity.position + Vec3(0, 1.5, 0)
            if not currentSign['entity'] or currentSign['entity'].position != pos or currentSign['n'] != sign:
                rotation = currentSign['entity'].rotation if currentSign['entity'] else (0, 0, 0)
                destroy(currentSign['entity'])
                currentSign = {"n": sign, "entity": Entity(model=f'models/sign{random.randint(0,2)+1}_{sign}.glb', rotation=rotation, position=pos, scale=1)}
            elif currentSign['entity']:
                currentSign['entity'].rotation_y += 1

    if held_keys['1']:
        sign = 1
    if held_keys['2']:
        sign = 2
    if held_keys['3']:
        sign = 3
    if held_keys['4']:
        sign = 4

    if held_keys['left mouse'] and hit.hit and currentSign['n']:
        print(currentSign['entity'].model)
        sign = Entity(
            model=currentSign['entity'].model,
            position=hit.entity.position + Vec3(0, 1, 0),
            rotation=currentSign['entity'].rotation,
            scale=currentSign['entity'].scale
        )
        sign.position = hit.entity.position + Vec3(0, 1.5, 0)
        grid.place_sign(currentSign['n'], currentSign['entity'].position)

        destroy(currentSign['entity'])
        currentSign = {"n": None, "entity": None}


app.run()