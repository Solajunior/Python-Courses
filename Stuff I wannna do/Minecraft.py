from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint

app = Ursina()
window.title = 'Minecraft Sandbox'
window.borderless = False
window.color = color.rgb(120, 180, 255)
window.background_color = color.rgb(120, 180, 255)
window.fps_counter.enabled = True
window.exit_button.visible = False

selected_block = 'grass'
block_palette = ['grass', 'dirt', 'stone', 'sand', 'wood', 'leaves']
block_textures = {
    'grass': 'grass',
    'dirt': 'dirt',
    'stone': 'stone',
    'sand': 'sand',
    'wood': 'wood',
    'leaves': 'leaves',
    'glass': 'glass',
}
world = {}
terrain_radius = 12

Sky(color=color.rgb(120, 200, 255))
DirectionalLight(rotation=(45, 45, 0), color=color.rgb(255, 240, 200))
AmbientLight(color=color.rgba(255, 255, 255, 120))

sun = Entity(parent=scene, position=(20, 25, -30), model='sphere', color=color.yellow, scale=4)
clouds = []
for i in range(10):
    cloud = Entity(parent=scene, position=(randint(-30, 30), randint(15, 25), randint(-30, 30)), model='cube', color=color.white, scale=(randint(4, 8), 1.5, randint(2, 4)))
    cloud.texture = 'white_cube'
    clouds.append(cloud)


def block_key(x, y, z):
    return (int(round(x)), int(round(y)), int(round(z)))


class Voxel(Entity):
    def __init__(self, position=(0, 0, 0), block_type='grass'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture=block_textures.get(block_type, 'white_cube'),
            color=color.white,
            scale=1,
            collider='box'
        )
        self.block_type = block_type


def set_block(x, y, z, block_type):
    key = block_key(x, y, z)
    if key in world:
        return world[key]

    voxel = Voxel(position=(x, y, z), block_type=block_type)
    world[key] = voxel
    return voxel


def remove_block(x, y, z):
    key = block_key(x, y, z)
    if key in world:
        destroy(world[key])
        world.pop(key)


def place_tree(x, y, z):
    trunk_height = randint(3, 5)
    for step in range(trunk_height):
        set_block(x, y + step, z, 'wood')

    canopy_y = y + trunk_height
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            for dy in range(-1, 3):
                if abs(dx) + abs(dz) + abs(dy) > 5:
                    continue
                if dx == 0 and dz == 0 and dy == 0:
                    continue
                set_block(x + dx, canopy_y + dy, z + dz, 'leaves')


def generate_world():
    for x in range(-terrain_radius, terrain_radius + 1):
        for z in range(-terrain_radius, terrain_radius + 1):
            surface = randint(1, 3)
            if abs(x) < 3 and abs(z) < 3:
                surface = 2

            for y in range(surface):
                if y == surface - 1:
                    block_type = 'grass'
                elif y >= surface - 3:
                    block_type = 'dirt'
                else:
                    block_type = 'stone'
                set_block(x, y, z, block_type)

            if surface >= 2 and randint(0, 7) == 0 and abs(x) > 2 and abs(z) > 2:
                place_tree(x, surface, z)

    for x in range(-terrain_radius, terrain_radius + 1):
        for z in range(-terrain_radius, terrain_radius + 1):
            for y in range(-2, 0):
                if (x, y, z) not in world:
                    set_block(x, y, z, 'sand')


def reset_player():
    player.position = (0, 8, 10)
    player.rotation_y = 0


def update_hud():
    selected_text.text = f'Block: {selected_block.upper()}   {selected_block}'


generate_world()

player = FirstPersonController(position=(0, 8, 10), speed=6, jump_height=2, gravity=1.5)
player.cursor.visible = False
player.mouse_sensitivity = Vec2(90, 90)
player.speed = 6
camera.fov = 90
mouse.locked = True

selected_text = Text(text='Block: GRASS', position=(0, 0.45), origin=(0, 0), scale=1.2, background=False)
info_text = Text(
    text='1=grass  2=dirt  3=stone  4=sand  5=wood  6=leaves\nLMB = break   RMB = place   Shift = sprint   Space = jump   R = reset   G = fly   Esc = quit',
    origin=(0, 0),
    y=0.38,
    scale=1.0,
    background=False,
)


def update_block_selection():
    global selected_block
    key_map = {'1': 'grass', '2': 'dirt', '3': 'stone', '4': 'sand', '5': 'wood', '6': 'leaves'}
    for key_name, block_name in key_map.items():
        if held_keys[key_name]:
            selected_block = block_name
            update_hud()


def mine_block():
    hit = raycast(camera.world_position, camera.forward, distance=6, ignore=(player,))
    if hit.hit and hasattr(hit.entity, 'block_type'):
        x, y, z = block_key(hit.entity.x, hit.entity.y, hit.entity.z)
        remove_block(x, y, z)


def place_block():
    hit = raycast(camera.world_position, camera.forward, distance=6, ignore=(player,))
    if not hit.hit or not hasattr(hit.entity, 'block_type'):
        return

    target_x, target_y, target_z = block_key(hit.entity.x, hit.entity.y, hit.entity.z)
    placement = Vec3(target_x, target_y, target_z) + hit.normal
    place_x, place_y, place_z = block_key(placement.x, placement.y, placement.z)

    if distance(Vec3(place_x, place_y, place_z), player.position) < 1.5:
        return
    if (place_x, place_y, place_z) in world:
        return

    set_block(place_x, place_y, place_z, selected_block)


def input(key):
    global selected_block

    if key in '123456':
        selected_block = {'1': 'grass', '2': 'dirt', '3': 'stone', '4': 'sand', '5': 'wood', '6': 'leaves'}[key]
        update_hud()

    if key == 'left mouse down':
        mine_block()
    elif key == 'right mouse down':
        place_block()

    if key == 'r':
        reset_player()

    if key == 'g':
        player.gravity = 0 if player.gravity != 0 else 1.5
        player.speed = 12 if player.gravity == 0 else 6

    if key == 'escape':
        application.quit()


def update():
    update_block_selection()

    if held_keys['left shift']:
        player.speed = 12 if player.gravity == 0 else 10
    else:
        player.speed = 12 if player.gravity == 0 else 6

    if held_keys['left control']:
        player.y -= 2 * time.dt

    if player.gravity == 0:
        if held_keys['space']:
            player.y += 5 * time.dt
        if held_keys['left control']:
            player.y -= 5 * time.dt

    player.y = clamp(player.y, -30, 60)


update_hud()
app.run()
