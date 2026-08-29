from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint

app = Ursina()
window.title = 'Minecraft 3D'
window.borderless = False
window.color = color.rgb(120, 180, 255)
window.background_color = color.rgb(120, 180, 255)
window.fps_counter.enabled = True
window.exit_button.visible = False

selected_block = 'grass'
block_types = ['grass', 'dirt', 'stone', 'sand', 'wood', 'leaves']
block_colors = {
    'grass': color.rgb(94, 168, 74),
    'dirt': color.rgb(122, 85, 52),
    'stone': color.rgb(125, 125, 125),
    'sand': color.rgb(214, 204, 148),
    'wood': color.rgb(156, 110, 62),
    'leaves': color.rgb(67, 175, 80),
}

Sky(color=color.rgb(120, 200, 255))
DirectionalLight(rotation=(45, 45, 0), color=color.rgb(255, 240, 200))
AmbientLight(color=color.rgba(255, 255, 255, 120))

class Voxel(Entity):
    def __init__(self, position=(0, 0, 0), block_type='grass'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture='white_cube',
            color=block_colors[block_type],
            scale=1,
            collider='box'
        )
        self.block_type = block_type


def build_ground():
    for x in range(-10, 11):
        for z in range(-10, 11):
            for y in range(0, 2):
                block_type = 'grass' if y == 1 else 'dirt'
                Voxel(position=(x, y, z), block_type=block_type)

            if randint(0, 16) == 0 and abs(x) > 2 and abs(z) > 2:
                trunk_height = randint(2, 4)
                for y in range(trunk_height):
                    Voxel(position=(x, 2 + y, z), block_type='wood')
                for dx in range(-1, 2):
                    for dz in range(-1, 2):
                        for dy in range(2):
                            if dx == 0 and dz == 0 and dy == 0:
                                continue
                            Voxel(position=(x + dx, 2 + trunk_height - 1 + dy, z + dz), block_type='leaves')


build_ground()

player = FirstPersonController(position=(0, 5, 8), speed=6, jump_height=2)
player.cursor.visible = False
player.gravity = 1.5
camera.fov = 90
mouse.locked = True

Text(text='1=grass  2=dirt  3=stone  4=sand  5=wood  6=leaves\nLeft click = break   Right click = place   Shift = sprint   R = reset   Esc = quit', origin=(0, 0), y=0.45, scale=1.1, background=False)


def update_block_selection():
    global selected_block
    for key_name, block_name in {'1': 'grass', '2': 'dirt', '3': 'stone', '4': 'sand', '5': 'wood', '6': 'leaves'}.items():
        if held_keys[key_name]:
            selected_block = block_name


def update():
    update_block_selection()

    if held_keys['escape']:
        application.quit()
    if held_keys['left shift']:
        player.speed = 10
    else:
        player.speed = 6

    if held_keys['r']:
        player.position = (0, 5, 8)

    if held_keys['left control']:
        player.y -= 2 * time.dt

    player.y = clamp(player.y, -20, 40)


app.run()
