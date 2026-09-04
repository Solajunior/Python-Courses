from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint, choice
import math

app = Ursina()
window.title = 'Minecraft Survival Sandbox'
window.borderless = False
window.color = color.rgb(120, 180, 255)
window.background_color = color.rgb(120, 180, 255)
window.fps_counter.enabled = True
window.exit_button.visible = False

selected_block = 'grass'
terrain_radius = 18
last_generated_center = None
generated_world = set()
world = {}
mobs = []

block_textures = {
    'grass': 'grass',
    'dirt': 'dirt',
    'stone': 'stone',
    'sand': 'sand',
    'wood': 'wood',
    'leaves': 'leaves',
    'glass': 'glass',
    'water': 'water',
    'coal_ore': 'stone',
    'iron_ore': 'stone',
    'gold_ore': 'stone',
    'diamond_ore': 'stone',
    'bedrock': 'stone',
}

inventory = {
    'grass': 25,
    'dirt': 20,
    'stone': 25,
    'sand': 15,
    'wood': 12,
    'leaves': 8,
    'glass': 0,
    'water': 0,
    'coal_ore': 0,
    'iron_ore': 0,
    'gold_ore': 0,
    'diamond_ore': 0,
    'pickaxe': 0,
    'sword': 0,
}

recipes = {
    'pickaxe': {'wood': 3, 'stone': 2},
    'sword': {'wood': 2, 'stone': 3},
    'glass': {'sand': 2},
    'iron_pickaxe': {'iron_ore': 3, 'wood': 2},
}

Sky(color=color.rgb(120, 200, 255))
DirectionalLight(rotation=(45, 45, 0), color=color.rgb(255, 240, 200))
AmbientLight(color=color.rgba(255, 255, 255, 120))

sun = Entity(parent=scene, position=(20, 25, -30), model='sphere', color=color.yellow, scale=4)
clouds = []
for i in range(12):
    cloud = Entity(
        parent=scene,
        position=(randint(-30, 30), randint(15, 25), randint(-30, 30)),
        model='cube',
        color=color.white,
        scale=(randint(4, 8), 1.5, randint(2, 4)),
    )
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
            collider='box',
        )
        self.block_type = block_type


class Mob(Entity):
    def __init__(self, position=(0, 0, 0), mob_type='zombie'):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            color=color.green if mob_type == 'zombie' else color.red,
            scale=(0.8, 1.6, 0.8),
            collider='box',
        )
        self.mob_type = mob_type
        self.is_mob = True
        self.hp = 12 if mob_type == 'zombie' else 10
        self.damage = 1 if mob_type == 'zombie' else 1.5
        self.speed = 1.4 if mob_type == 'zombie' else 1.8

    def update_ai(self):
        if not player:
            return

        direction = Vec3(player.x - self.x, 0, player.z - self.z)
        distance_to_player = direction.length()
        if distance_to_player > 0.001:
            direction = direction.normalized()
            if distance_to_player > 1.5:
                self.position += direction * self.speed * time.dt
            else:
                player.health -= self.damage * time.dt

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            destroy(self)
            if self in mobs:
                mobs.remove(self)
            inventory['coal_ore'] = inventory.get('coal_ore', 0) + randint(0, 2)
            inventory['stone'] = inventory.get('stone', 0) + 1


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
        block_type = world[key].block_type
        inventory[block_type] = inventory.get(block_type, 0) + 1
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


def find_surface_height(x, z):
    for y in range(18, -5, -1):
        if block_key(x, y, z) in world:
            return y
    return 1


def generate_column(x, z):
    height = 2 + int((math.sin(x * 0.8) + math.cos(z * 0.9)) * 2) + randint(0, 2)
    height = max(2, min(8, height))

    if abs(x) < 3 and abs(z) < 3:
        height = 2

    is_desert = abs(x) % 9 == 0 or abs(z) % 9 == 0

    for y in range(height):
        if y == height - 1:
            block_type = 'sand' if is_desert else 'grass'
        elif y >= height - 3:
            block_type = 'sand' if is_desert else 'dirt'
        else:
            block_type = 'stone'
        set_block(x, y, z, block_type)

        if block_type == 'stone' and randint(0, 35) == 0:
            ore_choice = choice(['coal_ore', 'iron_ore', 'gold_ore', 'diamond_ore'])
            set_block(x, y, z, ore_choice)

    if randint(0, 7) == 0 and abs(x) > 2 and abs(z) > 2:
        place_tree(x, height, z)

    for y in range(-2, 0):
        if (x, y, z) not in world:
            set_block(x, y, z, 'sand')


def generate_world_around_player(center_x, center_z, radius=terrain_radius):
    min_x = int(center_x) - radius
    max_x = int(center_x) + radius
    min_z = int(center_z) - radius
    max_z = int(center_z) + radius

    for x in range(min_x, max_x + 1):
        for z in range(min_z, max_z + 1):
            if (x, z) in generated_world:
                continue
            generate_column(x, z)
            generated_world.add((x, z))


def spawn_mob():
    if len(mobs) >= 14:
        return

    spawn_x = int(player.x) + randint(-18, 18)
    spawn_z = int(player.z) + randint(-18, 18)
    spawn_y = find_surface_height(spawn_x, spawn_z) + 1

    if (spawn_x, spawn_y, spawn_z) in world:
        return

    mob_type = choice(['zombie', 'skeleton'])
    enemy = Mob(position=(spawn_x, spawn_y, spawn_z), mob_type=mob_type)
    mobs.append(enemy)


def reset_player():
    player.position = (0, 8, 10)
    player.rotation_y = 0
    player.health = 20


def craft_item(item_name):
    if item_name not in recipes:
        print('Unknown recipe.')
        return

    recipe = recipes[item_name]
    for material, needed in recipe.items():
        if inventory.get(material, 0) < needed:
            print(f'Not enough {material} to craft {item_name}.')
            return

    for material, needed in recipe.items():
        inventory[material] -= needed

    inventory[item_name] += 1
    print(f'Crafted {item_name}!')
    update_hud()


def update_hud():
    if 'player' in globals():
        selected_text.text = (
            f'Block: {selected_block.upper()}   |   Health: {int(player.health)}   |   ' 
            f'Pickaxe: {inventory["pickaxe"]}   |   Sword: {inventory["sword"]}'
        )


def update_block_selection():
    global selected_block
    key_map = {
        '1': 'grass', '2': 'dirt', '3': 'stone', '4': 'sand',
        '5': 'wood', '6': 'leaves', '7': 'glass', '8': 'water'
    }
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
    if inventory.get(selected_block, 0) <= 0:
        return

    inventory[selected_block] -= 1
    set_block(place_x, place_y, place_z, selected_block)


def attack():
    hit = raycast(camera.world_position, camera.forward, distance=6, ignore=(player,))
    if hit.hit and getattr(hit.entity, 'is_mob', False):
        damage = 5 if inventory.get('sword', 0) > 0 else 2
        hit.entity.take_damage(damage)
        return

    for mob in mobs:
        if distance(mob.position, player.position) < 2.6:
            damage = 5 if inventory.get('sword', 0) > 0 else 2
            mob.take_damage(damage)
            return


def input(key):
    global selected_block

    if key in '12345678':
        selected_block = {
            '1': 'grass', '2': 'dirt', '3': 'stone', '4': 'sand',
            '5': 'wood', '6': 'leaves', '7': 'glass', '8': 'water'
        }[key]
        update_hud()

    if key == 'left mouse down':
        hit = raycast(camera.world_position, camera.forward, distance=6, ignore=(player,))
        if hit.hit and getattr(hit.entity, 'is_mob', False):
            attack()
        elif hit.hit and hasattr(hit.entity, 'block_type'):
            mine_block()

    elif key == 'right mouse down':
        place_block()

    if key == 'c':
        craft_item('pickaxe')
    elif key == 'v':
        craft_item('sword')
    elif key == 'b':
        craft_item('glass')

    if key == 'r':
        reset_player()

    if key == 'g':
        player.gravity = 0 if player.gravity != 0 else 1.5
        player.speed = 12 if player.gravity == 0 else 6

    if key == 'escape':
        application.quit()


def update():
    global last_generated_center

    update_block_selection()

    current_center = (int(player.x), int(player.z))
    if last_generated_center is None or abs(current_center[0] - last_generated_center[0]) > terrain_radius // 2 or abs(current_center[1] - last_generated_center[1]) > terrain_radius // 2:
        generate_world_around_player(player.x, player.z)
        last_generated_center = current_center

    if randint(0, 250) == 0:
        spawn_mob()

    for mob in mobs[:]:
        mob.update_ai()
        if player.health <= 0:
            reset_player()

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
    sun.rotation_y += 8 * time.dt
    update_hud()


generate_world_around_player(0, 0)

player = FirstPersonController(position=(0, 8, 10), speed=6, jump_height=2, gravity=1.5)
player.cursor.visible = False
player.mouse_sensitivity = Vec2(90, 90)
player.speed = 6
player.health = 20
camera.fov = 90
mouse.locked = True

selected_text = Text(text='Block: GRASS', position=(0, 0.45), origin=(0, 0), scale=1.2, background=False)
info_text = Text(
    text='1-8 = select block   |   LMB = mine / attack   |   RMB = place\nC = craft pickaxe   |   V = craft sword   |   B = craft glass\nShift = sprint   |   Space = jump   |   G = fly   |   R = reset   |   Esc = quit',
    origin=(0, 0),
    y=0.38,
    scale=0.95,
    background=False,
)

update_hud()
app.run()
