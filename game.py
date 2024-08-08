from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.lights import DirectionalLight
from datetime import datetime

from algorithm import Grid

app = Ursina()

beep = Audio('sfx/beep.wav', loop=False, autoplay=False)
explosion = Audio('sfx/explosion.wav', loop=False, autoplay=False)

# hammer = Entity(model='models/hammer.glb', position=(0, 2, 5), scale=0.4, collider='box')

grid = Grid(mines=20)
grid.new()
grid.print_grid()

player = FirstPersonController()
player.cast_shadows = True

player.position = (1, 1, 1)
player.cursor.visible = False

camera.ui.enabled = True

mouse.locked = True
mouse.visible = False

menu = Entity(model='quad', color=color.dark_gray, scale=(1, 0.5), parent=camera.ui, enabled=False)
title = Text(text='Minesweeper 3D', scale=(1, 2), y=0.3, x=-0.1, color=color.white, parent=menu)
continue_button = Button(text='Continue', scale=(0.2, 0.1), parent=menu, y=0.1, color=color.white, text_color=color.black)
exit_button = Button(text='Exit', scale=(0.2, 0.1), parent=menu, y=-0.1, color=color.white, text_color=color.black)

def close():
    menu.enabled = False
    mouse.locked = True
    mouse.visible = False
continue_button.on_click = close
exit_button.on_click = application.quit

menu_lost = Entity(model='quad', color=color.dark_gray, scale=(1, 0.5), parent=camera.ui, enabled=False)
title = Text(text='Minesweeper 3D', scale=(1, 2), y=0.3, x=-0.1, color=color.white, parent=menu_lost)
subtitle = Text(text='Game Over', scale=(0.5, 0.5), y=0.1, x=-0.1, color=color.white, parent=menu_lost)
restart_button = Button(text='Restart', scale=(0.2, 0.1), parent=menu_lost, y=0.1, color=color.white, text_color=color.black)
exit_button = Button(text='Exit', scale=(0.2, 0.1), parent=menu_lost, y=-0.1, color=color.white, text_color=color.black)

def restart():
    global signs, help_grid
    grid.new()
    grid.print_grid()
    menu_lost.enabled = False
    mouse.locked = True
    mouse.visible = False
    player.position = (1, 1, 1)
    player.rotation = (0, 0, 0)
    for sign in signs:
        for item in sign:
            destroy(item)
    signs = [[0 for _ in range(grid.width)] for _ in range(grid.height)]
    for item in help_grid:
        item.visible = False

restart_button.on_click = restart
exit_button.on_click = application.quit

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
        menu.enabled = not menu.enabled
        mouse.locked = not mouse.locked
        mouse.visible = not mouse.visible

    if menu.enabled: return

    if key == 'h':
        for item in help_grid:
            item.visible = not item.visible
    elif key == 'm':
        metal_detector.visible = not metal_detector.visible
        sign_around = None if metal_detector.visible else 1

sign_around = 1
currentSign = {"n": None, "entity": None}
signs = [[0 for _ in range(grid.width)] for _ in range(grid.height)]

beeps = 3
last_played = datetime.now().timestamp()

hammer_animation_playing = False
hammer_animation_direction = 1
hammer_animation_stage = 1
hammer_sign = None

def update():
    global currentSign, sign_around, last_played, hammer, hammer_sign, hammer_animation_playing, hammer_animation_direction, hammer_animation_stage
    start = player.position + Vec3(0, 1.5, 0)
    hit = raycast(start, camera.forward, ignore=help_grid+[player], distance=5)

    if hit.hit:
        hit_pos = hit.entity.position
        player_grid = grid.player_grid
        if player_grid[int(hit_pos.z // 2)][int(hit_pos.x // 2)] == 0 and not hammer_animation_playing:
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
        if menu.enabled: return
        sign_around = 1 if not metal_detector.visible else None
    if held_keys['2']:
        if menu.enabled: return
        sign_around = 2 if not metal_detector.visible else None
    if held_keys['3']:
        if menu.enabled: return
        sign_around = 3 if not metal_detector.visible else None
    if held_keys['4']:
        if menu.enabled: return
        sign_around = 4 if not metal_detector.visible else None

    if held_keys['left mouse'] and hit.hit and currentSign['n']:
        if menu.enabled: return
        sign = Entity(
            model=currentSign['entity'].model,
            position=hit.entity.position + Vec3(0, 1.2, 0),
            rotation=currentSign['entity'].rotation,
            scale=currentSign['entity'].scale,
            cast_shadows=True,
            collider='box'
        )
        hammer = Entity(model='models/hammer.glb', position=(1.5, 2.5, 0), scale=1, rotation=(0, 0, -30), collider='box', parent=sign)
        signs[int(hit.entity.position.z // 2)][int(hit.entity.position.x // 2)] = sign
        hammer_sign = sign
        hammer_animation_playing = True
        hammer_animation_direction = 1

        print(grid.get_cell(int(hit.entity.position.x // 2), int(hit.entity.position.z // 2)))

        grid.place_sign(currentSign['n'], currentSign['entity'].position)

        destroy(currentSign['entity'])
        currentSign = {"n": None, "entity": None}
    
    if hammer_animation_playing:
        hammer.rotation_z += -1 * hammer_animation_direction
        if hammer_animation_direction == -1 and hammer.rotation_z >= -30:
            hammer_animation_direction = 1
            hammer_animation_stage += 1

            if hammer_animation_stage == 4:
                hammer_animation_playing = False
                hammer_animation_stage = 1
                hammer.rotation_z = -30
                hammer.visible = False
                hammer_sign.collider = None
                hammer_sign = None

                return
        
        if hammer_animation_stage == 1:
            if hammer.rotation_z <= -67:
                hammer_animation_direction = -1
        
        if hammer_animation_stage == 2:
            if hammer.rotation_z <= -72:
                hammer_animation_direction = -1
        
        if hammer_animation_stage == 3:
            if hammer.rotation_z <= -78:
                hammer_animation_direction = -1

        while hammer.intersects(hammer_sign).hit:
            hammer_sign.position = hammer_sign.position - Vec3(0, 0.001, 0)
            hammer.position = hammer.position + Vec3(0, 0.001, 0)

            if hammer_animation_stage == 3:
                if grid.get_cell(int(hammer_sign.position.x // 2), int(hammer_sign.position.z // 2)) == -1:
                    print("Game Over")
                    explosion.play()
                    menu_lost.enabled = True
                    mouse.locked = False
                    mouse.visible = True


    if held_keys['r'] and hit.hit and player_grid[int(hit_pos.z // 2)][int(hit_pos.x // 2)] != 0:
        if menu.enabled: return
        grid.remove_sign(int(hit_pos.x // 2), int(hit_pos.z // 2))
        destroy(signs[int(hit_pos.z // 2)][int(hit_pos.x // 2)])
        currentSign = {"n": None, "entity": None}

    if metal_detector.visible:
        scan_pos = metal_detector.world_position
        if scan_pos.x < 0 or scan_pos.z < 0 or scan_pos.x > grid.width*2 or scan_pos.z > grid.height*2: return
        cell = grid.get_known_cell(round(scan_pos.x / 2), round(scan_pos.z / 2))
        angle = 45 if cell == 1 else 72 if cell == 2 else 100 if cell == 3 else 145 if cell == 4 else 0
        angle += random.randint(-2, 2) if cell else 0
        metal_detector_arrow.rotation_y = angle
        if cell not in [-1, 0]:
            interval = 1 if cell == 1 else 0.75 if cell == 2 else 0.5 if cell == 3 else 0.25
            if not last_played or datetime.now().timestamp() - last_played > interval:
                beep.play()
                last_played = datetime.now().timestamp()

app.run()