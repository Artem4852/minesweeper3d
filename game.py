from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.lights import DirectionalLight

from algorithm import Grid

app = Ursina()

grid = Grid(mines=20)
grid.new()

player = FirstPersonController()
player.cast_shadows = True
# player.gravity = 0
player.position = (1, 1, 1)
player.cursor.visible = False

light = DirectionalLight()
light.rotation = Vec3(45, 45, 0)
light.intensity = 2
light.cast_shadows = True

camera.bloom = True
camera.bloom_threshold = 0.3
camera.bloom_intensity = 1.5

sky = Sky()
sky.color = color.rgb(135, 206, 235)

# Metal detector
metal_detector = Entity(model='models/metal_detector.glb', position=(-0.3, 0.2, 0.8), scale=0.7, cast_shadows=True, parent=player, visible=False)
metal_detector_arrow = Entity(model='models/metal_detector_arrow.glb', position=(0, 1.68, -0.97), scale=1, cast_shadows=True, parent=metal_detector, rotation=(0, 0, 0))

# HelpGrid
help_grid = []
for y in range(grid.height):
    for x in range(grid.width):
        help_grid_item = Entity(model='plane', position=(2*x, 1.1, 2*y), scale=(1.8, 1, 1.8), collider='box', color=(255, 255, 255, 0.1))
        help_grid_item.cast_shadows = False
        help_grid_item.receive_shadows = False
        help_grid_item.visible = False
        help_grid.append(help_grid_item)

# Floor
for y in range(grid.height):
    for x in range(grid.width):
        floor = Entity(model=f'models/floor{random.randint(0,3)+1}.glb', position=(2*x, 0, 2*y), scale=1, collider='box')
        floor.cast_shadows = True
        floor.receive_shadows = True

        # floor = Entity(model='cube', position=(2*x, 0, 2*y), scale=(2, 2, 2), collider='box')
        # cell = grid.get_cell(x, y)
        # if cell == 1:
        #     floor.color = color.rgb(255, 0, 0)
        # elif cell == 2:
        #     floor.color = color.rgb(0, 255, 0)
        # elif cell == 3:
        #     floor.color = color.rgb(0, 0, 255)
        # elif cell == 4:
        #     floor.color = color.rgb(255, 255, 0)
        # elif cell == 0:
        #     floor.color = color.rgb(255, 255, 255)
        # else:
        #     floor.color = color.rgb(0, 0, 0)

# Fence
for x in range(grid.width//2):
    fence1 = Entity(model=f'models/fence{random.randint(0,5)+1}.glb', position=(1+4*x, 0.95, -1), scale=1, cast_shadows=True)
    fence1.collider = BoxCollider(fence1, size=(4.1, 6, 0.3))
    fence2 = Entity(model=f'models/fence{random.randint(0,5)+1}.glb', rotation=(0, 180, 0), position=(1+4*x, 0.95, grid.height*2-1), scale=1, cast_shadows=True)
    fence2.collider = BoxCollider(fence2, size=(4.1, 6, 0.3))

for y in range(grid.height//2):
    fence3 = Entity(model=f'models/fence{random.randint(0,5)+1}.glb', rotation=(0, 90, 0), position=(-1, 0.95, 1+4*y), scale=1, cast_shadows=True)
    fence3.collider = BoxCollider(fence3, size=(4.1, 6, 0.3))
    fence4 = Entity(model=f'models/fence{random.randint(0,5)+1}.glb', rotation=(0, 270, 0), position=(grid.width*2-1, 0.95, 1+4*y), scale=1, cast_shadows=True)
    fence4.collider = BoxCollider(fence4, size=(4.1, 6, 0.3))

def input(key):
    global sign_around
    if key == 'escape':
        application.quit()
    elif key == 'h':
        for item in help_grid:
            item.visible = not item.visible
    elif key == 'm':
        metal_detector.visible = not metal_detector.visible
        sign_around = None if metal_detector.visible else 1

sign_around = 1
currentSign = {"n": None, "entity": None}

def update():
    global currentSign, sign_around
    start = player.position + Vec3(0, 1.5, 0)
    hit = raycast(start, camera.forward, ignore=help_grid+[player])

    if hit.hit:
        hit_pos = hit.entity.position
        player_grid = grid.player_grid
        if player_grid[int(hit_pos.z // 2)][int(hit_pos.x // 2)] == 0:
            pos = hit.entity.position + Vec3(0, 1.5, 0)
            if not currentSign['entity'] or currentSign['entity'].position != pos or currentSign['n'] != sign_around:
                rotation = currentSign['entity'].rotation if currentSign['entity'] else (0, 0, 0)
                destroy(currentSign['entity'])
                if not sign_around: currentSign = {"n": None, "entity": None}
                else:
                    currentSign = {"n": sign_around, "entity": Entity(model=f'models/sign{random.randint(0,2)+1}_{sign_around}.glb', rotation=rotation, position=pos, scale=0.4)}
                    currentSign['entity'].cast_shadows = True
            elif currentSign['entity']:
                currentSign['entity'].rotation_y += 1 if not held_keys['r'] else 5
        else:
            destroy(currentSign['entity'])
            currentSign = {"n": None, "entity": None}

    if held_keys['1']:
        sign_around = 1 if not metal_detector.visible else None
    if held_keys['2']:
        sign_around = 2 if not metal_detector.visible else None
    if held_keys['3']:
        sign_around = 3 if not metal_detector.visible else None
    if held_keys['4']:
        sign_around = 4 if not metal_detector.visible else None

    if held_keys['left mouse'] and hit.hit and currentSign['n']:
        sign = Entity(
            model=currentSign['entity'].model,
            position=hit.entity.position + Vec3(0, 1, 0),
            rotation=currentSign['entity'].rotation,
            scale=currentSign['entity'].scale,
            cast_shadows=True
        )
        print(grid.get_cell(int(hit.entity.position.x // 2), int(hit.entity.position.z // 2)))
        if grid.get_cell(int(hit.entity.position.x // 2), int(hit.entity.position.z // 2)) == -1:
            print("Game Over")
            application.quit()
        grid.place_sign(currentSign['n'], currentSign['entity'].position)

        destroy(currentSign['entity'])
        currentSign = {"n": None, "entity": None}

    if metal_detector.visible:
        scan_pos = metal_detector.world_position
        cell = grid.get_known_cell(round(scan_pos.x / 2), round(scan_pos.z / 2))
        angle = 45 if cell == 1 else 72 if cell == 2 else 100 if cell == 3 else 145 if cell == 4 else 0
        angle += random.randint(-2, 2) if cell else 0
        metal_detector_arrow.rotation_y = angle

app.run()