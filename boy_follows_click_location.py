from pico2d import *
import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand = load_image('hand_arrow.png')

hand_x = random.randint(0, 1280)
hand_y = random.randint(0, 1024)

vx, vy = 0, 0

def remove_arrow(index):
    if index < len(arrows):
        del arrows[index]

def handle_events():
    global running
    global x, y, hand_x, hand_y, is_following, sprite_col, arrows, current_arrow_index

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            hand_x, hand_y = event.x, TUK_HEIGHT - 1 - event.y
            is_following = True
            arrows += [(hand_x, hand_y)]

running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
sprite_col = 0
is_following = False
arrows = []
last_arrow_x, last_arrow_y = 0, 0

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)

    if is_following and len(arrows) > 0:
        target_x, target_y = arrows[0]
        dx = target_x - x
        dy = target_y - y
        dis = math.sqrt(dx ** 2 + dy ** 2)

        if dis > 0:
            vx = dx / dis
            vy = dy / dis

        x += vx * 10
        y += vy * 10

        frame = (frame + 1) % 8

        if dx < 0:
            sprite_col = 0
        else:
            sprite_col = 1

        character.clip_draw(frame * 100, sprite_col * 100, 100, 100, x, y)

        if dis < 10:
            remove_arrow(0)

        last_arrow_x, last_arrow_y = target_x, target_y

    else :
        dx = last_arrow_x - x
        dy = last_arrow_y - y
        
        if dx < 0 :
            sprite_col = 3
        else :
            sprite_col = 2
        character.clip_draw(frame * 100, sprite_col * 100, 100, 100, x, y)

    for arrow_x, arrow_y in arrows:
        hand.draw(arrow_x, arrow_y)

    update_canvas()
    delay(0.05)
    handle_events()

close_canvas()
