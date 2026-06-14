import pygame
import sys
import datetime
import calendar
import os
import random

# Utility
# -------------------------------------------------------------------------

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Icon / object draw helpers
# -------------------------------------------------------------------------

def draw_flashlight_icon(surface, center_x, center_y, size):
    body_w, body_h = size * 0.3, size * 0.6
    pygame.draw.rect(surface, (80, 80, 80),
                     (center_x - body_w/2, center_y - body_h/3, body_w, body_h),
                     border_radius=int(size*0.05))
    pygame.draw.polygon(surface, (120, 120, 130), [
        (center_x - body_w/2, center_y - body_h/3),
        (center_x + body_w/2, center_y - body_h/3),
        (center_x + body_w/1.5, center_y - body_h/1.5),
        (center_x - body_w/1.5, center_y - body_h/1.5)
    ])
    pygame.draw.ellipse(surface, (255, 255, 200),
                        (center_x - body_w/1.5,
                         center_y - body_h/1.5 - body_w/4,
                         body_w*1.33, body_w/2))

def draw_key_icon(surface, center_x, center_y, size):
    head_r = size * 0.15
    shaft_w = size * 0.08
    shaft_h = size * 0.4
    pygame.draw.circle(surface, (255, 215, 0),
                       (int(center_x), int(center_y - shaft_h/2 - head_r/2)),
                       int(head_r), max(1, int(size*0.05)))
    pygame.draw.rect(surface, (255, 215, 0),
                     (center_x - shaft_w/2, center_y - shaft_h/2, shaft_w, shaft_h))
    pygame.draw.rect(surface, (255, 215, 0),
                     (center_x + shaft_w/2, center_y, shaft_w*1.5, shaft_w*1.5))
    pygame.draw.rect(surface, (255, 215, 0),
                     (center_x + shaft_w/2, center_y + shaft_h/2 - shaft_w*1.5, shaft_w*1.5, shaft_w*1.5))

def draw_sofa_hires(surface, sofa_rect_v):
    """Draw sofa at high resolution on screen surface (top-down view, grey, 4 cushions)"""
    SX = WINDOW_RES[0] / VIRTUAL_RES[0]
    SY = WINDOW_RES[1] / VIRTUAL_RES[1]
    x = int(sofa_rect_v.x * SX)
    y = int(sofa_rect_v.y * SY)
    w = int(sofa_rect_v.width * SX)
    h = int(sofa_rect_v.height * SY)
    
    arm_w = 22
    back_h = 22
    leg_h = 8
    inner_x = x + arm_w
    inner_w = w - arm_w * 2
    cw4 = inner_w // 4
    
    # Main body --
    pygame.draw.rect(surface, (195, 195, 205), (x, y, w, h), border_radius=5)
    
    # Back rest (top strip, facing TV) --
    pygame.draw.rect(surface, (172, 172, 182), (x, y, w, back_h), border_radius=5)
    for i in range(4):
        cx = inner_x + i * cw4
        acw = cw4 if i < 3 else inner_w - cw4 * 3
        pygame.draw.rect(surface, (155, 155, 165),
                         (cx + 2, y + 2, acw - 4, back_h - 4), border_radius=3)
        pygame.draw.rect(surface, (180, 180, 190),
                         (cx + 2, y + 2, acw - 4, back_h - 4), 1, border_radius=3)
                         
    # 4 seat cushions --
    seat_y = y + back_h
    seat_h = h - back_h - leg_h
    for i in range(4):
        cx = inner_x + i * cw4
        acw = cw4 if i < 3 else inner_w - cw4 * 3
        pygame.draw.rect(surface, (200, 200, 210),
                         (cx + 2, seat_y + 4, acw - 4, seat_h - 8), border_radius=4)
        pygame.draw.rect(surface, (225, 225, 235),
                         (cx + 2, seat_y + 4, acw - 4, seat_h - 8), 1, border_radius=4)
        pygame.draw.rect(surface, (170, 170, 180),
                         (cx + 2, seat_y + seat_h - 10, acw - 4, 5))
        if i < 3:
            pygame.draw.line(surface, (145, 145, 155),
                             (cx + acw, seat_y + 3),
                             (cx + acw, seat_y + seat_h - 3), 2)
                             
    # Left armrest --
    pygame.draw.rect(surface, (160, 160, 170), (x, y, arm_w, h - leg_h), border_radius=4)
    pygame.draw.rect(surface, (180, 180, 190), (x + 2, y + 2, arm_w - 4, h - leg_h - 4), 1, border_radius=4)
    pygame.draw.rect(surface, (130, 130, 140), (x + 2, y + h - leg_h - 10, arm_w - 4, 8))
    
    # Right armrest --
    pygame.draw.rect(surface, (160, 160, 170), (x + w - arm_w, y, arm_w, h - leg_h), border_radius=4)
    pygame.draw.rect(surface, (180, 180, 190), (x + w - arm_w + 2, y + 2, arm_w - 4, h - leg_h - 4), 1, border_radius=4)
    pygame.draw.rect(surface, (130, 130, 140), (x + w - arm_w + 2, y + h - leg_h - 10, arm_w - 4, 8))
    
    # Overall outline --
    pygame.draw.rect(surface, (35, 35, 45), (x, y, w, h - leg_h), 2, border_radius=5)
    
    # 4 legs --
    pygame.draw.rect(surface, (10, 10, 10), (x + 4, y + h - leg_h, leg_h, leg_h), border_radius=2)
    pygame.draw.rect(surface, (10, 10, 10), (x + w - leg_h - 4, y + h - leg_h, leg_h, leg_h), border_radius=2)
    pygame.draw.rect(surface, (10, 10, 10), (inner_x, y + h - leg_h, leg_h, leg_h), border_radius=2)
    pygame.draw.rect(surface, (10, 10, 10), (inner_x + inner_w - leg_h, y + h - leg_h, leg_h, leg_h), border_radius=2)

    # Decorative pillows (left side) --
    px = inner_x + 6
    py = seat_y + 5
    pygame.draw.rect(surface, (210, 198, 155), (px, py, 32, 26), border_radius=4)
    pygame.draw.rect(surface, (175, 152, 132), (px, py, 32, 26), 1, border_radius=4)
    pygame.draw.rect(surface, (160, 150, 170), (px + 10, py + 8, 30, 24), border_radius=4)
    pygame.draw.rect(surface, (140, 130, 140), (px + 10, py + 8, 30, 24), 1, border_radius=4)
    
    # Decorative blanket + pillow (right side) --
    bx = x + w - arm_w - 72
    by = seat_y + 5
    pygame.draw.rect(surface, (100, 120, 140), (bx, by, 48, 38), border_radius=3)
    pygame.draw.line(surface, (120, 140, 160), (bx, by + 10), (bx + 48, by + 10), 2)
    pygame.draw.line(surface, (120, 140, 160), (bx, by + 24), (bx + 48, by + 24), 2)
    for fi in range(6):
        fx = bx + 3 + fi * 7
        pygame.draw.line(surface, (150, 170, 190), (fx, by + 38), (fx, by + 46), 1)
    pygame.draw.rect(surface, (80, 80, 90), (bx + 16, py + 5, 28, 22), border_radius=4)
    for pi in range(3):
        pygame.draw.circle(surface, (70, 70, 80),
                           (bx + 16 + pi * 9, py + 5 + pi * 6), 2)

def draw_toilet(surface, rect):
    tank = pygame.Rect(rect.x + 2, rect.y, rect.width - 4, rect.height // 3)
    pygame.draw.rect(surface, (240, 240, 245), tank, border_radius=2)
    pygame.draw.rect(surface, (150, 150, 165), tank, 1, border_radius=2)
    bowl = pygame.Rect(rect.x, rect.y + rect.height // 3,
                       rect.width, rect.height * 2 // 3)
    pygame.draw.ellipse(surface, (240, 240, 245), bowl)
    pygame.draw.ellipse(surface, (150, 150, 165), bowl, 1)
    pygame.draw.ellipse(surface, (200, 220, 230), bowl.inflate(-8, -8))

def draw_sink(surface, rect):
    pygame.draw.rect(surface, (210, 210, 220), rect, border_radius=4)
    pygame.draw.rect(surface, (160, 160, 175), rect, 1, border_radius=4)
    basin = rect.inflate(-10, -10)
    pygame.draw.ellipse(surface, (240, 240, 250), basin)
    pygame.draw.ellipse(surface, (150, 150, 165), basin, 1)
    pygame.draw.circle(surface, (80, 80, 90), basin.center, 3)
    pygame.draw.rect(surface, (180, 180, 190),
                     (rect.centerx - 8, rect.y + 2, 16, 6), border_radius=2)
    pygame.draw.circle(surface, (250, 100, 100),
                       (rect.centerx - 5, rect.y + 5), 2)
    pygame.draw.circle(surface, (100, 100, 250),
                       (rect.centerx + 5, rect.y + 5), 2)

# Pygame Init
# -------------------------------------------------------------------------
pygame.init()
# Block mouse events to prevent event queue overflow (which silently drops KEYDOWN events)
pygame.event.set_blocked([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN,
                           pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL])

VIRTUAL_RES      = (320, 240)
VIRTUAL_RES_1080 = (1920, 1080)
WINDOW_RES       = (960, 760)
CHROMA = (3, 7, 11)                              # colorkey for hires-background overlay mode
_HIRES = (WINDOW_RES[0], WINDOW_RES[1] - 60)    # (960, 660) screen game area

screen = pygame.display.set_mode(WINDOW_RES)
pygame.display.set_caption("Retro 2D Game")
display_surface = pygame.Surface(VIRTUAL_RES).convert()
display_surface_1080 = pygame.Surface(VIRTUAL_RES_1080).convert()

BLACK           = (0, 0, 0)
MARBLE_COLOR_1  = (235, 235, 240)
MARBLE_COLOR_2  = (215, 215, 220)
PLAYER_COLOR    = (200, 50, 50)
SHADOW_COLOR    = (20, 20, 20, 100)
DESK_COLOR      = (139, 69, 19)
CABINET_COLOR   = (120, 70, 30)

# Game objects
# -------------------------------------------------------------------------
player_size = 20
player_x    = VIRTUAL_RES[0] / 2 - 50
player_y    = 150
player_speed = 2
player_dir    = "down"   # last movement direction for sprite rotation
player_moving = False    # True while movement keys are held

current_scene = "living_room"

# Perspective constants for four-wall one-point view (320×240 space)
_ROOM_VPT = 26   # top of back wall (ceiling junction)
_ROOM_VPY = 70   # bottom of back wall (floor junction)
_ROOM_LWX = 60   # left X of back wall
_ROOM_RWX = 260  # right X of back wall
_PLAYER_MIN_Y = 12   # top wall border for top-down view

# Per-room player movement bounds (virtual 320×240, player_size=20)
# (min_x, max_x, min_y, max_y)  — edit values in COLLISIONS.md then apply here
ROOM_BOUNDS = {
    "living_room": (40, 268, 75, 195),
    "bedroom":     (50, 270, 70, 195),
    "bathroom":    (70, 260, 120, 180),
}

# Living room  (top-down view, 320×240 virtual)
desk_rect           = pygame.Rect(105, 32, 120, 80)        # TV console 含植物+電視+月曆
calendar_rect       = pygame.Rect(195, 50, 14, 12)                           # 月曆圖示
tv_rect             = pygame.Rect(145, 32, 40, 35)         # 電視螢幕區域
cabinet_rect        = pygame.Rect(25, 35, 50, 70)          # 左側邊桌/抽屜
living_door_rect    = pygame.Rect(15, 120, 10, 50)         # 左牆門→臥室
sofa_rect           = pygame.Rect(90, 190, 130, 50)        # 沙發

# Bedroom (top-down view)
bedroom_door_rect   = pygame.Rect(280, 115, 18, 65)  # right wall door（下方，y=142-207）
bookshelf_rect      = pygame.Rect(20, 30, 57, 97)    # 左側書架（頂牆靠左）
computer_desk_rect  = pygame.Rect(78, 30, 139, 90)   # 電腦桌（頂牆中央）

# Bedroom new objects
bed_rect            = pygame.Rect(180, 30, 100, 90)   # 床
iron_cabinet_rect   = pygame.Rect(18, 135, 57, 85)    # 鐵櫃

# Bathroom (top-down view)
bathroom_exit_rect  = pygame.Rect(30, 77, 17, 83)    # 左牆出口門（y=77-160）
toilet_rect         = pygame.Rect(185, 70, 30, 90)   # 馬桶（中央）
sink_rect           = pygame.Rect(90, 75, 95, 85)    # 洗手台+木櫃（中左）
pipe_rect           = pygame.Rect(87, 3, 94, 37)     # 頂牆水管（正上方，y=3-40）
bathroom_door_rect  = pygame.Rect(280, 120, 10, 90)  # living room 右牆通廁所門

# Light switch on back wall, right of TV (320×240 space)
_SW_NX, _SW_NY, _SW_NW, _SW_NH = 258, 30, 11, 12

# Fonts & UI state
# -------------------------------------------------------------------------
calendar_date = datetime.date(2026, 6, 18)
prev_calendar_date = calendar_date

font               = pygame.font.SysFont("consolas", 16)
high_res_big_font  = pygame.font.SysFont("consolas", 48)
high_res_inst_font = pygame.font.SysFont("consolas", 36)
cal_header_font    = pygame.font.SysFont("consolas", 30)
cal_day_font       = pygame.font.SysFont("consolas", 24)
inv_font           = pygame.font.SysFont("consolas", 22)
cal_inst_font      = pygame.font.SysFont("consolas", 18)

ui_state          = "game"
calendar_stage    = "year" # "year" | "month" | "day"

cabinet_selection = 0
cabinet_drawer1_open = False
cabinet_drawer2_open = False
cabinet_item_pending = None  # item visible in open drawer, not yet picked up
has_flashlight    = False
has_key           = False
cabinet_message   = ""
_msg_timer        = 0    # frames until cabinet_message auto-clears
debug_rects       = False  # F1 to toggle collision rect overlay
debug_prox        = False  # F2 to toggle proximity rect overlay
inventory         = []

DATE_1988         = datetime.date(1988, 6, 22)
DATE_2026         = datetime.date(2026, 6, 22)
selected_inv_slot = -1  # -1 means no selection
last_inv_slot_key = -1  # track last pressed number key for toggle behavior
tv_channel = 0  # current TV channel selection (0=normal, 1=TETRIS)
room_lights_on    = False
# Light switch in 1920×1080 space (scaled from 320×240 _SW_N* constants)
light_switch_rect_1988 = pygame.Rect(
    int(_SW_NX * VIRTUAL_RES_1080[0] / VIRTUAL_RES[0]),
    int(_SW_NY * VIRTUAL_RES_1080[1] / VIRTUAL_RES[1]),
    max(8, int(_SW_NW * VIRTUAL_RES_1080[0] / VIRTUAL_RES[0])),
    max(10, int(_SW_NH * VIRTUAL_RES_1080[1] / VIRTUAL_RES[1]))
)
light_switch_prox = pygame.Rect(_SW_NX - 20, _SW_NY, _SW_NW + 40, 50)

# Object label & dialogue system
prompt_label      = ""
prompt_label_rect = None
dialogue_active   = False
dialogue_object   = ""
dialogue_text     = ""
dialogue_has_choices = True
dialogue_choice   = 0
dialogue_triggered = False

DIALOGUE_MAP = {
    "tv":           ("Should I turn on the TV?",                True),
    "cabinet":      ("Let me check what's in here...",          True),
    "calendar":     ("Should I try time traveling?",             True),
    "cartridge":    ("Should I take this cartridge?",           True),
    "light":        ("Should I flip the light switch?",         True),
    "bedroom":      ("Should I head to the bedroom?",           True),
    "bathroom":     ("Should I go to the bathroom?",            True),
    "frontdoor":    ("Should I inspect the front door?",        True),
    "livingroom":   ("Should I head back to the living room?",  True),
    "bookshelf":    ("These books look out of order...",        True),
    "computer":     ("Should I play some games?",               True),
    "bed":          ("Should I check out this bed?",            True),
    "iron_cabinet": ("Let me open this cabinet...",             True),
    "exit":         ("Should I head back?",                     True),
    "sink":         ("Let me take a look at this sink.",        True),
    "pipe":         ("This pipe is leaking badly...",           False),
    "ironbox":      ("Should I pick up this iron box?",         True),
    "ironbox_place":("Should I put this under the pipe?",       True),
    "ironbox_rusty":("This box is rusty... Can I open it?",     True),
    "shelf":        ("Should I inspect the shelf?",             True),
    "mirror":       ("Should I look at the mirror?",             True),
    "bathtub":      ("Should I fill the bathtub?",              True),
}

# Puzzle & Interaction States
bookshelf_order   = ["Red", "Blue", "Green"]
bookshelf_selection = 0
bookshelf_unlocked = False

iron_box_state    = 0  # 0: shelf, 1: holding, 2: under pipe, 3: rusty, 4: broken
cup_state         = 0  # 0: intact, 1: crushed
tetris_cart_spawned = False
tetris_cart_rect  = pygame.Rect(desk_rect.centerx - 7, desk_rect.y + 4, 12, 8)  # On the desk

main_door_rect    = pygame.Rect(225, 28, 52, 10)     # 主大門
door_puzzle_state = [False, False, False, False]

# Bathroom side-quest objects (2026 only)
mirror_rect       = pygame.Rect(110, 50, 63, 90)   # 鏡子（Sink 左側後牆）
bathtub_rect      = pygame.Rect(210, 70, 50, 130)  # 浴缸（右側），待 F1 校正
bathtub_state     = 0    # 0=空, 1=冷水, 2=熱水
bathtub_selection = 0    # 0=熱水, 1=冷水
mirror_breath_timer = 0  # >0 時顯示呼氣霧
mirror_fogged_in_ui = False  # True once player breathes inside mirror UI
mirror_breathed_once = False  # True once player has breathed on mirror at least once (unlocks bathtub)
# Tetris constants & state
# -------------------------------------------------------------------------
TETRIS_W = 10
TETRIS_H = 20
TETRIS_LINES_WIN = 20
TETRIS_CELL = 20

# PIECES: list of rotation states, each state = list of (col, row) offsets
TETRIS_SHAPES = [
    [[(0,1),(1,1),(2,1),(3,1)], [(1,0),(1,1),(1,2),(1,3)]], # I
    [[(0,0),(0,1),(1,0),(1,1)]], # O
    [[(0,1),(1,1),(2,1),(1,0)], [(1,0),(1,1),(1,2),(2,1)], [(0,1),(1,1),(2,1),(1,2)], [(1,0),(1,1),(1,2),(0,1)]], # T
    [[(0,1),(1,1),(2,1),(0,0)], [(1,0),(1,1),(1,2),(2,0)], [(0,1),(1,1),(2,1),(2,2)], [(1,0),(1,1),(1,2),(0,2)]], # J
    [[(0,1),(1,1),(2,1),(2,0)], [(1,0),(1,1),(1,2),(2,2)], [(0,1),(1,1),(2,1),(0,2)], [(1,0),(1,1),(1,2),(0,0)]], # L
    [[(1,1),(2,1),(0,2),(1,2)], [(1,0),(1,1),(2,1),(2,2)]], # S
    [[(0,1),(1,1),(1,2),(2,2)], [(2,0),(2,1),(1,1),(1,2)]]  # Z
]

TETRIS_COLORS = [
    (0, 220, 220), (220, 220, 0), (180, 0, 180), (0, 0, 220), 
    (220, 140, 0), (0, 220, 0), (220, 0, 0)
]

tetris_board       = None
tetris_piece_type  = 0
tetris_piece_rot   = 0
tetris_piece_x     = 0
tetris_piece_y     = 0
tetris_lines_cleared = 0
tetris_game_over   = False
tetris_won         = False
tetris_fall_time   = 0
tetris_fall_speed  = 350  # ms - starts fast (high difficulty)
tetris_just_exited = False # prevents immediate re-trigger
has_mystery_cube   = False



















# -------------------------------------------------------------------------
# Street-Fighter mini-game
# -------------------------------------------------------------------------
fighter_player_wins = 0
fighter_enemy_wins  = 0
fighter_state       = "fighting"
fighter_message     = "P1: Arrows+SPACE Attack | CPU: Zangief"

rt_p1 = {}
rt_p2 = {}

def init_rt_fighter():
    global rt_p1, rt_p2, fighter_state, fighter_message
    rt_p1 = {"x": 200, "y": 470, "vy": 0, "hp": 100, "state": "idle", "dir": 1, "atk_timer": 0, "color": (50, 100, 255)}
    rt_p2 = {"x": VIRTUAL_RES_1080[0]-200, "y": 470, "vy": 0, "hp": 100, "state": "idle", "dir": -1, "atk_timer": 0, "color": (255, 100, 50)}
    fighter_state = "fighting"
    fighter_message = "P1: Arrows+SPACE Attack | CPU: Zangief"


init_rt_fighter()

try:
    tv_image_path = get_resource_path(os.path.join("picture", "08_Back_to_Future_TV2_去背.png"))
    tv_image = pygame.image.load(tv_image_path)
except Exception as e:
    print(f"Could not load TV2 image: {e}")
    tv_image = None

try:
    tetris_tv_image = pygame.image.load(get_resource_path(os.path.join("picture", "TETRIS_TV_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load TETRIS_TV_去背.png: {e}")
    tetris_tv_image = None

tv_1988_no_remote = None
try:
    tv_1988_no_remote = pygame.image.load(get_resource_path(os.path.join("picture", "1988_黑白電視_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 1988_黑白電視_去背.png: {e}")

tv_1988_with_remote = None
try:
    tv_1988_with_remote = pygame.image.load(get_resource_path(os.path.join("picture", "1988_黑白電視_提示_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 1988_黑白電視_提示_去背.png: {e}")

try:
    sf2_icon_raw = pygame.image.load(get_resource_path(os.path.join("picture", "SF2.jpg")))
    sf2_icon = sf2_icon_raw
except Exception as e:
    print(f"Could not load SF2 icon: {e}")
    sf2_icon = None

# Scene background images and player sprite
bg_living = bg_living_orig = bg_bathroom = bg_bedroom = None
bg_1988_living = None
bg_1988_bathroom = None
bg_1988_bedroom = None
bg_time_travel = None
player_img_1988_idle = player_img_1988_walk_down = player_img_1988_walk_up = None
player_img_1988_walk_left = player_img_1988_walk_right = None
player_img_2026_idle = player_img_2026_walk_down = player_img_2026_walk_up = None
player_img_2026_walk_left = player_img_2026_walk_right = None
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "2026_客廳_T.png"))).convert()
    bg_living = pygame.transform.scale(_raw, _HIRES)
except Exception as e:
    print(f"Could not load 客廳 bg: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "2026_客廳Original_T.png"))).convert()
    bg_living_orig = pygame.transform.scale(_raw, _HIRES)
except Exception as e:
    print(f"Could not load 客廳Original bg: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "2026_廁所_T.png"))).convert()
    bg_bathroom = pygame.transform.scale(_raw, _HIRES)
except Exception as e:
    print(f"Could not load 廁所 bg: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "2026_房間_T.png"))).convert()
    bg_bedroom = pygame.transform.scale(_raw, _HIRES)
except Exception as e:
    print(f"Could not load 房間 bg: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "1988_客廳_T.png"))).convert()
    bg_1988_living = pygame.transform.scale(_raw, VIRTUAL_RES_1080)
except Exception as e:
    print(f"Could not load 1988_客廳_T.png: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "BB_Digi_去背.png"))).convert_alpha()
    player_img_1988_idle = pygame.transform.scale(_raw, (186, 186))
except Exception as e:
    print(f"Could not load BB_Digi_去背.png: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "BB_Digi_T_去背.png"))).convert_alpha()
    _walk_sq = pygame.transform.scale(_raw, (186, 186))
    player_img_1988_walk_down  = _walk_sq
    player_img_1988_walk_up    = pygame.transform.rotate(_walk_sq, 180)
    player_img_1988_walk_left  = pygame.transform.rotate(_walk_sq, -90)
    player_img_1988_walk_right = pygame.transform.rotate(_walk_sq, 90)
except Exception as e:
    print(f"Could not load BB_Digi_T_去背.png: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "BB_去背.png"))).convert_alpha()
    player_img_2026_idle = pygame.transform.scale(_raw, (267, 186))
except Exception as e:
    print(f"Could not load BB_去背.png: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "BB_T_去背.png"))).convert_alpha()
    _walk_sq = pygame.transform.scale(_raw, (186, 186))
    player_img_2026_walk_down  = _walk_sq
    player_img_2026_walk_up    = pygame.transform.rotate(_walk_sq, 180)
    player_img_2026_walk_left  = pygame.transform.rotate(_walk_sq, -90)
    player_img_2026_walk_right = pygame.transform.rotate(_walk_sq, 90)
except Exception as e:
    print(f"Could not load BB_T.png: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "Time_Travel.png"))).convert()
    bg_time_travel = pygame.transform.scale(_raw, WINDOW_RES)
except Exception as e:
    print(f"Could not load Time_Travel.png: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "1988_廁所_T.png"))).convert()
    bg_1988_bathroom = pygame.transform.scale(_raw, VIRTUAL_RES_1080)
except Exception as e:
    print(f"Could not load 1988_廁所_T.png: {e}")
mirror_img = None
try:
    mirror_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "Mirror_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load Mirror_去背.png: {e}")
mirror_clear_img = mirror_fog_img = None
try:
    mirror_clear_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "鏡子_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 鏡子_去背.png: {e}")
try:
    mirror_fog_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "鏡子_微霧_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 鏡子_微霧_去背.png: {e}")
mirror_full_fog_img = None
try:
    mirror_full_fog_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "鏡子_全霧_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 鏡子_全霧_去背.png: {e}")
cab_img_closed = cab_img_l1 = cab_img_l2 = None
cab_img_l1_empty = cab_img_l2_empty = None
for _cab_name, _cab_key in [("客廳櫃_去背.png", "closed"),
                              ("客廳櫃_L1_去背.png", "l1"),
                              ("客廳櫃_L2_去背.png", "l2"),
                              ("客廳櫃_L1_空_去背.png", "l1_empty"),
                              ("客廳櫃_L2_空_去背.png", "l2_empty")]:
    try:
        _cimg = pygame.image.load(
            get_resource_path(os.path.join("picture", _cab_name))).convert_alpha()
        if _cab_key == "closed": cab_img_closed = _cimg
        elif _cab_key == "l1":   cab_img_l1 = _cimg
        elif _cab_key == "l2":   cab_img_l2 = _cimg
        elif _cab_key == "l1_empty": cab_img_l1_empty = _cimg
        elif _cab_key == "l2_empty": cab_img_l2_empty = _cimg
    except Exception as e:
        print(f"Could not load {_cab_name}: {e}")
flashlight_img = None
try:
    flashlight_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "手電筒_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 手電筒_去背.png: {e}")
remote_img = None
try:
    remote_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "遙控器_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 遙控器_去背.png: {e}")

iron_cabinet_img = None
try:
    iron_cabinet_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "2026房間鐵櫃_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 2026房間鐵櫃_去背.png: {e}")

gashapon_img = None
try:
    gashapon_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "扭蛋機_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 扭蛋機_去背.png: {e}")
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "1988_房間_T.png"))).convert()
    bg_1988_bedroom = pygame.transform.scale(_raw, VIRTUAL_RES_1080)
except Exception as e:
    print(f"Could not load 1988_房間_T.png: {e}")

clock = pygame.time.Clock()

# Pre-allocated surfaces for 1988 dark scene (avoids per-frame 8MB+ allocations)
_dark_overlay = pygame.Surface(VIRTUAL_RES_1080, pygame.SRCALPHA)
_scaled_1988  = pygame.Surface(WINDOW_RES).convert()


def draw_cartridge_icon(surface, rect, color):
    """Draw a game cartridge icon: body + top notch + contact strip."""
    pygame.draw.rect(surface, color, rect, border_radius=3)
    pygame.draw.rect(surface, tuple(max(0, c - 50) for c in color), rect, 2, border_radius=3)
    # Top notch (connector area)
    notch_w = rect.width // 3
    notch_h = max(4, rect.height // 5)
    notch_x = rect.x + (rect.width - notch_w) // 2
    pygame.draw.rect(surface, (20, 20, 20), (notch_x, rect.y, notch_w, notch_h))
    # Contact strips at bottom
    strip_h = max(3, rect.height // 8)
    for j in range(5):
        sx = rect.x + 4 + j * (rect.width - 8) // 5
        pygame.draw.rect(surface, (200, 180, 50),
                         (sx, rect.bottom - strip_h - 2, (rect.width - 8) // 6, strip_h))

# Scene draw helpers
# -------------------------------------------------------------------------

def draw_desk_and_calendar(surface):
    global selected_inv_slot, inventory, remote_img, calendar_date, DATE_2026
    # Desk with perspective: lighter top face + darker front face
    desk_top   = pygame.Rect(desk_rect.x, desk_rect.y, desk_rect.w, 11)
    desk_front = pygame.Rect(desk_rect.x + 2, desk_rect.y + 11, desk_rect.w - 2, 7)
    pygame.draw.rect(surface, DESK_COLOR, desk_top)
    pygame.draw.rect(surface, (100, 50, 10), desk_front)
    pygame.draw.rect(surface, (70, 30, 5), desk_rect, 1)

    # Calendar icon on LEFT side of desk
    cal_x, cal_y, cal_w, cal_h = desk_rect.x + 4, desk_rect.y + 3, 14, 12
    pygame.draw.rect(surface, (250, 250, 250), (cal_x, cal_y, cal_w, cal_h))
    pygame.draw.rect(surface, (200, 50, 50), (cal_x, cal_y, cal_w, 4))
    pygame.draw.rect(surface, (20, 20, 20), (cal_x, cal_y, cal_w, cal_h), 1)
    for row in range(2):
        for col in range(3):
            pygame.draw.rect(surface, (150, 150, 150),
                             (cal_x + 2 + col * 4, cal_y + 5 + row * 4, 2, 2))

    # Tetris cartridge on desk (any year 8/8)
    if tetris_cart_spawned:
        draw_cartridge_icon(surface, tetris_cart_rect, (50, 200, 80))

    # TV on RIGHT side of desk — always shown (dark screen in non-2026, lit in 2026)
    pygame.draw.rect(surface, (28, 28, 28), tv_rect, border_radius=2)
    pygame.draw.rect(surface, (18, 18, 18), tv_rect, 1, border_radius=2)
    if calendar_date == DATE_2026:
        pygame.draw.rect(surface, (60, 80, 90),
                         (tv_rect.x + 2, tv_rect.y + 2, tv_rect.width - 4, tv_rect.height - 5))
        pygame.draw.rect(surface, (255, 50, 50),
                         (tv_rect.right - 4, tv_rect.bottom - 3, 2, 2))

        # Show remote control next to TV if player selected it (in inventory)
        selected_remote = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Remote"
        if selected_remote and remote_img:
            # Draw remote next to TV in virtual coordinates
            _rx = tv_rect.right + 8
            _ry = tv_rect.centery - 3
            _rw, _rh = 6, 6
            try:
                _remote_scaled = pygame.transform.scale(remote_img, (_rw, _rh))
                surface.blit(_remote_scaled, (_rx, _ry))
            except:
                # Fallback: draw simple rectangle if image fails
                pygame.draw.rect(surface, (100, 100, 150), (_rx, _ry, _rw, _rh))
    else:
        pygame.draw.rect(surface, (20, 22, 25),
                         (tv_rect.x + 2, tv_rect.y + 2, tv_rect.width - 4, tv_rect.height - 5))

def draw_grid_calendar_ui(surface, date):
    """Three-stage calendar rendering..."""
    if bg_time_travel:
        surface.blit(bg_time_travel, (0, 0))
    else:
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))

    cal_w, cal_h = 500, 510
    cal_x = (WINDOW_RES[0] - cal_w) // 2
    cal_y = (WINDOW_RES[1] - cal_h) // 2
    _cal_cx = cal_x + cal_w // 2

    pygame.draw.rect(surface, (22, 22, 22), (cal_x, cal_y, cal_w, cal_h), border_radius=12)
    pygame.draw.rect(surface, (200, 50, 50), (cal_x, cal_y, cal_w, 60), border_radius=12)

    # Stage breadcrumb
    stage_labels = [("year", "Year"), ("month", "Month"), ("day", "Day")]
    sx = cal_x + 20
    for i, (key, label) in enumerate(stage_labels):
        active = (calendar_stage == key)
        col = (255, 255, 255) if active else (80, 130, 80)
        arr = cal_day_font.render(label, True, col)
        surface.blit(arr, (sx, cal_y + 15))
        sx += arr.get_width()
        if key != "day":
            arr = cal_day_font.render(" > ", True, (60, 100, 60))
            surface.blit(arr, (sx, cal_y + 15))
            sx += arr.get_width()

    pygame.draw.line(surface, (0, 140, 0), (cal_x, cal_y + 60), (cal_x + cal_w, cal_y + 60), 2)

    if calendar_stage == "year":
        # Large year number
        yr_big = high_res_big_font.render(str(date.year), True, (255, 255, 100))
        surface.blit(yr_big, yr_big.get_rect(center=(_cal_cx, cal_y + 210)))
        # Decade label
        dec = cal_header_font.render(f"{date.year // 10 * 10}s", True, (150, 200, 150))
        surface.blit(dec, dec.get_rect(center=(_cal_cx, cal_y + 100)))
        inst = "Up/Dn: +/- 10YR   Lt/Rt: +/- 1YR   SPACE: Confirm   ESC: Close"

    elif calendar_stage == "month":
        yr = high_res_inst_font.render(str(date.year), True, (200, 200, 100))
        surface.blit(yr, yr.get_rect(center=(_cal_cx, cal_y + 85)))
        month_short = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        mw, mh = 120, 50
        mx0 = cal_x + (cal_w - 4*mw) // 2
        my0 = cal_y + 120
        for i, mname in enumerate(month_short):
            row = i // 4
            col = i % 4
            mx = mx0 + col * mw
            my = my0 + row * mh
            sel = (date.month == i + 1)
            bg = (50, 120, 50) if sel else (30, 40, 30)
            pygame.draw.rect(surface, bg, (mx, my, mw - 4, mh - 4), border_radius=4)
            pygame.draw.rect(surface, (0, 180, 0), (mx, my, mw - 4, mh - 4), 1, border_radius=4)
            mc = (255, 255, 255) if sel else (175, 175, 175)
            m_txt = cal_day_font.render(mname, True, mc)
            surface.blit(m_txt, m_txt.get_rect(center=(mx + mw//2, my + mh//2)))
        inst = "Left/Right: Change Month   SPACE: Confirm   ESC: Back"

    else: # "day"
        month_names_full = ["January", "February", "March", "April", "May", "June",
                            "July", "August", "September", "October", "November", "December"]
        hdr = cal_header_font.render(
            f"{month_names_full[date.month-1]} {date.year}", True, (255, 255, 100))
        surface.blit(hdr, hdr.get_rect(center=(_cal_cx, cal_y + 75)))
        pygame.draw.line(surface, (0, 140, 0), (cal_x+20, cal_y+100), (cal_x+cal_w-20, cal_y+100), 1)

        dow_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        cell_w = cal_w / 7
        cell_h = (cal_h - 150) / 6
        for i, lbl in enumerate(dow_labels):
            color = (255, 110, 110) if i == 0 else (170, 220, 170)
            s = cal_day_font.render(lbl, True, color)
            surface.blit(s, (cal_x + i*cell_w + (cell_w - s.get_width())/2, cal_y + 118))
        pygame.draw.line(surface, (0, 100, 0), (cal_x+20, cal_y+134), (cal_x+cal_w-20, cal_y+134), 1)

        first_day = datetime.date(date.year, date.month, 1)
        first_weekday = (first_day.weekday() + 1) % 7
        days_in_month = calendar.monthrange(date.year, date.month)[1]
        
        for day in range(1, days_in_month + 1):
            idx = first_weekday + day - 1
            row = idx // 7
            col = idx % 7
            cx = cal_x + col * cell_w
            cy = cal_y + 150 + row * cell_h
            if day == date.day:
                pygame.draw.rect(surface, (210, 185, 0),
                                 (cx + 4, cy + 4, cell_w - 8, cell_h - 8), border_radius=6)
                day_color = (0, 0, 0)
            else:
                day_color = (255, 170, 170) if col == 0 else (175, 255, 175)
            ds = cal_day_font.render(str(day), True, day_color)
            surface.blit(ds, ds.get_rect(center=(cx + cell_w/2, cy + cell_h/2)))

        inst = "Arrows: Move   SPACE: Confirm Date   ESC: Back to Month"

    is_ = cal_inst_font.render(inst, True, (150, 175, 150))
    surface.blit(is_, is_.get_rect(center=(_cal_cx, cal_y + cal_h - 16)))

# Mystery Cube Icon
# -------------------------------------------------------------------------
def draw_mystery_cube_icon(surface, cx, cy, size):
    """Isometric mystery cube with rune symbols."""
    s = size / 2
    # Shadow
    pygame.draw.ellipse(surface, (20, 20, 30, 100), (cx - s, cy + s/2, size, s))
    # Front face
    pygame.draw.rect(surface, (40, 20, 60), (cx - s, cy - s/2, size, size))
    # Top face
    pygame.draw.polygon(surface, (65, 35, 95), [
        (cx - s, cy - s/2),
        (cx, cy - s),
        (cx + s, cy - s/2),
        (cx, cy)
    ])
    # Right face
    pygame.draw.polygon(surface, (28, 12, 42), [
        (cx, cy),
        (cx + s, cy - s/2),
        (cx + s, cy + s/2),
        (cx, cy + s)
    ])
    # Rune on front face
    rc = (180, 100, 255)
    pygame.draw.line(surface, rc, (cx - s/2, cy), (cx - s/4, cy - s/4), 2)
    pygame.draw.line(surface, rc, (cx - s/4, cy - s/4), (cx - s/2, cy + s/4), 2)
    pygame.draw.line(surface, rc, (cx - s/2, cy + s/4), (cx - s/4, cy + s/4), 2)
    # Outline
    pygame.draw.rect(surface, (100, 50, 150), (cx - s, cy - s/2, size, size), 1)

# Tetris helpers
# -------------------------------------------------------------------------

def tetris_get_cells(ptype, rot, px, py):
    shape = TETRIS_SHAPES[ptype][rot % len(TETRIS_SHAPES[ptype])]
    return [(px + cx, py + cy) for cx, cy in shape]

def tetris_valid(board, ptype, rot, px, py):
    for cx, cy in tetris_get_cells(ptype, rot, px, py):
        if cx < 0 or cx >= TETRIS_W or cy >= TETRIS_H:
            return False
        if cy >= 0 and board[cy][cx] is not None:
            return False
    return True

def tetris_place(board, ptype, rot, px, py):
    color = TETRIS_COLORS[ptype]
    for cx, cy in tetris_get_cells(ptype, rot, px, py):
        if 0 <= cy < TETRIS_H and 0 <= cx < TETRIS_W:
            board[cy][cx] = color

def tetris_clear_lines(board):
    new_board = [row for row in board if any(c is None for c in row)]
    cleared = TETRIS_H - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, [None] * TETRIS_W)
    return new_board, cleared

def init_tetris():
    global tetris_board, tetris_piece_type, tetris_piece_rot
    global tetris_piece_x, tetris_piece_y, tetris_next_type
    global tetris_lines_cleared, tetris_game_over, tetris_won
    global tetris_fall_time, tetris_fall_speed, tetris_just_exited
    tetris_board = [[None]*TETRIS_W for _ in range(TETRIS_H)]
    tetris_piece_type = random.randint(0, len(TETRIS_SHAPES)-1)
    tetris_next_type = random.randint(0, len(TETRIS_SHAPES)-1)
    tetris_piece_rot = 0
    tetris_piece_x = TETRIS_W // 2 - 2
    tetris_piece_y = 0
    tetris_lines_cleared = 0
    tetris_game_over = False
    tetris_won = False
    tetris_fall_speed = 350
    tetris_fall_time = pygame.time.get_ticks()
    tetris_just_exited = False

def draw_tetris_ui(surface):
    """Render the full Tetris game screen."""
    C = TETRIS_CELL
    BX = (WINDOW_RES[0] - TETRIS_W * C) // 2 - 80
    BY = (WINDOW_RES[1] - TETRIS_H * C) // 2

    # Board background + grid
    pygame.draw.rect(surface, (10, 10, 32), (BX, BY, TETRIS_W*C, TETRIS_H*C))
    for gx in range(TETRIS_W + 1):
        pygame.draw.line(surface, (20, 20, 40), (BX + gx*C, BY), (BX + gx*C, BY + TETRIS_H*C))
    for gy in range(TETRIS_H + 1):
        pygame.draw.line(surface, (20, 20, 40), (BX, BY + gy*C), (BX + TETRIS_W*C, BY + gy*C))
    pygame.draw.rect(surface, (60, 60, 100), (BX, BY, TETRIS_W*C, TETRIS_H*C), 2)

    # Placed cells
    for cy in range(TETRIS_H):
        for cx in range(TETRIS_W):
            if tetris_board[cy][cx]:
                pygame.draw.rect(surface, tetris_board[cy][cx], (BX+cx*C+1, BY+cy*C+1, C-2, C-2))
                pygame.draw.rect(surface, (255, 255, 255), (BX+cx*C+1, BY+cy*C+1, C-2, C-2), 1)

    # Ghost piece
    if not tetris_game_over and not tetris_won:
        gy_ghost = tetris_piece_y
        while tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, gy_ghost+1):
            gy_ghost += 1
        ghost_col = tuple(c//5 for c in TETRIS_COLORS[tetris_piece_type])
        for gx, gy in tetris_get_cells(tetris_piece_type, tetris_piece_rot, tetris_piece_x, gy_ghost):
            if gy >= 0:
                pygame.draw.rect(surface, ghost_col, (BX+gx*C+1, BY+gy*C+1, C-2, C-2))
                pygame.draw.rect(surface, (50, 50, 50), (BX+gx*C+1, BY+gy*C+1, C-2, C-2), 1)

        # Active piece
        col = TETRIS_COLORS[tetris_piece_type]
        for gx, gy in tetris_get_cells(tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y):
            if gy >= 0:
                pygame.draw.rect(surface, col, (BX+gx*C+1, BY+gy*C+1, C-2, C-2))
                pygame.draw.rect(surface, (255, 255, 255), (BX+gx*C+1, BY+gy*C+1, C-2, C-2), 1)

    # Side panel
    PX = BX + TETRIS_W * C + 24
    PY = BY
    sf = pygame.font.SysFont("consolas", 32)
    cf = pygame.font.SysFont("consolas", 24)

    # Title
    title = high_res_big_font.render("TETRIS", True, (255, 50, 50))
    surface.blit(title, title.get_rect(center=(PX + 80, PY - 45)))

    # Progress
    surface.blit(sf.render(f"{tetris_lines_cleared}/{TETRIS_LINES_WIN}", True, (200, 200, 255)), (PX, PY+10))
    bar_w = 180
    pygame.draw.rect(surface, (50, 50, 50), (PX, PY+45, bar_w, 14))
    prog = min(1.0, tetris_lines_cleared / max(1, TETRIS_LINES_WIN))
    pygame.draw.rect(surface, (100, 250, 100), (PX, PY+45, int(bar_w*prog), 14))
    pygame.draw.rect(surface, (80, 80, 120), (PX, PY+45, bar_w, 14), 2)

    # Next piece
    surface.blit(sf.render("NEXT:", True, (200, 200, 200)), (PX, PY+72))
    pygame.draw.rect(surface, (20, 20, 40), (PX, PY+105, 4*C, 4*C))
    for gx, gy in tetris_get_cells(tetris_next_type, 0, 0, 0):
        pygame.draw.rect(surface, TETRIS_COLORS[tetris_next_type], (PX+gx*C+16, PY+105+gy*C+16, C-2, C-2))

    # Controls
    for i, txt in enumerate(["L/R: Move", "Up: Rotate", "Dn: Soft Drop", "SPACE: Hard Drop", "ESC: Exit"]):
        surface.blit(cf.render(txt, True, (130, 130, 130)), (PX, PY+200+i*28))

    # Speed indicator
    spd_pct = max(0, 100 - int((tetris_fall_speed - 80) / 2.7))
    surface.blit(cf.render(f"Speed: {spd_pct}%", True, (200, 100, 100)), (PX, PY+360))

    # Overlay messages
    if tetris_game_over:
        ov = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        ov.fill((0, 0, 0, 180))
        surface.blit(ov, (0, 0))
        surface.blit(high_res_big_font.render("GAME OVER", True, (255, 50, 50)),
                     high_res_big_font.render("GAME OVER", True, (255, 50, 50)).get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2-50)))
        surface.blit(high_res_inst_font.render("SPACE to Restart, ESC to Exit", True, (200, 200, 200)),
                     high_res_inst_font.render("SPACE to Restart, ESC to Exit", True, (200, 200, 200)).get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2+20)))

    elif tetris_won:
        ov = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        ov.fill((0, 0, 0, 160))
        surface.blit(ov, (0, 0))
        surface.blit(high_res_big_font.render("YOU WIN!", True, (255, 255, 0)),
                     high_res_big_font.render("YOU WIN!", True, (255, 255, 0)).get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2-50)))
        surface.blit(high_res_inst_font.render("Mystery Cube obtained! ESC to exit.", True, (200, 255, 200)),
                     high_res_inst_font.render("Mystery Cube obtained! ESC to exit.", True, (200, 255, 200)).get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2+20)))
        draw_mystery_cube_icon(surface, WINDOW_RES[0]//2, WINDOW_RES[1]//2 - 120, 60)

def draw_retro_player(surface, x, y):
    """Fat guy with full black hair, glasses, and visible belly."""
    # Shadow
    pygame.draw.ellipse(surface, (10, 80, 10), (x - 4, y + player_size - 1, player_size + 8, 6))
    
    # Legs (dark blue jeans)
    pygame.draw.rect(surface, (35, 45, 100), (x + 2, y + 13, 7, 7))
    pygame.draw.rect(surface, (35, 45, 100), (x + 11, y + 13, 7, 7))
    # Shoes
    pygame.draw.rect(surface, (25, 15, 8), (x, y + 18, 9, 4))
    pygame.draw.rect(surface, (25, 15, 8), (x + 11, y + 18, 9, 4))
    
    # Belly (skin color, big round, sticking out below shirt)
    pygame.draw.ellipse(surface, (220, 155, 105), (x - 4, y + 9, 28, 11))
    # Belly button
    pygame.draw.circle(surface, (250, 200, 150), (x + 10, y + 14), 1)
    
    # Shirt (short - only upper torso, blue)
    pygame.draw.ellipse(surface, (80, 120, 200), (x - 2, y + 5, 24, 8))
    # Shirt line
    pygame.draw.line(surface, (60, 95, 170), (x + 10, y + 6), (x + 10, y + 11), 1)
    
    # Arms (short fat, at shirt level)
    pygame.draw.ellipse(surface, (80, 120, 200), (x - 5, y + 6, 6, 5))
    pygame.draw.ellipse(surface, (80, 120, 200), (x + 19, y + 6, 6, 5))
    # Hands
    pygame.draw.circle(surface, (255, 200, 150), (x - 3, y + 11), 3)
    pygame.draw.circle(surface, (255, 200, 150), (x + 22, y + 11), 3)
    
    # Head (big round, skin)
    pygame.draw.ellipse(surface, (255, 200, 150), (x + 3, y - 5, 14, 14))
    
    # Full black hair (complete coverage, not sparse)
    pygame.draw.ellipse(surface, (22, 15, 6), (x + 2, y - 6, 16, 10))  # top dome
    pygame.draw.rect(surface, (22, 15, 6), (x + 2, y - 2, 16, 5))     # fill sides
    pygame.draw.rect(surface, (22, 15, 6), (x + 2, y - 2, 4, 7))      # left side hair
    pygame.draw.rect(surface, (22, 15, 6), (x + 14, y - 2, 4, 7))     # right side hair
    
    # Glasses - left lens (thick black frame)
    pygame.draw.rect(surface, (22, 22, 22), (x + 4, y + 1, 6, 5), 1)
    pygame.draw.rect(surface, (200, 230, 255), (x + 5, y + 2, 4, 3))
    # Glasses - right lens
    pygame.draw.rect(surface, (22, 22, 22), (x + 11, y + 1, 6, 5), 1)
    pygame.draw.rect(surface, (200, 230, 255), (x + 12, y + 2, 4, 3))
    # Bridge
    pygame.draw.line(surface, (22, 22, 22), (x + 9, y + 3), (x + 11, y + 3), 1)
    # Temples
    pygame.draw.line(surface, (22, 22, 22), (x + 3, y + 4), (x + 4, y + 3), 1)
    pygame.draw.line(surface, (22, 22, 22), (x + 17, y + 4), (x + 19, y + 3), 1)
    
    # Nose
    pygame.draw.rect(surface, (220, 160, 110), (x + 10, y + 7, 1, 2))
    
    # Mouth (smile)
    pygame.draw.rect(surface, (180, 100, 80), (x + 8, y + 10, 5, 1))

def draw_retro_player_hires(surface, vx, vy):
    """High-res fat guy drawn directly on screen surface (3x scale)."""
    SX = WINDOW_RES[0] / VIRTUAL_RES[0]
    SY = WINDOW_RES[1] / VIRTUAL_RES[1]
    cx = int(vx * SX + (player_size / 2) * SX)
    cy = int(vy * SY + (player_size / 2) * SY)

    # Shadow
    pygame.draw.ellipse(surface, (10, 80, 10), (cx - 18, cy + 26, 52, 14))

    # Shoes
    pygame.draw.ellipse(surface, (25, 15, 8), (cx - 14, cy + 22, 22, 10))
    pygame.draw.ellipse(surface, (25, 15, 8), (cx + 3, cy + 22, 22, 10))
    
    # Legs (dark blue jeans)
    pygame.draw.rect(surface, (35, 45, 100), (cx - 10, cy + 8, 16, 18))
    pygame.draw.rect(surface, (35, 45, 100), (cx + 6, cy + 8, 16, 18))
    
    # Belly (skin, big round, sticking out below shirt)
    pygame.draw.ellipse(surface, (220, 155, 105), (cx - 26, cy - 2, 52, 24))
    pygame.draw.ellipse(surface, (255, 200, 150), (cx - 24, cy, 48, 20))
    # Belly button
    pygame.draw.circle(surface, (250, 200, 150), (cx, cy + 13), 3)

    # Shirt (short, blue, only upper torso)
    pygame.draw.ellipse(surface, (80, 120, 200), (cx - 22, cy - 16, 44, 24))
    # Shirt line
    pygame.draw.line(surface, (60, 95, 170), (cx, cy - 14), (cx, cy + 6), 2)
    
    # Arms
    pygame.draw.ellipse(surface, (80, 120, 200), (cx - 30, cy - 14, 16, 12))
    pygame.draw.ellipse(surface, (80, 120, 200), (cx + 14, cy - 14, 16, 12))
    # Hands
    pygame.draw.circle(surface, (255, 200, 150), (cx - 24, cy - 2), 6)
    pygame.draw.circle(surface, (255, 200, 150), (cx + 24, cy - 2), 6)

    # Head
    pygame.draw.ellipse(surface, (255, 200, 150), (cx - 20, cy - 40, 40, 40))
    
    # Hair
    pygame.draw.ellipse(surface, (22, 15, 6), (cx - 22, cy - 44, 44, 22))
    pygame.draw.rect(surface, (22, 15, 6), (cx - 22, cy - 32, 44, 14))
    pygame.draw.rect(surface, (22, 15, 6), (cx - 22, cy - 32, 12, 20))
    pygame.draw.rect(surface, (22, 15, 6), (cx + 10, cy - 32, 12, 20))

    # Glasses - left
    pygame.draw.rect(surface, (22, 22, 22), (cx - 16, cy - 28, 16, 12), 2)
    pygame.draw.rect(surface, (200, 230, 255), (cx - 14, cy - 26, 12, 8))
    # Glasses - right
    pygame.draw.rect(surface, (22, 22, 22), (cx + 2, cy - 28, 16, 12), 2)
    pygame.draw.rect(surface, (200, 230, 255), (cx + 4, cy - 26, 12, 8))
    # Bridge
    pygame.draw.line(surface, (22, 22, 22), (cx - 2, cy - 22), (cx + 2, cy - 22), 2)
    # Temples
    pygame.draw.line(surface, (22, 22, 22), (cx - 20, cy - 24), (cx - 16, cy - 24), 2)
    pygame.draw.line(surface, (22, 22, 22), (cx + 18, cy - 24), (cx + 22, cy - 24), 2)
    
    # Nose
    pygame.draw.rect(surface, (220, 160, 110), (cx - 2, cy - 14, 4, 6))
    
    # Mouth (smile)
    pygame.draw.rect(surface, (180, 100, 80), (cx - 6, cy - 4, 12, 2))

def draw_fighter(surface, center_x, center_y, is_player, action, hp):
    color = (50, 150, 255) if is_player else (255, 100, 50)
    if hp <= 0:
        color = (100, 100, 100)
    
    eye_dir = 1 if is_player else -1
    if action == "hurt":
        eye_dir *= -1
    
    body_rect = pygame.Rect(center_x - 20, center_y - 40, 40, 80)
    
    if action == "idle":
        pygame.draw.rect(surface, color, body_rect, border_radius=5)
        pygame.draw.circle(surface, (255, 150, 150), (center_x, center_y - 60), 20)
        pygame.draw.circle(surface, (0, 0, 0), (center_x + eye_dir * 8, center_y - 65), 4)
        pygame.draw.rect(surface, color, (center_x - 30, center_y - 40, 12, 40))
        pygame.draw.rect(surface, color, (center_x + 18, center_y - 40, 12, 40))
    
    elif action == "punch":
        pygame.draw.rect(surface, color, body_rect, border_radius=5)
        pygame.draw.circle(surface, (255, 150, 150), (center_x + eye_dir * 10, center_y - 60), 20)
        pygame.draw.circle(surface, (0, 0, 0), (center_x + eye_dir * 18, center_y - 65), 4)
        pygame.draw.rect(surface, color, (center_x - 10, center_y - 30, 50 * eye_dir, 15))
        pygame.draw.rect(surface, color, (center_x - 15, center_y - 40, 12, 40))
        
    elif action == "kick":
        pygame.draw.rect(surface, color, (center_x - 15, center_y - 40, 30, 80), border_radius=5)
        pygame.draw.circle(surface, (255, 150, 150), (center_x, center_y - 60), 20)
        pygame.draw.circle(surface, (0, 0, 0), (center_x + eye_dir * 8, center_y - 65), 4)
        pygame.draw.rect(surface, color, (center_x - 15, center_y + 10, 40 * eye_dir, 15))
    
    elif action == "block":
        pygame.draw.rect(surface, color, body_rect, border_radius=5)
        pygame.draw.circle(surface, (255, 150, 150), (center_x - eye_dir * 5, center_y - 55), 20)
        pygame.draw.circle(surface, (0, 0, 0), (center_x, center_y - 60), 4)
        pygame.draw.rect(surface, color, (center_x + eye_dir * 15, center_y - 50, 15, 40))
        
    else: # hurt
        pygame.draw.rect(surface, color, (center_x - 20, center_y - 30, 40, 70), border_radius=5)
        pygame.draw.circle(surface, (255, 150, 150), (center_x - eye_dir * 10, center_y - 50), 20)
        pygame.draw.circle(surface, (0, 0, 0), (center_x - eye_dir * 5, center_y - 55), 4)

def draw_zangief(surface, x, y, direction, state, hp, invul_timer):
    if invul_timer % 4 > 1:
        return
    skin = (255, 180, 140) if hp > 0 else (150, 150, 150)
    scar = (200, 100, 100) if hp > 0 else (100, 100, 100)
    under = (200, 30, 30) if hp > 0 else (100, 50, 50)
    boots = (150, 40, 40) if hp > 0 else (80, 80, 80)
    hair = (80, 40, 20)
    
    # Body (massive)
    pygame.draw.rect(surface, skin, (x - 30, y - 50, 60, 50), border_radius=10)
    pygame.draw.rect(surface, under, (x - 20, y, 40, 20), border_radius=5)
    
    # Legs & Boots
    pygame.draw.rect(surface, skin, (x - 25, y + 20, 15, 20))
    pygame.draw.rect(surface, skin, (x + 10, y + 20, 15, 20))
    pygame.draw.rect(surface, boots, (x - 30, y + 40, 25, 25))
    pygame.draw.rect(surface, boots, (x + 5, y + 40, 25, 25))
    
    # ...fighter rendering ends around here...
    
    # Head & Face
    pygame.draw.circle(surface, skin, (x, y - 60), 20)
    pygame.draw.rect(surface, hair, (x - 15, y - 80, 30, 10))
    pygame.draw.rect(surface, hair, (x - 20, y - 75, 5, 20))
    pygame.draw.rect(surface, hair, (x + 15, y - 75, 5, 20))
    pygame.draw.line(surface, scar, (x - 10, y - 55), (x + 10, y - 65), 2)
    pygame.draw.line(surface, scar, (x + 10, y - 55), (x - 10, y - 65), 2)
    # Beard
    pygame.draw.circle(surface, hair, (x, y - 45), 12)
    pygame.draw.rect(surface, hair, (x - 12, y - 55, 24, 15))
    if direction == 1:
        pygame.draw.rect(surface, hair, (x + 25, y - 10, 10, 8))
    else:
        pygame.draw.rect(surface, hair, (x - 35, y - 10, 10, 8))
        
    eye_x = x + 8 if direction == 1 else x - 8
    pygame.draw.circle(surface, (255, 255, 255), (eye_x, y - 60), 8)
    pygame.draw.circle(surface, (0, 0, 0), (eye_x + (4 if direction == 1 else -4), y - 60), 4)
    
    if state == "attacking":
        pygame.draw.rect(surface, skin, (x - 40, y - 45, 30, 15))
        pygame.draw.rect(surface, skin, (x + 10, y - 45, 30, 15))
    else:
        pygame.draw.rect(surface, skin, (x - 35, y - 15, 15, 30))
        pygame.draw.rect(surface, skin, (x + 20, y - 15, 15, 30))

# 1988 low-res dark-scene renderer (all rooms)
# -------------------------------------------------------------------------

def render_1988_scene(px_v, py_v, pS_v, flashlight_active):
    V = VIRTUAL_RES_1080
    ds = display_surface_1080

    # Draw full 16bit scene at low-res first
    if current_scene == "living_room":
        ds.blit(bg_1988_living, (0, 0))

    elif current_scene == "bedroom":
        ds.blit(bg_1988_bedroom, (0, 0))

    elif current_scene == "bathroom":
        ds.blit(bg_1988_bathroom, (0, 0))
        # Iron box state drawing on top of background
        tx = toilet_rect.x * V[0] // VIRTUAL_RES[0]
        ty = toilet_rect.y * V[1] // VIRTUAL_RES[1]
        tw = max(1, toilet_rect.width * V[0] // VIRTUAL_RES[0])
        th = max(1, toilet_rect.height * V[1] // VIRTUAL_RES[1])
        if iron_box_state == 0:
            pygame.draw.rect(ds, (160, 140, 110), (tx + 2, ty + 2, max(4, tw // 2), max(4, th // 2)))
            pygame.draw.rect(ds, (100, 80, 60), (tx + 2, ty + 2, max(4, tw // 2), max(4, th // 2)), 1)
        elif iron_box_state == 1:
            pygame.draw.rect(ds, (160, 140, 110), (px_v + 6, py_v - 4, 6, 5))
        elif iron_box_state == 2:
            pygame.draw.rect(ds, (150, 130, 100), (ppx - 2, ppy + pph + 2, ppw + 4, 6))
            pygame.draw.rect(ds, (100, 80, 60), (ppx - 2, ppy + pph + 2, ppw + 4, 6), 1)


    # Only apply darkness overlay when lights are OFF
    if not room_lights_on:
        # Reuse pre-allocated surface — avoid 8MB allocation per frame
        _dark_overlay.fill((0, 0, 0, 250))

        if flashlight_active:
            fl_radius = 300
            for r in range(fl_radius, -1, -5):  # step 5 (was 3): ~40% fewer iterations
                progress = r / fl_radius
                a = int(250 * (progress ** 0.5))
                pygame.draw.circle(_dark_overlay, (0, 0, 0, a), (px_v, py_v), r)
        else:
            amb_r = 40
            for r in range(amb_r, -1, -2):  # step 2 (was 1): half iterations
                progress = r / amb_r
                a = int(250 * (progress ** 0.4))
                pygame.draw.circle(_dark_overlay, (0, 0, 0, a), (px_v, py_v), r)

        # Calendar glow — use draw.circle instead of slow get_at/set_at pixel loop
        if current_scene == "living_room":
            gcx = desk_rect.x * V[0] // VIRTUAL_RES[0] + desk_rect.width * V[0] // VIRTUAL_RES[0] // 2
            gcy = desk_rect.y * V[1] // VIRTUAL_RES[1] + desk_rect.height * V[1] // VIRTUAL_RES[1] // 2
            pygame.draw.circle(_dark_overlay, (0, 0, 0, 150), (gcx, gcy), 12)

        ds.blit(_dark_overlay, (0, 0))
    # else: room_lights_on == True -> no darkness, full scene visible


    # Reuse pre-allocated output surface — avoid per-frame 960×720 allocation
    pygame.transform.scale(ds, WINDOW_RES, _scaled_1988)
    return _scaled_1988

# Object label & dialogue helpers
# -------------------------------------------------------------------------

def _do_proximity_check():
    """Set prompt_label/prompt_label_rect based on player position each frame."""
    global prompt_label, prompt_label_rect
    prompt_label = ""
    prompt_label_rect = None
    if ui_state != "game" or dialogue_active:
        return
    if current_scene == "living_room":
        # In 1988 without lights, restrict interactions
        is_1988_dark = calendar_date == DATE_1988 and not room_lights_on
        # Must select flashlight in inventory to use light switch
        has_flashlight_selected = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Flashlight"

        if tetris_cart_spawned and player_rect.colliderect(calendar_proximity_rect):
            prompt_label = "Cartridge"
            prompt_label_rect = calendar_rect
        elif player_rect.colliderect(calendar_proximity_rect):
            prompt_label = "Calendar"
            prompt_label_rect = calendar_rect
        elif is_1988_dark:
            # In 1988 dark: only allow light switch if flashlight is selected in inventory
            if has_flashlight_selected and player_rect.colliderect(light_switch_prox):
                prompt_label = "Light"
                prompt_label_rect = light_switch_prox
            # If dark without selected flashlight, no other interactions allowed
        elif calendar_date in (DATE_1988, DATE_2026):
            if player_rect.colliderect(living_door_prox):
                prompt_label = "Bedroom"
                prompt_label_rect = living_door_rect
            elif player_rect.colliderect(bathroom_door_prox):
                prompt_label = "Bathroom"
                prompt_label_rect = bathroom_door_rect
            elif player_rect.colliderect(tv_proximity_rect):
                prompt_label = "TV"
                prompt_label_rect = tv_rect
            elif player_rect.colliderect(cabinet_proximity_rect):
                prompt_label = "Cabinet"
                prompt_label_rect = cabinet_rect
            elif calendar_date == DATE_2026:
                if player_rect.colliderect(main_door_rect.inflate(5, 100)):
                    prompt_label = "Front Door"
                    prompt_label_rect = main_door_rect
    elif current_scene == "bedroom":
        if player_rect.colliderect(bedroom_door_prox):
            prompt_label = "Living Room"
            prompt_label_rect = bedroom_door_rect
        elif player_rect.colliderect(bookshelf_prox):
            prompt_label = "Bookshelf"
            prompt_label_rect = bookshelf_rect
        elif player_rect.colliderect(computer_prox):
            prompt_label = "Computer"
            prompt_label_rect = computer_desk_rect
        elif player_rect.colliderect(bed_rect.inflate(16, 16)):
            prompt_label = "Bed"
            prompt_label_rect = bed_rect
        elif player_rect.colliderect(iron_cabinet_rect.inflate(16, 16)):
            prompt_label = "Iron Cabinet"
            prompt_label_rect = iron_cabinet_rect
    elif current_scene == "bathroom":
        if player_rect.colliderect(bathroom_exit_prox):
            prompt_label = "Exit"
            prompt_label_rect = bathroom_exit_rect
        elif (calendar_date != DATE_1988 and
              player_rect.colliderect(mirror_rect.inflate(24, 80))):
            prompt_label = "Mirror"
            prompt_label_rect = mirror_rect
        elif (calendar_date != DATE_1988 and mirror_breathed_once and
              player_rect.colliderect(bathtub_rect.inflate(16, 16))):
            prompt_label = "Bathtub"
            prompt_label_rect = bathtub_rect
        elif player_rect.colliderect(pipe_rect.inflate(12, 12)):
            prompt_label = "Pipe"
            prompt_label_rect = pipe_rect


def _draw_label(surface):
    """Render short object name above (or below if near top) its rect in window coords."""
    if not prompt_label or not prompt_label_rect:
        return
    _SX = WINDOW_RES[0] / VIRTUAL_RES[0]
    _SY = (WINDOW_RES[1] - 60) / VIRTUAL_RES[1]
    lx = int(prompt_label_rect.centerx * _SX)
    txt = cal_day_font.render(prompt_label, True, (255, 255, 255))
    _half_w = txt.get_width() // 2 + 6
    lx = max(_half_w, min(WINDOW_RES[0] - _half_w, lx))
    _th = txt.get_height()
    _obj_top_px = int(prompt_label_rect.top * _SY)
    _obj_bot_px = int(prompt_label_rect.bottom * _SY)
    if _obj_top_px < _th + 10:
        # Object is near top — show label BELOW the object
        ly = _obj_bot_px + _th + 6
    else:
        ly = max(_th + 4, _obj_top_px - 6)
    bg = pygame.Surface((txt.get_width() + 8, _th + 4), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 160))
    surface.blit(bg, bg.get_rect(midbottom=(lx, ly)))
    surface.blit(txt, txt.get_rect(midbottom=(lx, ly - 2)))


def _cab_current_img():
    """Return the cabinet PNG matching current drawer state."""
    has_flashlight_in_inv = "Flashlight" in inventory
    has_remote_in_inv = "Remote" in inventory

    if cabinet_drawer2_open:
        if has_remote_in_inv:
            return cab_img_l2_empty or cab_img_l2 or cab_img_l1 or cab_img_closed
        else:
            return cab_img_l2 or cab_img_l1 or cab_img_closed
    elif cabinet_drawer1_open:
        if has_flashlight_in_inv:
            return cab_img_l1_empty or cab_img_l1 or cab_img_closed
        else:
            return cab_img_l1 or cab_img_closed
    return cab_img_closed


def _check_collision(r):
    """Return True if rect r overlaps any solid object in the current scene."""
    if current_scene == "living_room":
        if r.colliderect(desk_rect): return True
        if calendar_date in (DATE_1988, DATE_2026):
            if (r.colliderect(sofa_rect) or r.colliderect(cabinet_rect) or
                    r.colliderect(living_door_rect) or
                    r.colliderect(bathroom_door_rect) or
                    r.colliderect(bedroom_door_rect)): return True
            if calendar_date == DATE_2026 and r.colliderect(main_door_rect):
                return True
    elif current_scene == "bedroom":
        if (r.colliderect(bookshelf_rect) or r.colliderect(computer_desk_rect) or
                r.colliderect(bed_rect) or r.colliderect(iron_cabinet_rect) or
                r.colliderect(bedroom_door_rect)): return True
    elif current_scene == "bathroom":
        if (r.colliderect(toilet_rect) or r.colliderect(sink_rect) or
                r.colliderect(bathroom_exit_rect) or r.colliderect(bathtub_rect)): return True
    return False


def _draw_debug_rects(surface):
    """Overlay collision rects in red and room bounds in blue (F1)."""
    _SX = WINDOW_RES[0] / VIRTUAL_RES[0]
    _SY = (WINDOW_RES[1] - 60) / VIRTUAL_RES[1]
    _font = pygame.font.SysFont("consolas", 14)
    if current_scene == "living_room":
        rects = [desk_rect, calendar_rect, tv_rect, cabinet_rect,
                 living_door_rect, bathroom_door_rect, main_door_rect, sofa_rect]
    elif current_scene == "bedroom":
        rects = [bedroom_door_rect, bookshelf_rect, computer_desk_rect, bed_rect, iron_cabinet_rect]
    else:  # bathroom
        rects = [bathroom_exit_rect, pipe_rect, toilet_rect]
        if calendar_date != DATE_1988:
            rects += [mirror_rect, bathtub_rect]
    for r in rects:
        sr = (int(r.x * _SX), int(r.y * _SY), int(r.w * _SX), int(r.h * _SY))
        pygame.draw.rect(surface, (255, 0, 0), sr, 2)
        surface.blit(_font.render(f"({r.x},{r.y},{r.w},{r.h})", True, (255, 200, 0)),
                     (sr[0], sr[1] - 16))
    # Room movement bounds in blue (ROOM_BOUNDS format: min_x, max_x, min_y, max_y)
    bx0, bx1, by0, by1 = ROOM_BOUNDS.get(current_scene, (12, 288, 12, 208))
    bsr = (int(bx0 * _SX), int(by0 * _SY),
           int((bx1 - bx0) * _SX), int((by1 - by0) * _SY))
    pygame.draw.rect(surface, (80, 140, 255), bsr, 2)
    surface.blit(_font.render(f"bounds ({bx0},{bx1},{by0},{by1})", True, (80, 200, 255)),
                 (bsr[0], bsr[1] - 16))
    # Legend
    pygame.draw.rect(surface, (255, 0, 0),    (8,  8, 12, 12), 2)
    surface.blit(_font.render("F1 collision", True, (255, 200, 0)), (24,  6))
    pygame.draw.rect(surface, (80, 140, 255), (8, 24, 12, 12), 2)
    surface.blit(_font.render("F1 bounds",    True, (80, 200, 255)), (24, 22))


def _draw_debug_prox(surface):
    """Overlay proximity rects in green with object name labels (F2)."""
    _SX = WINDOW_RES[0] / VIRTUAL_RES[0]
    _SY = (WINDOW_RES[1] - 60) / VIRTUAL_RES[1]
    _font = pygame.font.SysFont("consolas", 14)

    def _draw_p(r, name):
        sr = (int(r.x * _SX), int(r.y * _SY), int(r.w * _SX), int(r.h * _SY))
        pygame.draw.rect(surface, (0, 220, 0), sr, 2)
        surface.blit(_font.render(name, True, (0, 255, 120)), (sr[0], sr[1] - 16))

    if current_scene == "living_room":
        _draw_p(calendar_proximity_rect,        "calendar")
        _draw_p(tv_proximity_rect,              "tv")
        _draw_p(cabinet_proximity_rect,         "cabinet")
        _draw_p(living_door_prox,               "living_door")
        _draw_p(bathroom_door_prox,             "bathroom_door")
        _draw_p(main_door_rect.inflate(5, 100), "main_door")
    elif current_scene == "bedroom":
        _draw_p(bedroom_door_prox, "bedroom_door")
        _draw_p(bookshelf_prox,    "bookshelf")
        _draw_p(computer_prox,     "computer")
        _draw_p(bed_rect.inflate(16, 16), "bed")
        _draw_p(iron_cabinet_rect.inflate(16, 16), "iron_cabinet")
    else:  # bathroom
        _draw_p(bathroom_exit_prox,            "exit")
        _draw_p(pipe_rect.inflate(12, 12),     "pipe")
        _draw_p(toilet_rect.inflate(16, 16),   "toilet")
        if calendar_date != DATE_1988:
            _draw_p(mirror_rect.inflate(24, 80),   "mirror")
            _draw_p(bathtub_rect.inflate(16, 16),  "bathtub")

    pygame.draw.rect(surface, (0, 220, 0), (8, 24, 12, 12), 2)
    surface.blit(_font.render("F2 proximity", True, (0, 255, 120)), (24, 22))


def draw_dialogue_ui(surface):
    """Draw character bust (upper body + thighs) at bottom-right and speech bubble."""
    _bust_src = player_img_1988_idle if calendar_date == DATE_1988 else player_img_2026_idle
    _bw = 0
    if _bust_src:
        _sw, _sh = _bust_src.get_size()
        _crop_h = int(_sh * 0.65)   # top 65% — includes upper body and thighs
        _crop = _bust_src.subsurface(pygame.Rect(0, 0, _sw, _crop_h))
        _display_h = _crop_h * 9   # 3x larger than previous (which was _half_h * 3)
        _display_w = int(_sw * _display_h / _crop_h)
        _max_h = WINDOW_RES[1] - 60
        if _display_h > _max_h:
            _display_h = _max_h
            _display_w = int(_sw * _display_h / _crop_h)
        if _display_w > WINDOW_RES[0] // 2:
            _display_w = WINDOW_RES[0] // 2
            _display_h = int(_crop_h * _display_w / _sw)
        _bw = _display_w
        _bust = pygame.transform.scale(_crop, (_display_w, _display_h))
        _by = WINDOW_RES[1] - 98 - _display_h
        if _by < 0:
            _by = 0
        surface.blit(_bust, (WINDOW_RES[0] - _display_w - 10, _by))
    _margin = 15
    _box_w = min(400, WINDOW_RES[0] - _bw - _margin * 3)
    if _box_w < 200:
        _box_w = 200
    _box_h = 165
    _box_y = WINDOW_RES[1] - 98 - _box_h
    _box_x = WINDOW_RES[0] - _bw - _box_w - _margin
    if _box_x < _margin:
        _box_x = _margin
    pygame.draw.rect(surface, (20, 20, 35), (_box_x, _box_y, _box_w, _box_h), border_radius=10)
    pygame.draw.rect(surface, (120, 160, 220), (_box_x, _box_y, _box_w, _box_h), 2, border_radius=10)
    _txt = cal_day_font.render(dialogue_text, True, (220, 220, 255))
    surface.blit(_txt, (_box_x + 16, _box_y + 20))
    if dialogue_has_choices:
        for _i, _lbl in enumerate(["Yes", "No"]):
            _col = (255, 220, 60) if _i == dialogue_choice else (160, 160, 160)
            _prefix = "▶ " if _i == dialogue_choice else "  "
            _cs = cal_day_font.render(_prefix + _lbl, True, _col)
            surface.blit(_cs, (_box_x + 16 + _i * 100, _box_y + _box_h - 44))
    else:
        _cs = cal_day_font.render("[SPACE to continue]", True, (140, 140, 140))
        surface.blit(_cs, (_box_x + 16, _box_y + _box_h - 44))


def _trigger_action(obj):
    """Execute the game action after dialogue confirmation."""
    global ui_state, current_scene, player_x, player_y
    global room_lights_on, iron_box_state, tetris_cart_spawned, cabinet_message, _msg_timer
    global dialogue_triggered, fighter_message, bathtub_state, mirror_breath_timer, mirror_fogged_in_ui, mirror_breathed_once
    dialogue_triggered = True
    if obj == "tv":
        ui_state = "tv"
    elif obj == "cabinet":
        ui_state = "cabinet"
    elif obj == "calendar":
        ui_state = "calendar"
        dialogue_triggered = False
    elif obj == "cartridge":
        inventory.append("Tetris Cartridge")
        tetris_cart_spawned = False
        cabinet_message = "Got Tetris Cartridge from the desk!"; _msg_timer = 180
        dialogue_triggered = False
    elif obj == "light":
        room_lights_on = True
        dialogue_triggered = False
    elif obj == "bedroom":
        current_scene = "bedroom"
        player_x = bedroom_door_rect.left - player_size - 10
        player_y = bedroom_door_rect.centery - player_size // 2
        dialogue_triggered = False
    elif obj == "bathroom":
        current_scene = "bathroom"
        player_x = bathroom_exit_rect.right + 10
        player_y = bathroom_exit_rect.centery - player_size // 2
        dialogue_triggered = False
    elif obj == "frontdoor":
        ui_state = "main_door"
    elif obj == "livingroom":
        current_scene = "living_room"
        player_x = living_door_rect.right + 10
        player_y = living_door_rect.centery - player_size // 2
        dialogue_triggered = False
    elif obj == "bookshelf":
        ui_state = "bookshelf"
        dialogue_triggered = False
    elif obj == "iron_cabinet":
        ui_state = "iron_cabinet"
        dialogue_triggered = False
    elif obj == "computer":
        selected_item = inventory[selected_inv_slot] if selected_inv_slot >= 0 and selected_inv_slot < len(inventory) else None
        if selected_item == "SF2 Cartridge":
            ui_state = "computer"
            init_rt_fighter()
            fighter_message = ""
        elif selected_item == "Tetris Cartridge":
            ui_state = "tetris"
            init_tetris()
        else:
            ui_state = "computer_idle"
        dialogue_triggered = False
    elif obj == "exit":
        current_scene = "living_room"
        player_x = bathroom_door_rect.left - player_size - 10
        player_y = bathroom_door_rect.centery - player_size // 2
        dialogue_triggered = False
    elif obj == "pipe":
        dialogue_triggered = False
    elif obj == "ironbox":
        iron_box_state = 1
        cabinet_message = "Picked up iron box! Place it under the leaking pipe."; _msg_timer = 180
        dialogue_triggered = False
    elif obj == "ironbox_place":
        iron_box_state = 2
        cabinet_message = "Iron box placed under the pipe. Water will rust it..."; _msg_timer = 180
        dialogue_triggered = False
    elif obj == "ironbox_rusty":
        ui_state = "iron_box"
        dialogue_triggered = False
    elif obj == "shelf":
        dialogue_triggered = False
    elif obj == "mirror":
        ui_state = "mirror"
        mirror_fogged_in_ui = False
        dialogue_triggered = False
    elif obj == "bathtub":
        ui_state = "bathtub_fill"
        dialogue_triggered = False


# Inventory bar helper
# -------------------------------------------------------------------------

def draw_inventory_bar():
    slot_size = 60
    num_slots = 10
    start_x = (WINDOW_RES[0] - num_slots * (slot_size + 10)) // 2
    bar_y = WINDOW_RES[1] - 92

    pygame.draw.rect(screen, (0, 0, 0),
                     (0, bar_y - 6, WINDOW_RES[0], WINDOW_RES[1] - (bar_y - 6)))

    for i in range(num_slots):
        sr = pygame.Rect(start_x + i * (slot_size+10), bar_y, slot_size, slot_size)
        bc = (255, 255, 255) if i == selected_inv_slot and selected_inv_slot >= 0 else (200, 200, 200)
        pygame.draw.rect(screen, bc, sr, 4)
        pygame.draw.rect(screen, (40, 40, 40), sr)
        if i == selected_inv_slot and selected_inv_slot >= 0:
            pygame.draw.rect(screen, (100, 100, 150), sr, 2)
        if i < len(inventory):
            item = inventory[i]
            if item == "Flashlight":
                if flashlight_img:
                    icon = pygame.transform.scale(flashlight_img, (60, 60))
                    screen.blit(icon, (sr.centerx - 30, sr.centery - 30))
                else:
                    draw_flashlight_icon(screen, sr.centerx, sr.centery, 50)
            elif item == "Key":
                draw_key_icon(screen, sr.centerx, sr.centery, 50)
            elif item == "MysteryCube":
                draw_mystery_cube_icon(screen, sr.centerx, sr.centery, 44)
            elif item == "SF2 Cartridge":
                if sf2_icon:
                    icon = pygame.transform.scale(sf2_icon, (slot_size - 8, slot_size - 8))
                    screen.blit(icon, (sr.x + 4, sr.y + 4))
                else:
                    draw_cartridge_icon(screen, sr.inflate(-10, -10), (220, 80, 30))
            elif item == "Tetris Cartridge":
                draw_cartridge_icon(screen, sr.inflate(-10, -10), (50, 200, 80))
            elif item == "Remote":
                if remote_img:
                    icon = pygame.transform.scale(remote_img, (60, 60))
                    screen.blit(icon, (sr.centerx - 30, sr.centery - 30))
                else:
                    pygame.draw.rect(screen, (60, 60, 180), sr.inflate(-12, -8))
                    pygame.draw.rect(screen, (100, 100, 220), sr.inflate(-12, -8), 2)
            elif item in ("Strange Cube 2", "MysteryCube"):
                draw_mystery_cube_icon(screen, sr.centerx, sr.centery, 44)
            else:
                pygame.draw.rect(screen, (150, 80, 200), sr.inflate(-14, -14))
        # Slot number label
        num_label = font.render(str(i + 1), True, (180, 180, 180))
        screen.blit(num_label, num_label.get_rect(centerx=sr.centerx, top=sr.bottom + 3))

# Main loop
# -------------------------------------------------------------------------

running = True
while running:
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # Date change detection
    if calendar_date != prev_calendar_date:
        if prev_calendar_date == DATE_1988 and calendar_date != DATE_1988:
            if iron_box_state == 2:
                iron_box_state = 3  # iron box rusts when returning from 1988
        if calendar_date == DATE_1988:
            room_lights_on = False
        prev_calendar_date = calendar_date

    # Safety: dialogue_active must not persist when not in game state
    if dialogue_active and ui_state != "game":
        dialogue_active = False

    # Auto-clear cabinet_message after timer expires
    if _msg_timer > 0:
        _msg_timer -= 1
    elif cabinet_message:
        cabinet_message = ""

    # Mirror breath fog timer
    if mirror_breath_timer > 0:
        mirror_breath_timer -= 1

    # Proximity rects
    calendar_proximity_rect = calendar_rect.inflate(5, 110)
    tv_proximity_rect       = tv_rect.inflate(5, 100)
    cabinet_proximity_rect = cabinet_rect.inflate(16, 16)
    living_door_prox   = living_door_rect.inflate(50, 0)
    bathroom_door_prox = bathroom_door_rect.inflate(70, 0)
    bedroom_door_prox  = bedroom_door_rect.inflate(20, 20)
    bookshelf_prox     = bookshelf_rect.inflate(16, 16)
    computer_prox      = computer_desk_rect.inflate(16, 16)
    bed_prox           = bed_rect.inflate(16, 16)
    iron_cabinet_prox  = iron_cabinet_rect.inflate(16, 16)
    bathroom_exit_prox = bathroom_exit_rect.inflate(50, 5)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:

            if dialogue_active:
                if event.key in (pygame.K_LEFT, pygame.K_UP):
                    dialogue_choice = 0
                elif event.key in (pygame.K_RIGHT, pygame.K_DOWN):
                    dialogue_choice = 1
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if dialogue_has_choices and dialogue_choice == 1:
                        dialogue_active = False
                    else:
                        _obj = dialogue_object
                        dialogue_active = False
                        _trigger_action(_obj)
                        # Flush queued key events to prevent rapid re-trigger
                        pygame.event.clear(pygame.KEYDOWN)
                elif event.key == pygame.K_ESCAPE:
                    dialogue_active = False
                continue

            if event.key == pygame.K_F1:
                debug_rects = not debug_rects
            if event.key == pygame.K_F2:
                debug_prox = not debug_prox

            if ui_state == "game":
                if event.key == pygame.K_1:
                    selected_inv_slot = 0 if last_inv_slot_key != 0 else -1
                    last_inv_slot_key = 0 if selected_inv_slot == 0 else -1
                elif event.key == pygame.K_2:
                    selected_inv_slot = 1 if last_inv_slot_key != 1 else -1
                    last_inv_slot_key = 1 if selected_inv_slot == 1 else -1
                elif event.key == pygame.K_3:
                    selected_inv_slot = 2 if last_inv_slot_key != 2 else -1
                    last_inv_slot_key = 2 if selected_inv_slot == 2 else -1
                elif event.key == pygame.K_4:
                    selected_inv_slot = 3 if last_inv_slot_key != 3 else -1
                    last_inv_slot_key = 3 if selected_inv_slot == 3 else -1
                elif event.key == pygame.K_5:
                    selected_inv_slot = 4 if last_inv_slot_key != 4 else -1
                    last_inv_slot_key = 4 if selected_inv_slot == 4 else -1
                
                elif event.key == pygame.K_SPACE:
                    _obj = ""
                    if current_scene == "living_room":
                        is_1988_dark = calendar_date == DATE_1988 and not room_lights_on
                        has_flashlight_selected = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Flashlight"

                        if tetris_cart_spawned and player_rect.colliderect(calendar_proximity_rect):
                            _obj = "cartridge"
                        elif player_rect.colliderect(calendar_proximity_rect):
                            _obj = "calendar"
                        elif is_1988_dark:
                            # In 1988 dark: only allow light switch with selected flashlight
                            if has_flashlight_selected and player_rect.colliderect(light_switch_prox):
                                _obj = "light"
                        elif calendar_date in (DATE_1988, DATE_2026):
                            if player_rect.colliderect(living_door_prox):
                                _obj = "bedroom"
                            elif player_rect.colliderect(bathroom_door_prox):
                                _obj = "bathroom"
                            elif calendar_date in (DATE_1988, DATE_2026):
                                if player_rect.colliderect(tv_proximity_rect):
                                    _obj = "tv"
                                elif player_rect.colliderect(cabinet_proximity_rect):
                                    _obj = "cabinet"
                            if calendar_date == DATE_2026:
                                if player_rect.colliderect(main_door_rect.inflate(5, 100)):
                                    _obj = "frontdoor"
                    elif current_scene == "bedroom":
                        if player_rect.colliderect(bedroom_door_prox):
                            _obj = "livingroom"
                        elif player_rect.colliderect(bookshelf_prox):
                            _obj = "bookshelf"
                        elif player_rect.colliderect(computer_prox):
                            _obj = "computer"
                        elif player_rect.colliderect(bed_rect.inflate(16, 16)):
                            _obj = "bed"
                        elif player_rect.colliderect(iron_cabinet_rect.inflate(16, 16)):
                            _obj = "iron_cabinet"
                    elif current_scene == "bathroom":
                        if player_rect.colliderect(bathroom_exit_prox):
                            _obj = "exit"
                        elif (calendar_date != DATE_1988 and
                              player_rect.colliderect(mirror_rect.inflate(24, 80))):
                            _obj = "mirror"
                        elif (calendar_date != DATE_1988 and mirror_breathed_once and
                              player_rect.colliderect(bathtub_rect.inflate(16, 16))):
                            _obj = "bathtub"
                        elif player_rect.colliderect(pipe_rect.inflate(12, 12)):
                            if calendar_date == DATE_1988 and iron_box_state == 1:
                                _obj = "ironbox_place"
                            else:
                                _obj = "pipe"
                    if _obj and _obj in DIALOGUE_MAP:
                        dialogue_active = True
                        dialogue_object = _obj
                        dialogue_text, dialogue_has_choices = DIALOGUE_MAP[_obj]
                        dialogue_choice = 0
                        
            elif ui_state == "computer_idle":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"

            elif ui_state == "computer":
                # Always allow number key selection and escape
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif event.key == pygame.K_1:
                    selected_inv_slot = 0 if last_inv_slot_key != 0 else -1
                    last_inv_slot_key = 0 if selected_inv_slot == 0 else -1
                elif event.key == pygame.K_2:
                    selected_inv_slot = 1 if last_inv_slot_key != 1 else -1
                    last_inv_slot_key = 1 if selected_inv_slot == 1 else -1
                elif event.key == pygame.K_3:
                    selected_inv_slot = 2 if last_inv_slot_key != 2 else -1
                    last_inv_slot_key = 2 if selected_inv_slot == 2 else -1
                elif event.key == pygame.K_4:
                    selected_inv_slot = 3 if last_inv_slot_key != 3 else -1
                    last_inv_slot_key = 3 if selected_inv_slot == 3 else -1
                elif event.key == pygame.K_5:
                    selected_inv_slot = 4 if last_inv_slot_key != 4 else -1
                    last_inv_slot_key = 4 if selected_inv_slot == 4 else -1
                # Other keys depend on fighter state
                elif fighter_state == "fighting":
                    if event.key == pygame.K_SPACE and rt_p1["state"] != "attacking":
                        rt_p1["atk_timer"] = 15
                        rt_p1["state"] = "attacking"
                        if abs(rt_p1["x"] - rt_p2["x"]) < 70 and rt_p1["y"] >= 470 and rt_p2["y"] >= 470:
                            rt_p2["hp"] -= 10
                            rt_p2["state"] = "jumping"
                    elif event.key == pygame.K_UP and rt_p1["y"] >= 470:
                        rt_p1["vy"] = -15
                        rt_p1["state"] = "jumping"
                elif fighter_state == "round_over":
                    if event.key == pygame.K_SPACE:
                        rt_p1["hp"] = 100
                        rt_p2["hp"] = 100
                        rt_p1["state"] = "idle"
                        rt_p2["state"] = "idle"
                        rt_p1["x"] = 200
                        rt_p2["x"] = VIRTUAL_RES_1080[0] - 200
                        rt_p1["vy"] = 0
                        rt_p2["vy"] = 0
                        fighter_state = "fighting"
                        fighter_message = ""
                elif fighter_state == "game_over":
                    if event.key == pygame.K_SPACE and fighter_enemy_wins == 2:
                        fighter_enemy_wins = 0
                        fighter_player_wins = 0
                        init_rt_fighter()
                        
            elif ui_state == "tv":
                if event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                    ui_state = "game"
                    tv_channel = 0  # reset channel when closing
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    # Handle inventory slot selection even in TV UI
                    if event.key == pygame.K_1:
                        selected_inv_slot = 0 if last_inv_slot_key != 0 else -1
                        last_inv_slot_key = 0 if selected_inv_slot == 0 else -1
                    elif event.key == pygame.K_2:
                        selected_inv_slot = 1 if last_inv_slot_key != 1 else -1
                        last_inv_slot_key = 1 if selected_inv_slot == 1 else -1
                    elif event.key == pygame.K_3:
                        selected_inv_slot = 2 if last_inv_slot_key != 2 else -1
                        last_inv_slot_key = 2 if selected_inv_slot == 2 else -1
                    elif event.key == pygame.K_4:
                        selected_inv_slot = 3 if last_inv_slot_key != 3 else -1
                        last_inv_slot_key = 3 if selected_inv_slot == 3 else -1
                    elif event.key == pygame.K_5:
                        selected_inv_slot = 4 if last_inv_slot_key != 4 else -1
                        last_inv_slot_key = 4 if selected_inv_slot == 4 else -1
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    # Only allow channel switching if remote is selected
                    selected_remote = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Remote"
                    if selected_remote:
                        if event.key == pygame.K_UP:
                            tv_channel = (tv_channel - 1) % 2
                        elif event.key == pygame.K_DOWN:
                            tv_channel = (tv_channel + 1) % 2

            elif ui_state == "cabinet":
                if event.key == pygame.K_ESCAPE:
                    cabinet_item_pending = None
                    ui_state = "game"
                    dialogue_triggered = False
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    # Handle inventory slot selection even in cabinet UI
                    slot_map = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3, pygame.K_5: 4}
                    slot_idx = slot_map[event.key]
                    selected_inv_slot = slot_idx if last_inv_slot_key != slot_idx else -1
                    last_inv_slot_key = slot_idx if selected_inv_slot == slot_idx else -1
                elif event.key == pygame.K_UP:
                    cabinet_selection = 0; cabinet_message = ""; _msg_timer = 0
                elif event.key == pygame.K_DOWN:
                    cabinet_selection = 1; cabinet_message = ""; _msg_timer = 0
                elif event.key == pygame.K_SPACE:
                    # If an item is visible and waiting to be picked up, pick it up
                    if cabinet_item_pending:
                        inventory.append(cabinet_item_pending)
                        if cabinet_item_pending == "Flashlight":
                            has_flashlight = True
                        cabinet_message = f"Got {cabinet_item_pending}!"; _msg_timer = 180
                        cabinet_item_pending = None
                    elif cabinet_selection == 0:
                        if not cabinet_drawer1_open:
                            cabinet_drawer1_open = True
                            if not has_flashlight:
                                cabinet_item_pending = "Flashlight"
                                cabinet_message = "Flashlight is here! SPACE to take it."; _msg_timer = 180
                            else:
                                cabinet_message = "Drawer is empty."; _msg_timer = 180
                        else:
                            if not has_flashlight:
                                cabinet_item_pending = "Flashlight"
                                cabinet_message = "Flashlight is here! SPACE to take it."; _msg_timer = 180
                            else:
                                cabinet_message = "Drawer is empty."; _msg_timer = 180
                    elif cabinet_selection == 1:
                        # Must select key in inventory to open drawer 2
                        has_key_selected = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Key"
                        if not has_key:
                            cabinet_message = "This drawer is locked. Need a key."; _msg_timer = 180
                        elif not has_key_selected:
                            cabinet_message = "Need to select the key in inventory!"; _msg_timer = 180
                        elif not cabinet_drawer2_open:
                            cabinet_drawer2_open = True
                            cabinet_item_pending = "Remote"
                            cabinet_message = "There's a remote inside! SPACE to take it."; _msg_timer = 180
                        else:
                            if "Remote" not in inventory and cabinet_drawer2_open:
                                cabinet_item_pending = "Remote"
                                cabinet_message = "Remote is here! SPACE to take it."; _msg_timer = 180
                            else:
                                cabinet_message = "Drawer is empty."; _msg_timer = 180

            elif ui_state == "calendar":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif calendar_stage == "year":
                    if event.key == pygame.K_SPACE:
                        calendar_stage = "month"
                    elif event.key == pygame.K_UP:
                        try: calendar_date = calendar_date.replace(year=calendar_date.year + 10)
                        except: pass
                    elif event.key == pygame.K_DOWN:
                        try: calendar_date = calendar_date.replace(year=max(1, calendar_date.year - 10))
                        except: pass
                    elif event.key == pygame.K_RIGHT:
                        try: calendar_date = calendar_date.replace(year=calendar_date.year + 1)
                        except: pass
                    elif event.key == pygame.K_LEFT:
                        try: calendar_date = calendar_date.replace(year=max(1, calendar_date.year - 1))
                        except: pass
                elif calendar_stage == "month":
                    if event.key == pygame.K_ESCAPE:
                        calendar_stage = "year"
                    elif event.key == pygame.K_SPACE:
                        calendar_stage = "day"
                    elif event.key == pygame.K_RIGHT:
                        y, m, d = calendar_date.year, calendar_date.month, calendar_date.day
                        m += 1
                        if m == 13: m = 1; y += 1
                        calendar_date = datetime.date(y, m, min(d, calendar.monthrange(y,m)[1]))
                    elif event.key == pygame.K_LEFT:
                        y, m, d = calendar_date.year, calendar_date.month, calendar_date.day
                        m -= 1
                        if m == 0: m = 12; y -= 1
                        calendar_date = datetime.date(y, m, min(d, calendar.monthrange(y,m)[1]))
                else: # "day"
                    if event.key == pygame.K_ESCAPE:
                        calendar_stage = "month"
                    elif event.key == pygame.K_SPACE:
                        ui_state = "game"
                        calendar_stage = "year"
                    elif event.key == pygame.K_RIGHT:
                        calendar_date += datetime.timedelta(days=1)
                    elif event.key == pygame.K_LEFT:
                        calendar_date -= datetime.timedelta(days=1)
                    elif event.key == pygame.K_UP:
                        calendar_date -= datetime.timedelta(days=7)
                    elif event.key == pygame.K_DOWN:
                        calendar_date += datetime.timedelta(days=7)

            elif ui_state == "tetris":
                # Always allow number key selection and escape
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                    tetris_just_exited = True
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    # Handle inventory slot selection in tetris (always allowed)
                    slot_map = {pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3, pygame.K_5: 4}
                    slot_idx = slot_map[event.key]
                    selected_inv_slot = slot_idx if last_inv_slot_key != slot_idx else -1
                    last_inv_slot_key = slot_idx if selected_inv_slot == slot_idx else -1
                elif tetris_game_over or tetris_won:
                    if event.key == pygame.K_SPACE:
                        init_tetris()
                else:
                    if event.key == pygame.K_LEFT:
                        if tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x - 1, tetris_piece_y):
                            tetris_piece_x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x + 1, tetris_piece_y):
                            tetris_piece_x += 1
                    elif event.key == pygame.K_UP:
                        nr = tetris_piece_rot + 1
                        if tetris_valid(tetris_board, tetris_piece_type, nr, tetris_piece_x, tetris_piece_y):
                            tetris_piece_rot = nr
                    elif event.key == pygame.K_DOWN:
                        if tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y + 1):
                            tetris_piece_y += 1
                    elif event.key == pygame.K_SPACE:
                        while tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y + 1):
                            tetris_piece_y += 1
                        tetris_place(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y)
                        tetris_board, cleared = tetris_clear_lines(tetris_board)
                        tetris_lines_cleared += cleared
                        tetris_fall_speed = max(80, 350 - tetris_lines_cleared * 13)
                        if tetris_lines_cleared >= TETRIS_LINES_WIN:
                            tetris_won = True
                            if not has_mystery_cube:
                                has_mystery_cube = True
                                inventory.append("MysteryCube")
                        else:
                            tetris_piece_type = tetris_next_type
                            tetris_next_type = random.randint(0, len(TETRIS_SHAPES)-1)
                            tetris_piece_rot = 0
                            tetris_piece_x = TETRIS_W // 2 - 2
                            tetris_piece_y = 0
                            if not tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y):
                                tetris_game_over = True
                        tetris_fall_time = pygame.time.get_ticks()

            elif ui_state == "iron_cabinet":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif event.key == pygame.K_UP:
                    ui_state = "gashapon"
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    # Handle inventory slot selection in iron cabinet
                    if event.key == pygame.K_1:
                        selected_inv_slot = 0 if last_inv_slot_key != 0 else -1
                        last_inv_slot_key = 0 if selected_inv_slot == 0 else -1
                    elif event.key == pygame.K_2:
                        selected_inv_slot = 1 if last_inv_slot_key != 1 else -1
                        last_inv_slot_key = 1 if selected_inv_slot == 1 else -1
                    elif event.key == pygame.K_3:
                        selected_inv_slot = 2 if last_inv_slot_key != 2 else -1
                        last_inv_slot_key = 2 if selected_inv_slot == 2 else -1
                    elif event.key == pygame.K_4:
                        selected_inv_slot = 3 if last_inv_slot_key != 3 else -1
                        last_inv_slot_key = 3 if selected_inv_slot == 3 else -1
                    elif event.key == pygame.K_5:
                        selected_inv_slot = 4 if last_inv_slot_key != 4 else -1
                        last_inv_slot_key = 4 if selected_inv_slot == 4 else -1

            elif ui_state == "gashapon":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "iron_cabinet"

            elif ui_state == "bookshelf":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif calendar_date != DATE_1988:
                    if event.key == pygame.K_LEFT:
                        bookshelf_selection = max(0, bookshelf_selection - 1)
                    elif event.key == pygame.K_RIGHT:
                        bookshelf_selection = min(1, bookshelf_selection + 1)
                    elif event.key in (pygame.K_UP, pygame.K_DOWN):
                        i = bookshelf_selection
                        bookshelf_order[i], bookshelf_order[i+1] = bookshelf_order[i+1], bookshelf_order[i]
                    elif event.key == pygame.K_SPACE:
                        if bookshelf_unlocked and "SF2 Cartridge" not in inventory:
                            inventory.append("SF2 Cartridge")
                            ui_state = "game"
                            cabinet_message = "Got SF2 Cartridge!"; _msg_timer = 180

                    if bookshelf_order == ["Blue", "Green", "Red"] and not bookshelf_unlocked:
                        bookshelf_unlocked = True

            elif ui_state == "main_door":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif event.key == pygame.K_SPACE:
                    cubes = [i for i in inventory if "Cube" in i]
                    # We can just let SPACE try to insert a cube if they have one not inserted yet
                    for i in range(4):
                        if not door_puzzle_state[i] and len(cubes) > i:
                            door_puzzle_state[i] = True
                            break

            elif ui_state == "sink":
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                    ui_state = "game"
                    if cup_state == 0:
                        cup_state = 1

            elif ui_state == "iron_box":
                # Only reached in 2026 when iron_box_state == 3 (rusty box)
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif event.key == pygame.K_SPACE:
                    if iron_box_state == 3:
                        iron_box_state = 4
                        inventory.append("Strange Cube 2")
                        cabinet_message = "Broke open the rusty iron box! Found a strange cube!"; _msg_timer = 180
                        ui_state = "game"

            elif ui_state == "mirror":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                    mirror_fogged_in_ui = False
                    mirror_breath_timer = 0
                elif event.key == pygame.K_SPACE:
                    if not mirror_fogged_in_ui:
                        mirror_fogged_in_ui = True
                        mirror_breath_timer = 120   # in-world fog timer
                        mirror_breathed_once = True  # unlock bathtub
                    else:
                        ui_state = "game"
                        mirror_fogged_in_ui = False
                        pygame.event.clear(pygame.KEYDOWN)

            elif ui_state == "bathtub_fill":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                    bathtub_state = 0
                    bathtub_selection = 0
                elif event.key in (pygame.K_LEFT, pygame.K_UP):
                    bathtub_selection = 0   # Hot water
                elif event.key in (pygame.K_RIGHT, pygame.K_DOWN):
                    bathtub_selection = 1   # Cold water
                elif event.key == pygame.K_SPACE:
                    bathtub_state = 2 if bathtub_selection == 0 else 1
                    cabinet_message = ("Bathtub filled with hot water!"
                                       if bathtub_state == 2
                                       else "Bathtub filled with cold water!")
                    _msg_timer = 180
                    ui_state = "game"
                    pygame.event.clear(pygame.KEYDOWN)

    # Player movement
    keys = pygame.key.get_pressed()
    old_x, old_y = player_x, player_y

    if ui_state == "game":
        _moved = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed; player_dir = "left"; _moved = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed; player_dir = "right"; _moved = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed; player_dir = "up"; _moved = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed; player_dir = "down"; _moved = True
        player_moving = _moved

    elif ui_state == "computer" and fighter_state == "fighting":
        if rt_p1["state"] != "attacking":
            if keys[pygame.K_LEFT]:
                rt_p1["x"] -= 4
                rt_p1["dir"] = -1
                if rt_p1["y"] >= 470: rt_p1["state"] = "moving"
            elif keys[pygame.K_RIGHT]:
                rt_p1["x"] += 4
                rt_p1["dir"] = 1
                if rt_p1["y"] >= 470: rt_p1["state"] = "moving"
            else:
                if rt_p1["y"] >= 470: rt_p1["state"] = "idle"

        if rt_p2["state"] != "attacking":
            dist = rt_p1["x"] - rt_p2["x"]
            if abs(dist) > 65:
                if dist > 0: rt_p2["x"] += 2; rt_p2["dir"] = 1
                else: rt_p2["x"] -= 2; rt_p2["dir"] = -1
                if rt_p2["y"] >= 470: rt_p2["state"] = "moving"
            elif abs(dist) <= 65 and rt_p2["atk_timer"] == 0 and random.random() < 0.05:
                rt_p2["atk_timer"] = 20
                rt_p2["state"] = "attacking"
                if rt_p1["y"] >= 470 and rt_p1["state"] != "jumping":
                    rt_p1["hp"] -= 15
            else:
                if rt_p2["y"] >= 470: rt_p2["state"] = "idle"
                if random.random() < 0.02 and rt_p2["y"] >= 470:
                    rt_p2["vy"] = -15; rt_p2["state"] = "jumping"

        for p in [rt_p1, rt_p2]:
            p["y"] += p["vy"]
            p["vy"] += 1
            if p["y"] > 470: p["y"] = 470; p["vy"] = 0
            p["x"] = max(50, min(p["x"], WINDOW_RES[0] - 50))
            if p["atk_timer"] > 0:
                p["atk_timer"] -= 1
                if p["atk_timer"] == 0 and p["y"] >= 470:
                    p["state"] = "idle"
            if p.get("invul_timer", 0) > 0:
                p["invul_timer"] -= 1

        p1r = pygame.Rect(rt_p1["x"] - 20, rt_p1["y"] - 40, 40, 80)
        p2r = pygame.Rect(rt_p2["x"] - 20, rt_p2["y"] - 40, 40, 80)

        if rt_p1["state"] == "attacking":
            hx = rt_p1["x"] + 40 * rt_p1["dir"]
            hitbox = pygame.Rect(hx - 20, rt_p1["y"] - 30, 40, 20)
            if hitbox.colliderect(p2r) and rt_p2.get("invul_timer", 0) == 0:
                rt_p2["hp"] -= 10
                rt_p2["invul_timer"] = 30
                rt_p2["x"] += 20 * rt_p1["dir"]

        if rt_p2["state"] == "attacking":
            hx = rt_p2["x"] + 40 * rt_p2["dir"]
            hitbox = pygame.Rect(hx - 20, rt_p2["y"] - 30, 40, 20)
            if hitbox.colliderect(p1r) and rt_p1.get("invul_timer", 0) == 0:
                rt_p1["hp"] -= 15
                rt_p1["invul_timer"] = 30
                rt_p1["x"] += 20 * rt_p2["dir"]

        if rt_p1["hp"] <= 0:
            fighter_enemy_wins += 1
            if fighter_enemy_wins == 2:
                fighter_state = "game_over"
                fighter_message = "CPU WINS! (Press SPACE to restart)"
            else:
                fighter_state = "round_over"
                fighter_message = "CPU Wins Round! (Press SPACE)"

        if rt_p2["hp"] <= 0:
            fighter_player_wins += 1
            if fighter_player_wins == 2:
                fighter_state = "game_over"
                if not has_key:
                    has_key = True
                    inventory.append("Key")
                    fighter_message = "P1 WINS! Got Key! (Press ESC)"
                else:
                    fighter_message = "P1 WINS! (Press ESC)"
            else:
                fighter_state = "round_over"
                fighter_message = "P1 Wins Round! (Press SPACE)"

    # Tetris fall logic
    if ui_state == "tetris" and not tetris_game_over and not tetris_won:
        now = pygame.time.get_ticks()
        if now - tetris_fall_time > tetris_fall_speed:
            if tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y + 1):
                tetris_piece_y += 1
            else:
                tetris_place(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y)
                tetris_board, cleared = tetris_clear_lines(tetris_board)
                tetris_lines_cleared += cleared
                tetris_fall_speed = max(80, 350 - tetris_lines_cleared * 13)
                if tetris_lines_cleared >= TETRIS_LINES_WIN:
                    tetris_won = True
                    if not has_mystery_cube:
                        has_mystery_cube = True
                        inventory.append("MysteryCube")
                else:
                    tetris_piece_type = tetris_next_type
                    tetris_next_type = random.randint(0, len(TETRIS_SHAPES)-1)
                    tetris_piece_rot = 0
                    tetris_piece_x = TETRIS_W // 2 - 2
                    tetris_piece_y = 0
                    if not tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y):
                        tetris_game_over = True
            tetris_fall_time = now

    # Per-room wall boundary clamp + per-axis collision
    _bx_min, _bx_max, _by_min, _by_max = ROOM_BOUNDS.get(
        current_scene, (12, 288, 12, 208))

    # X axis
    player_x = max(_bx_min, min(player_x, _bx_max))
    if _check_collision(pygame.Rect(player_x, player_y, player_size, player_size)):
        player_x = old_x

    # Y axis
    player_y = max(_by_min, min(player_y, _by_max))
    if _check_collision(pygame.Rect(player_x, player_y, player_size, player_size)):
        player_y = old_y

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # Rendering
    # -------------------------------------------------------------------------

    # Reset tetris_just_exited when player leaves living room
    if current_scene != "living_room":
        tetris_just_exited = False

    # Tetris cartridge spawn (Any year, 8/8)
    if calendar_date.month == 8 and calendar_date.day == 8:
        if "Tetris Cartridge" not in inventory:
            tetris_cart_spawned = True
    else:
        tetris_cart_spawned = False
        
    # Tetris cartridge is SPACE-triggered (handled in SPACE event section below)

    # Tetris rendering
    if ui_state == "tetris":
        draw_tetris_ui(screen)
        draw_inventory_bar()
        pygame.display.flip()
        clock.tick(60)
        continue

    # 1988 dark scene
    if calendar_date == DATE_1988 and ui_state in ("game", "tv"):
        sx = WINDOW_RES[0] / VIRTUAL_RES[0]
        sy = WINDOW_RES[1] / VIRTUAL_RES[1]
        px_1080 = int(player_x * VIRTUAL_RES_1080[0] / VIRTUAL_RES[0])
        py_1080 = int(player_y * VIRTUAL_RES_1080[1] / VIRTUAL_RES[1])
        pS_1080 = max(4, player_size * VIRTUAL_RES_1080[0] // VIRTUAL_RES[0])
        # Flashlight light only active if selected in inventory
        fl_active = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Flashlight"

        screen.blit(render_1988_scene(px_1080, py_1080, pS_1080, fl_active), (0, 0))

        _1988_walk = {
            "down": player_img_1988_walk_down, "up": player_img_1988_walk_up,
            "left": player_img_1988_walk_left, "right": player_img_1988_walk_right,
        }
        _1988_sprite = _1988_walk.get(player_dir) if player_moving else player_img_1988_idle
        if _1988_sprite is None:
            _1988_sprite = player_img_1988_idle
        if _1988_sprite:
            _SX = WINDOW_RES[0] / VIRTUAL_RES[0]
            _SY = (WINDOW_RES[1] - 60) / VIRTUAL_RES[1]
            _iw, _ih = _1988_sprite.get_size()
            _cx = int(player_x * _SX + player_size * _SX / 2)
            _bot = int(player_y * _SY + player_size * _SY)
            screen.blit(_1988_sprite, (_cx - _iw // 2, _bot - _ih))

        if not room_lights_on:
            if current_scene == "living_room":
                hint = high_res_inst_font.render(
                    "Find light switch | Flashlight ready" if fl_active else
                    "Pitch black. Pick up flashlight!",
                    True, (150, 150, 150))
            elif current_scene == "bedroom":
                hint = high_res_inst_font.render(
                    "Dark bedroom | SPACE at door to return" if fl_active else
                    "Dark bedroom | Find flashlight first",
                    True, (150, 150, 150))
            else:
                hint = high_res_inst_font.render(
                    "Dark bathroom | SPACE at door to return" if fl_active else
                    "Dark bathroom | Find flashlight first",
                    True, (150, 150, 150))
            screen.blit(hint, hint.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-200)))

        _do_proximity_check()
        if prompt_label and prompt_label_rect:
            _draw_label(screen)
        if dialogue_active:
            draw_dialogue_ui(screen)
        if debug_rects:
            _draw_debug_rects(screen)
        if debug_prox:
            _draw_debug_prox(screen)
        draw_inventory_bar()
        pygame.display.flip()
        clock.tick(60)
        continue

    # ---- BACKGROUND PHASE ----
    _use_hires_bg = None
    if current_scene == "living_room":
        if calendar_date == DATE_2026 and bg_living:
            _use_hires_bg = bg_living
        elif calendar_date != DATE_1988 and bg_living_orig:
            _use_hires_bg = bg_living_orig
    elif current_scene == "bedroom" and bg_bedroom:
        _use_hires_bg = bg_bedroom
    elif current_scene == "bathroom" and bg_bathroom:
        _use_hires_bg = bg_bathroom

    if _use_hires_bg:
        screen.blit(_use_hires_bg, (0, 0))
        display_surface.fill(CHROMA)
    elif current_scene == "bathroom":
        # 廁所 fallback：藍白磁磚 + 透視牆
        display_surface.fill((215, 220, 230))
        for i in range(0, VIRTUAL_RES[0], 20):
            for j in range(0, VIRTUAL_RES[1], 20):
                pygame.draw.rect(display_surface, (200, 205, 215), (i, j, 20, 20), 1)
        _VPT = _ROOM_VPT;  _VPB = _ROOM_VPY;  _LWX = _ROOM_LWX;  _RWX = _ROOM_RWX
        _BWBK=(235,245,252); _BWCEL=(220,232,242); _BWSID=(208,220,232); _BWLN=(155,170,185)
        pygame.draw.polygon(display_surface, _BWCEL,
                            [(0,0),(VIRTUAL_RES[0],0),(_RWX,_VPT),(_LWX,_VPT)])
        pygame.draw.rect(display_surface, _BWBK, (_LWX,_VPT,_RWX-_LWX,_VPB-_VPT))
        pygame.draw.polygon(display_surface, _BWSID,
                            [(0,0),(_LWX,_VPT),(_LWX,_VPB),(0,VIRTUAL_RES[1])])
        pygame.draw.polygon(display_surface, _BWSID,
                            [(VIRTUAL_RES[0],0),(_RWX,_VPT),(_RWX,_VPB),(VIRTUAL_RES[0],VIRTUAL_RES[1])])
        pygame.draw.line(display_surface, _BWLN, (0,0), (_LWX,_VPT), 2)
        pygame.draw.line(display_surface, _BWLN, (VIRTUAL_RES[0],0), (_RWX,_VPT), 2)
        pygame.draw.line(display_surface, _BWLN, (_LWX,_VPT), (_RWX,_VPT), 2)
        pygame.draw.line(display_surface, _BWLN, (_LWX,_VPB), (_RWX,_VPB), 2)
        pygame.draw.line(display_surface, _BWLN, (_LWX,_VPT), (_LWX,_VPB), 2)
        pygame.draw.line(display_surface, _BWLN, (_RWX,_VPT), (_RWX,_VPB), 2)
        pygame.draw.line(display_surface, _BWLN, (0,VIRTUAL_RES[1]), (_LWX,_VPB), 1)
        pygame.draw.line(display_surface, _BWLN, (VIRTUAL_RES[0],VIRTUAL_RES[1]), (_RWX,_VPB), 1)
    else:
        # 客廳 / 房間 fallback：大理石地板 + 透視牆
        display_surface.fill(MARBLE_COLOR_1)
        for i in range(0, VIRTUAL_RES[0], 32):
            for j in range(0, VIRTUAL_RES[1], 32):
                if (i // 32 + j // 32) % 2 == 0:
                    pygame.draw.rect(display_surface, MARBLE_COLOR_2, (i, j, 32, 32))
        _VPT = _ROOM_VPT;  _VPB = _ROOM_VPY;  _LWX = _ROOM_LWX;  _RWX = _ROOM_RWX
        _WBK  = (248, 248, 245)
        _WCEL = (235, 233, 230)
        _WSID = (220, 218, 215)
        _WLN  = (160, 155, 150)
        pygame.draw.polygon(display_surface, _WCEL,
                            [(0,0),(VIRTUAL_RES[0],0),(_RWX,_VPT),(_LWX,_VPT)])
        pygame.draw.rect(display_surface, _WBK,
                         (_LWX, _VPT, _RWX - _LWX, _VPB - _VPT))
        pygame.draw.polygon(display_surface, _WSID,
                            [(0,0),(_LWX,_VPT),(_LWX,_VPB),(0,VIRTUAL_RES[1])])
        pygame.draw.polygon(display_surface, _WSID,
                            [(VIRTUAL_RES[0],0),(_RWX,_VPT),(_RWX,_VPB),(VIRTUAL_RES[0],VIRTUAL_RES[1])])
        pygame.draw.line(display_surface, _WLN, (0,0), (_LWX,_VPT), 2)
        pygame.draw.line(display_surface, _WLN, (VIRTUAL_RES[0],0), (_RWX,_VPT), 2)
        pygame.draw.line(display_surface, _WLN, (_LWX,_VPT), (_RWX,_VPT), 2)
        pygame.draw.line(display_surface, _WLN, (_LWX,_VPB), (_RWX,_VPB), 2)
        pygame.draw.line(display_surface, _WLN, (_LWX,_VPT), (_LWX,_VPB), 2)
        pygame.draw.line(display_surface, _WLN, (_RWX,_VPT), (_RWX,_VPB), 2)
        pygame.draw.line(display_surface, _WLN, (0,VIRTUAL_RES[1]), (_LWX,_VPB), 1)
        pygame.draw.line(display_surface, _WLN, (VIRTUAL_RES[0],VIRTUAL_RES[1]), (_RWX,_VPB), 1)

    if current_scene == "living_room":
        if _use_hires_bg:
            # 背景圖含所有家具；只畫動態 overlay
            if tetris_cart_spawned:
                draw_cartridge_icon(display_surface, tetris_cart_rect, (50, 200, 80))
            # Show remote control next to TV if selected
            if remote_img and calendar_date == DATE_2026:
                selected_remote = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Remote"
                if selected_remote:
                    _rx = tv_rect.right + 8
                    _ry = tv_rect.centery - 3
                    _rw, _rh = 6, 6
                    try:
                        _remote_scaled = pygame.transform.scale(remote_img, (_rw, _rh))
                        display_surface.blit(_remote_scaled, (_rx, _ry))
                    except:
                        pass
        else:
            # 1988 或無圖 fallback：全部程式碼繪製
            draw_desk_and_calendar(display_surface)
            if calendar_date == DATE_2026:
                # Main door
                pygame.draw.rect(display_surface, (100, 50, 50), main_door_rect)
                pygame.draw.rect(display_surface, (80, 30, 30), main_door_rect.inflate(-4, -4))
                for i in range(4):
                    pygame.draw.rect(display_surface, (20, 20, 20), (main_door_rect.centerx - 12 + i*6, main_door_rect.y + 8, 4, 4))
                # Cabinet
                pygame.draw.rect(display_surface, (140, 90, 50), cabinet_rect)
                pygame.draw.rect(display_surface, (100, 60, 30), cabinet_rect.inflate(-4, -4))
                pygame.draw.rect(display_surface, (60, 30, 10),
                                 (cabinet_rect.x + 2, cabinet_rect.y + 20, cabinet_rect.width - 4, 2))
                pygame.draw.rect(display_surface, (60, 30, 10),
                                 (cabinet_rect.x + 2, cabinet_rect.y + 60, cabinet_rect.width - 4, 2))
                pygame.draw.circle(display_surface, (200, 200, 200),
                                   (cabinet_rect.centerx - 10, cabinet_rect.y + 10), 3)
                pygame.draw.circle(display_surface, (200, 200, 200),
                                   (cabinet_rect.centerx - 10, cabinet_rect.y + 40), 3)
                pygame.draw.circle(display_surface, (200, 200, 200),
                                   (cabinet_rect.centerx - 10, cabinet_rect.y + 80), 3)
                # Living door (to bedroom)
                pygame.draw.rect(display_surface, (120, 80, 50), living_door_rect)
                pygame.draw.rect(display_surface, (80, 40, 20), living_door_rect.inflate(-4, -4))
                pygame.draw.circle(display_surface, (200, 200, 50),
                                   (living_door_rect.right - 6, living_door_rect.centery - 2), 4)
                # Light switch
                pygame.draw.rect(display_surface, (205, 203, 200),
                                 (_SW_NX - 1, _SW_NY - 1, _SW_NW + 2, _SW_NH + 2))
                pygame.draw.rect(display_surface, (130, 128, 125),
                                 (_SW_NX, _SW_NY, _SW_NW, _SW_NH), 1)
                pygame.draw.circle(display_surface, (70, 140, 70),
                                   (_SW_NX + _SW_NW // 2, _SW_NY + _SW_NH // 2), 2)
                # Bathroom door
                pygame.draw.rect(display_surface, (120, 80, 50), bathroom_door_rect)
                pygame.draw.rect(display_surface, (80, 40, 20), bathroom_door_rect.inflate(-4, -4))
                pygame.draw.circle(display_surface, (200, 200, 50),
                                   (bathroom_door_rect.left + 4, bathroom_door_rect.centery), 4)

        # (Player drawn high-res on screen after scaling)

    elif current_scene == "bedroom":
        if not _use_hires_bg:
            # Bedroom door
            pygame.draw.rect(display_surface, (80, 40, 20), bedroom_door_rect)
            pygame.draw.rect(display_surface, (120, 80, 50), bedroom_door_rect.inflate(-4, -4))
            pygame.draw.circle(display_surface, (200, 200, 50),
                               (bedroom_door_rect.left + 6, bedroom_door_rect.centery - 2), 4)
            # Bookshelf
            pygame.draw.rect(display_surface, (90, 50, 20), bookshelf_rect)
            pygame.draw.rect(display_surface, (60, 30, 10), bookshelf_rect.inflate(-2, -2))
            for i in range(1, 4):
                pygame.draw.line(display_surface, (40, 20, 5),
                                 (bookshelf_rect.x, bookshelf_rect.y + i * 5),
                                 (bookshelf_rect.right, bookshelf_rect.y + i * 5), 1)
                pygame.draw.rect(display_surface, (200, 50, 50),
                                 (bookshelf_rect.x + 5, bookshelf_rect.y + i * 5 - 4, 3, 4))
                pygame.draw.rect(display_surface, (50, 200, 50),
                                 (bookshelf_rect.x + 15, bookshelf_rect.y + i * 5 - 4, 3, 4))
                pygame.draw.rect(display_surface, (50, 50, 200),
                                 (bookshelf_rect.x + 25, bookshelf_rect.y + i * 5 - 4, 3, 4))
            # Computer desk
            pygame.draw.rect(display_surface, (180, 180, 180), computer_desk_rect)
            pygame.draw.rect(display_surface, (120, 120, 120), computer_desk_rect.inflate(-4, -4))
            csr = pygame.Rect(computer_desk_rect.centerx - 15, computer_desk_rect.y - 15, 30, 20)
            pygame.draw.rect(display_surface, (80, 80, 80), csr)
            pygame.draw.rect(display_surface, (40, 40, 40), csr.inflate(-4, -4))
            pygame.draw.rect(display_surface, (200, 200, 255),
                             (csr.x + 2, csr.y + 2, csr.width - 4, csr.height - 4))
            pygame.draw.rect(display_surface, (50, 100, 255),
                             (csr.x + 4, csr.y + 4, csr.width - 8, csr.height - 8))
            # Bed
            pygame.draw.rect(display_surface, (180, 100, 80), bed_rect)
            pygame.draw.rect(display_surface, (150, 80, 60), bed_rect.inflate(-6, -6))
            # Iron Cabinet
            pygame.draw.rect(display_surface, (100, 100, 100), iron_cabinet_rect)
            pygame.draw.rect(display_surface, (120, 120, 120), iron_cabinet_rect.inflate(-3, -3))

    elif current_scene == "bathroom":
        if _use_hires_bg:
            # Dynamic overlays only: iron box states + pipe drip
            if calendar_date == DATE_1988 and iron_box_state == 0:
                bx, by = toilet_rect.x + 2, toilet_rect.y - 3
                pygame.draw.rect(display_surface, (160, 150, 120), (bx, by, 14, 10))
                pygame.draw.rect(display_surface, (100, 90, 70), (bx, by, 14, 10), 1)
            elif iron_box_state == 3:
                bx, by = toilet_rect.x + 2, toilet_rect.y - 3
                pygame.draw.rect(display_surface, (130, 70, 20), (bx, by, 14, 10))
                pygame.draw.rect(display_surface, (80, 40, 10), (bx, by, 14, 10), 1)
                pygame.draw.line(display_surface, (160, 85, 25), (bx + 3, by + 1), (bx + 3, by + 8), 1)
                pygame.draw.line(display_surface, (160, 85, 25), (bx + 9, by + 2), (bx + 9, by + 9), 1)
            if iron_box_state == 2 and calendar_date == DATE_1988:
                px_p, py_p = pipe_rect.x, pipe_rect.y
                pw_p, ph_p = pipe_rect.width, pipe_rect.height
                pygame.draw.rect(display_surface, (150, 130, 100), (px_p - 2, py_p + ph_p + 4, pw_p + 4, 8))
                pygame.draw.rect(display_surface, (100, 85, 65), (px_p - 2, py_p + ph_p + 4, pw_p + 4, 8), 1)
        else:
            # White tile floor
            display_surface.fill((215, 220, 230))
            for i in range(0, VIRTUAL_RES[0], 20):
                for j in range(0, VIRTUAL_RES[1], 20):
                    pygame.draw.rect(display_surface, (200, 205, 215), (i, j, 20, 20), 1)
            # Four-wall perspective (bathroom blue-white style)
            _VPT = _ROOM_VPT;  _VPB = _ROOM_VPY;  _LWX = _ROOM_LWX;  _RWX = _ROOM_RWX
            _BWBK  = (235, 245, 252)
            _BWCEL = (220, 232, 242)
            _BWSID = (208, 220, 232)
            _BWLN  = (155, 170, 185)
            pygame.draw.polygon(display_surface, _BWCEL,
                                [(0,0),(VIRTUAL_RES[0],0),(_RWX,_VPT),(_LWX,_VPT)])
            pygame.draw.rect(display_surface, _BWBK,
                             (_LWX, _VPT, _RWX - _LWX, _VPB - _VPT))
            pygame.draw.polygon(display_surface, _BWSID,
                                [(0,0),(_LWX,_VPT),(_LWX,_VPB),(0,VIRTUAL_RES[1])])
            pygame.draw.polygon(display_surface, _BWSID,
                                [(VIRTUAL_RES[0],0),(_RWX,_VPT),(_RWX,_VPB),(VIRTUAL_RES[0],VIRTUAL_RES[1])])
            pygame.draw.line(display_surface, _BWLN, (0,0), (_LWX,_VPT), 2)
            pygame.draw.line(display_surface, _BWLN, (VIRTUAL_RES[0],0), (_RWX,_VPT), 2)
            pygame.draw.line(display_surface, _BWLN, (_LWX,_VPT), (_RWX,_VPT), 2)
            pygame.draw.line(display_surface, _BWLN, (_LWX,_VPB), (_RWX,_VPB), 2)
            pygame.draw.line(display_surface, _BWLN, (_LWX,_VPT), (_LWX,_VPB), 2)
            pygame.draw.line(display_surface, _BWLN, (_RWX,_VPT), (_RWX,_VPB), 2)
            pygame.draw.line(display_surface, _BWLN, (0,VIRTUAL_RES[1]), (_LWX,_VPB), 1)
            pygame.draw.line(display_surface, _BWLN, (VIRTUAL_RES[0],VIRTUAL_RES[1]), (_RWX,_VPB), 1)
            # Bathtub on right side (below horizon)
            tub_x = VIRTUAL_RES[0] - 85
            pygame.draw.rect(display_surface, (240, 240, 245), (tub_x, 74, 70, 90))
            pygame.draw.rect(display_surface, (200, 225, 240), (tub_x + 5, 79, 60, 80))
            pygame.draw.ellipse(display_surface, (180, 210, 230), (tub_x + 5, 79, 60, 14))
            pygame.draw.rect(display_surface, (170, 170, 180), (tub_x, 74, 70, 90), 2)
            pygame.draw.rect(display_surface, (200, 200, 210), (tub_x + 28, 71, 5, 8))
            # Wall shelf
            shelf_x, shelf_y = toilet_rect.x - 2, toilet_rect.y - 6
            pygame.draw.rect(display_surface, (180, 160, 140), (shelf_x, shelf_y + 4, toilet_rect.width + 4, 4))
            pygame.draw.rect(display_surface, (210, 195, 170), (shelf_x, shelf_y, toilet_rect.width + 4, 5))
            # Exit door
            pygame.draw.rect(display_surface, (80, 40, 20), bathroom_exit_rect)
            pygame.draw.rect(display_surface, (120, 80, 50), bathroom_exit_rect.inflate(-4, -4))
            pygame.draw.circle(display_surface, (200, 200, 50),
                               (bathroom_exit_rect.right - 6, bathroom_exit_rect.centery - 2), 4)
            # Toilet
            draw_toilet(display_surface, toilet_rect)
            # Iron box on shelf
            if calendar_date == DATE_1988 and iron_box_state == 0:
                bx, by = toilet_rect.x + 2, toilet_rect.y - 3
                pygame.draw.rect(display_surface, (160, 150, 120), (bx, by, 14, 10))
                pygame.draw.rect(display_surface, (100, 90, 70), (bx, by, 14, 10), 1)
            elif iron_box_state == 3:
                bx, by = toilet_rect.x + 2, toilet_rect.y - 3
                pygame.draw.rect(display_surface, (130, 70, 20), (bx, by, 14, 10))
                pygame.draw.rect(display_surface, (80, 40, 10), (bx, by, 14, 10), 1)
                pygame.draw.line(display_surface, (160, 85, 25), (bx + 3, by + 1), (bx + 3, by + 8), 1)
                pygame.draw.line(display_surface, (160, 85, 25), (bx + 9, by + 2), (bx + 9, by + 9), 1)
            # Sink
            draw_sink(display_surface, sink_rect)
            # Leaking pipe
            px_p, py_p = pipe_rect.x, pipe_rect.y
            pw_p, ph_p = pipe_rect.width, pipe_rect.height
            pygame.draw.rect(display_surface, (80, 85, 95), (px_p - 3, py_p, pw_p + 6, 5))
            pygame.draw.rect(display_surface, (100, 105, 115), (px_p, py_p, pw_p, ph_p))
            pygame.draw.rect(display_surface, (130, 135, 145), (px_p + 2, py_p, pw_p - 4, ph_p), 1)
            if iron_box_state == 2 and calendar_date == DATE_1988:
                pygame.draw.rect(display_surface, (150, 130, 100), (px_p - 2, py_p + ph_p + 4, pw_p + 4, 8))
                pygame.draw.rect(display_surface, (100, 85, 65), (px_p - 2, py_p + ph_p + 4, pw_p + 4, 8), 1)

    # Scale low-res to window; colorkey makes CHROMA pixels transparent when hires bg is in use
    scaled_surface = pygame.transform.scale(display_surface, (WINDOW_RES[0], WINDOW_RES[1] - 60))
    if _use_hires_bg:
        scaled_surface.set_colorkey(CHROMA)
    screen.blit(scaled_surface, (0, 0))

    # High-res player drawn first so wall furniture appears in front
    _is_1988 = (calendar_date == DATE_1988)
    _idle_img = player_img_1988_idle if _is_1988 else player_img_2026_idle
    _walk_map = {
        "down":  player_img_1988_walk_down  if _is_1988 else player_img_2026_walk_down,
        "up":    player_img_1988_walk_up    if _is_1988 else player_img_2026_walk_up,
        "left":  player_img_1988_walk_left  if _is_1988 else player_img_2026_walk_left,
        "right": player_img_1988_walk_right if _is_1988 else player_img_2026_walk_right,
    }
    _psprite = _walk_map.get(player_dir) if player_moving else _idle_img
    if _psprite is None:
        _psprite = _idle_img
    if _psprite:
        _SX = WINDOW_RES[0] / VIRTUAL_RES[0]
        _SY = (WINDOW_RES[1] - 60) / VIRTUAL_RES[1]
        _iw, _ih = _psprite.get_size()
        _cx = int(player_x * _SX + player_size * _SX / 2)
        _bot = int(player_y * _SY + player_size * _SY)
        screen.blit(_psprite, (_cx - _iw // 2, _bot - _ih))
    else:
        draw_retro_player_hires(screen, player_x, player_y)

    # High-res sofa (living room only, fallback only when no hires bg)
    if current_scene == "living_room" and not _use_hires_bg and calendar_date == DATE_2026:
        draw_sofa_hires(screen, sofa_rect)

    # Object label & dialogue overlay
    _do_proximity_check()
    if prompt_label and prompt_label_rect:
        _draw_label(screen)
    if dialogue_active:
        draw_dialogue_ui(screen)

    # UI Overlays
    if ui_state == "calendar":
        draw_grid_calendar_ui(screen, calendar_date)

    elif ui_state == "tv":
        # Select which TV image to show based on date and channel
        current_tv_img = None

        # Check if 1988 date
        if calendar_date == DATE_1988:
            # In 1988, show appropriate TV image based on remote selection
            selected_remote = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Remote"
            if selected_remote and tv_1988_with_remote:
                current_tv_img = tv_1988_with_remote
            elif tv_1988_no_remote:
                current_tv_img = tv_1988_no_remote
        else:
            # 2026: use normal channel switching
            if tv_channel == 0 and tv_image:
                current_tv_img = tv_image
            elif tv_channel == 1 and tetris_tv_image:
                current_tv_img = tetris_tv_image

        if current_tv_img:
            _tw = int(current_tv_img.get_width() * 0.3)
            _th = int(current_tv_img.get_height() * 0.3)
            _tx = (WINDOW_RES[0] - _tw) // 2
            _ty = (WINDOW_RES[1] - _th) // 2
            screen.blit(pygame.transform.scale(current_tv_img, (_tw, _th)), (_tx, _ty))

            # Show remote control image at far right if player selected it
            selected_remote = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Remote"
            if selected_remote:
                if remote_img:
                    _rw = int(remote_img.get_width() * 0.2)
                    _rh = int(remote_img.get_height() * 0.2)
                    _rx = WINDOW_RES[0] - _rw
                    _ry = WINDOW_RES[1] // 2 - _rh // 2
                    screen.blit(pygame.transform.scale(remote_img, (_rw, _rh)), (_rx, _ry))
        else:
            _avail_w = WINDOW_RES[0] - 200
            _avail_h = WINDOW_RES[1] - 200
            _tw, _th = _avail_w, _avail_h
            _tx, _ty = 100, 100
            pygame.draw.rect(screen, (40, 40, 40), (_tx, _ty, _tw, _th))
            ts = high_res_big_font.render("TV is ON", True, (255, 255, 255))
            screen.blit(ts, ts.get_rect(center=(_tx + _tw // 2, _ty + _th // 2)))

        # Show instructions
        selected_remote = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Remote"
        if selected_remote:
            inst = high_res_inst_font.render("Up/Down: Change Channel | SPACE/ESC: Close", True, (200, 200, 200))
        else:
            inst = high_res_inst_font.render("SPACE or ESC to close  (選擇遙控器可轉台)", True, (200, 200, 200))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

    elif ui_state == "bathtub_fill":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 210))
        screen.blit(overlay, (0, 0))
        _title = cal_day_font.render("Fill the bathtub with:", True, (200, 230, 255))
        screen.blit(_title, _title.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 - 70)))
        for _i, (_lbl, _col) in enumerate([("Hot Water", (255, 120, 60)),
                                            ("Cold Water", (100, 180, 255))]):
            _sel = (bathtub_selection == _i)
            _prefix = "▶ " if _sel else "  "
            _tc = _col if _sel else (90, 90, 90)
            _opt = cal_day_font.render(_prefix + _lbl, True, _tc)
            screen.blit(_opt, _opt.get_rect(center=(WINDOW_RES[0]//2,
                                                     WINDOW_RES[1]//2 - 10 + _i * 56)))
        _hint = cal_inst_font.render(
            "Left/Right: Choose   SPACE: Confirm   ESC: Cancel", True, (110, 110, 110))
        screen.blit(_hint, _hint.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 + 110)))

    elif ui_state == "mirror":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))
        if bathtub_state == 2:
            _mimg = mirror_full_fog_img
        else:
            _mimg = mirror_fog_img if mirror_fogged_in_ui else mirror_clear_img
        if _mimg:
            _avail_w = WINDOW_RES[0] - 160
            _avail_h = WINDOW_RES[1] - 200
            _ratio = _mimg.get_width() / _mimg.get_height()
            _mw2 = min(_avail_w, int(_avail_h * _ratio))
            _mh2 = int(_mw2 / _ratio)
            _mx3 = (WINDOW_RES[0] - _mw2) // 2
            _my3 = (WINDOW_RES[1] - _mh2) // 2
            screen.blit(pygame.transform.scale(_mimg, (_mw2, _mh2)), (_mx3, _my3))
        if mirror_fogged_in_ui:
            _hint2 = cal_inst_font.render("SPACE: Close", True, (160, 160, 160))
        else:
            _hint2 = cal_inst_font.render("SPACE: Breathe   ESC: Close", True, (160, 160, 160))
        screen.blit(_hint2, _hint2.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 80)))

    elif ui_state == "cabinet":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, 0))

        # Crop the actual cabinet from bg image and zoom it for the dialog
        _SX_c = WINDOW_RES[0] / VIRTUAL_RES[0]
        _SY_c = (WINDOW_RES[1] - 60) / VIRTUAL_RES[1]
        _bg_src = bg_living_orig or bg_living
        _dw, _dh = 440, 560
        _dx = (WINDOW_RES[0] - _dw) // 2
        _dy = (WINDOW_RES[1] - _dh) // 2 - 20
        if _bg_src:
            _ci_popup = _cab_current_img()
            if _ci_popup:
                screen.blit(pygame.transform.scale(_ci_popup, (_dw, _dh)), (_dx, _dy))
            else:
                _cx = int(cabinet_rect.centerx * _SX_c)
                _cy = int((cabinet_rect.centery + 40) * _SY_c)
                _cw, _ch = 220, 320
                _cr = pygame.Rect(_cx - _cw // 2, _cy - _ch // 3, _cw, _ch)
                _cr = _cr.clip(pygame.Rect(0, 0, *_HIRES))
                _cab_crop = _bg_src.subsurface(_cr)
                screen.blit(pygame.transform.scale(_cab_crop, (_dw, _dh)), (_dx, _dy))
        else:
            pygame.draw.rect(screen, (120, 80, 40), pygame.Rect(_dx, _dy, _dw, _dh), border_radius=10)
            pygame.draw.rect(screen, (80, 50, 20), pygame.Rect(_dx, _dy, _dw, _dh), 4, border_radius=10)

        _d1_rect = pygame.Rect(_dx + 30, _dy + _dh // 4, _dw - 60, _dh // 4)
        _d2_rect = pygame.Rect(_dx + 30, _dy + _dh // 2 + 10, _dw - 60, _dh // 4)

        # Draw yellow border around selected drawer (width /2, height *0.8)
        _border_width = 2
        if cabinet_selection == 0:
            _bd1 = _d1_rect.inflate(-_d1_rect.width // 2, -int(_d1_rect.height * 0.2))
            # Move down closer to second drawer
            _bd1 = _bd1.move(0, _dh // 8)
            pygame.draw.rect(screen, (255, 255, 80), _bd1, _border_width, border_radius=6)
        else:
            _bd2 = _d2_rect.inflate(-_d2_rect.width // 2, -int(_d2_rect.height * 0.2))
            pygame.draw.rect(screen, (255, 255, 80), _bd2, _border_width, border_radius=6)

        if cabinet_message:
            msg = high_res_inst_font.render(cabinet_message, True, (255, 100, 100))
            screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0] // 2, _dy - 40)))
        inst = high_res_inst_font.render("Up/Dn: Select | SPACE: Open/Interact | ESC: Close", True, (220, 220, 220))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0] // 2, WINDOW_RES[1] - 110)))
        if dialogue_triggered:
            _bust_src = player_img_1988_idle if calendar_date == DATE_1988 else player_img_2026_idle
            if _bust_src:
                _bh = 200
                _bw = int(_bust_src.get_width() * _bh / _bust_src.get_height())
                _bust = pygame.transform.scale(_bust_src, (_bw, _bh))
                screen.blit(_bust, (WINDOW_RES[0] - _bw - 10, WINDOW_RES[1] - 60 - _bh))

    elif ui_state == "computer_idle":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))
        mon_r = pygame.Rect(WINDOW_RES[0]//2 - 220, WINDOW_RES[1]//2 - 160, 440, 280)
        pygame.draw.rect(screen, (30, 30, 30), mon_r, border_radius=8)
        pygame.draw.rect(screen, (80, 80, 80), mon_r, 4, border_radius=8)
        scr_r = mon_r.inflate(-24, -24)
        pygame.draw.rect(screen, (0, 15, 0), scr_r)
        blink_on = (pygame.time.get_ticks() // 600) % 2 == 0
        if blink_on:
            ic = high_res_inst_font.render("INSERT CARTRIDGE", True, (0, 255, 60))
            screen.blit(ic, ic.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 - 20)))
        hint_ic = font.render("Select a cartridge (1-5) then press SPACE near computer  |  ESC: close", True, (0, 180, 40))
        screen.blit(hint_ic, hint_ic.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 + 40)))
        pygame.draw.rect(screen, (50, 50, 50), (WINDOW_RES[0]//2 - 30, mon_r.bottom, 60, 20))

    elif ui_state == "computer":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        c_rect = pygame.Rect(100, 100, WINDOW_RES[0] - 200, WINDOW_RES[1] - 200)
        pygame.draw.rect(screen, (20, 20, 20), c_rect, border_radius=10)
        pygame.draw.rect(screen, (150, 150, 150), c_rect, 4, border_radius=10)
        
        screen.blit(font.render("STREET FIGHTER II", True, (255, 50, 50)), (c_rect.x + 20, c_rect.y + 20))

        pygame.draw.rect(screen, (100, 200, 100), (c_rect.x + 50, c_rect.y + 500, c_rect.width - 100, 20))

        # Win indicator circles (left = player, right = enemy)
        for i in range(2):
            col_p = (255, 215, 0) if i < fighter_player_wins else (60, 60, 60)
            pygame.draw.circle(screen, col_p, (c_rect.x + 50 + i * 22, c_rect.y + 32), 8)
            col_e = (255, 215, 0) if i < fighter_enemy_wins else (60, 60, 60)
            pygame.draw.circle(screen, col_e, (c_rect.right - 50 - i * 22, c_rect.y + 32), 8)

        # Health bars
        pygame.draw.rect(screen, (255, 0, 0), (c_rect.x + 50, c_rect.y + 60, 300, 20))
        pygame.draw.rect(screen, (0, 255, 0), (c_rect.x + 50, c_rect.y + 60, 3 * max(0, rt_p1["hp"]), 20))

        pygame.draw.rect(screen, (255, 0, 0), (c_rect.right - 350, c_rect.y + 60, 300, 20))
        pygame.draw.rect(screen, (0, 255, 0), (c_rect.right - 50 - 3 * max(0, rt_p2["hp"]), c_rect.y + 60, 3 * max(0, rt_p2["hp"]), 20))

        screen.blit(font.render("PLAYER 1", True, (255, 255, 255)), (c_rect.x + 50, c_rect.y + 40))
        screen.blit(font.render("COMPUTER", True, (255, 255, 255)), (c_rect.right - 350, c_rect.y + 40))

        draw_fighter(screen, rt_p1["x"], rt_p1["y"], True, rt_p1["state"], rt_p1["hp"])
        draw_zangief(screen, rt_p2["x"], rt_p2["y"], rt_p2["dir"], rt_p2["state"], rt_p2["hp"], rt_p2.get("invul_timer", 0))

        if fighter_message:
            msg = high_res_inst_font.render(fighter_message, True, (255, 255, 0))
            screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, c_rect.y + 200)))

        inst = high_res_inst_font.render("Arrows: Move/Jump | SPACE: Attack | ESC: Close", True, (200, 200, 200))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

        # Draw inventory bar in computer UI
        draw_inventory_bar()

    elif ui_state == "iron_cabinet":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, 0))

        # Display iron cabinet image
        if iron_cabinet_img:
            _w = int(iron_cabinet_img.get_width() * 0.4)
            _h = int(iron_cabinet_img.get_height() * 0.4)
            _x = (WINDOW_RES[0] - _w) // 2
            _y = (WINDOW_RES[1] - _h) // 2
            screen.blit(pygame.transform.scale(iron_cabinet_img, (_w, _h)), (_x, _y))

        inst = high_res_inst_font.render("UP: Open Gashapon | ESC: Close", True, (220, 220, 220))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

        draw_inventory_bar()

    elif ui_state == "gashapon":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, 0))

        # Display gashapon machine
        if gashapon_img:
            _w = int(gashapon_img.get_width() * 0.5)
            _h = int(gashapon_img.get_height() * 0.5)
            _x = (WINDOW_RES[0] - _w) // 2
            _y = (WINDOW_RES[1] - _h) // 2
            screen.blit(pygame.transform.scale(gashapon_img, (_w, _h)), (_x, _y))

        inst = high_res_inst_font.render("ESC: Back to Cabinet", True, (220, 220, 220))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

        draw_inventory_bar()

    elif ui_state == "bookshelf":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        b_rect = pygame.Rect(WINDOW_RES[0]//2 - 200, WINDOW_RES[1]//2 - 150, 400, 300)
        pygame.draw.rect(screen, (90, 50, 20), b_rect, border_radius=10)
        pygame.draw.rect(screen, (60, 30, 10), b_rect, 5, border_radius=10)
        
        colors = {"Red": (200, 50, 50), "Blue": (50, 50, 200), "Green": (50, 200, 50)}
        
        if calendar_date == DATE_1988:
            display_order = ["Blue", "Green", "Red"]
        else:
            display_order = bookshelf_order

        for i, b in enumerate(display_order):
            book_r = pygame.Rect(b_rect.x + 80 + i*90, b_rect.y + 100, 60, 150)
            pygame.draw.rect(screen, colors[b], book_r)
            if i == bookshelf_selection and calendar_date != DATE_1988:
                pygame.draw.rect(screen, (255, 255, 0), book_r, 3)
                
        if bookshelf_unlocked and "SF2 Cartridge" not in inventory:
            # Draw cartridge sitting between books
            cart_r = pygame.Rect(b_rect.centerx - 24, b_rect.y + 60, 48, 30)
            draw_cartridge_icon(screen, cart_r, (220, 80, 30))
            msg = high_res_inst_font.render("SPACE to take SF2 Cartridge!", True, (255, 220, 0))
        elif bookshelf_unlocked:
            msg = high_res_inst_font.render("SF2 Cartridge taken.", True, (150, 255, 100))
        elif calendar_date == DATE_1988:
            msg = high_res_inst_font.render("Books are stuck...", True, (200, 200, 200))
        else:
            msg = high_res_inst_font.render("L/R: Select | U/D: Swap | ESC: Close", True, (200, 200, 200))
        screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-100)))

    elif ui_state == "main_door":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        d_rect = pygame.Rect(WINDOW_RES[0]//2 - 200, WINDOW_RES[1]//2 - 200, 400, 400)
        pygame.draw.rect(screen, (100, 50, 50), d_rect, border_radius=10)
        
        # 4 slots
        for i in range(4):
            slot_r = pygame.Rect(d_rect.x + 80 + i*60, d_rect.centery, 40, 40)
            pygame.draw.rect(screen, (20, 20, 20), slot_r)
            if door_puzzle_state[i]:
                pygame.draw.rect(screen, (255, 100, 255), slot_r.inflate(-10, -10))
                
        if all(door_puzzle_state):
            msg = high_res_inst_font.render("DOOR OPENED! YOU ESCAPED!", True, (0, 255, 0))
        else:
            msg = high_res_inst_font.render("SPACE: Insert Cube | ESC: Close", True, (200, 200, 200))
        screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-100)))

    elif ui_state == "sink":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        cx, cy = WINDOW_RES[0] // 2, WINDOW_RES[1] // 2
        CUP_COLOR  = (110, 80, 50)
        CUP_RUST   = (160, 90, 30)
        if cup_state == 0:
            # Draw intact cup: trapezoid body + ellipse top + ellipse bottom
            cup_pts = [(cx - 28, cy - 50), (cx + 28, cy - 50),
                       (cx + 22, cy + 30), (cx - 22, cy + 30)]
            pygame.draw.polygon(screen, CUP_COLOR, cup_pts)
            pygame.draw.polygon(screen, CUP_RUST, cup_pts, 3)
            pygame.draw.ellipse(screen, CUP_RUST, (cx - 28, cy - 58, 56, 16))
            pygame.draw.ellipse(screen, (80, 55, 25), (cx - 22, cy + 22, 44, 14))
            # Rust streaks
            for rx, ry in [(-12, -20), (8, -5), (-3, 10)]:
                pygame.draw.line(screen, (180, 100, 20), (cx + rx, cy + ry), (cx + rx + 4, cy + ry + 18), 2)
            msg_str = "A rusty cup. SPACE to pick it up."
        else:
            # Smashed cup: scatter fragments
            frags = [
                [(cx - 30, cy - 10), (cx - 10, cy - 30), (cx, cy - 10)],
                [(cx + 5,  cy - 25), (cx + 30, cy - 15), (cx + 15, cy + 5)],
                [(cx - 20, cy + 10), (cx + 5,  cy + 5),  (cx - 5,  cy + 35)],
                [(cx + 10, cy + 15), (cx + 35, cy + 10), (cx + 25, cy + 35)],
            ]
            for frag in frags:
                pygame.draw.polygon(screen, CUP_RUST, frag)
                pygame.draw.polygon(screen, CUP_COLOR, frag, 2)
            msg_str = "The cup crumbled in your hand!"
        msg = high_res_inst_font.render(msg_str, True, (220, 200, 160))
        screen.blit(msg, msg.get_rect(center=(cx, cy + 80)))

    elif ui_state == "iron_box":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        if calendar_date == DATE_1988:
            if iron_box_state == 0:
                msg_str = "An iron box. SPACE to pick up."
            elif iron_box_state == 1:
                msg_str = "Holding iron box. SPACE to put under leaky pipe."
            else:
                msg_str = "Iron box is placed under the leak."
        else:
            if iron_box_state == 3:
                msg_str = "A rusty iron box! SPACE to break it open."
            elif iron_box_state == 4:
                msg_str = "It's broken. You found a Strange Cube!"
            else:
                msg_str = "Just an empty shelf."
                
        msg = high_res_inst_font.render(msg_str, True, (200, 200, 200))
        screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2)))

    # Easter Egg overlays
    if ui_state == "game" and current_scene == "living_room":
        import datetime
        if calendar_date == datetime.date(2023, 6, 19):
            msg = high_res_inst_font.render("This date feels familiar... (Easter Egg Place)", True, (200, 200, 200))
            screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, 50)))
        elif calendar_date == datetime.date(1994, 10, 23):
            msg = high_res_inst_font.render("A strange memory surfaces... (Easter Egg Place)", True, (200, 200, 200))
            screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, 50)))

    # Inventory bar (hidden when calendar is open)
    if ui_state != "calendar":
        draw_inventory_bar()

    if debug_rects:
        _draw_debug_rects(screen)
    if debug_prox:
        _draw_debug_prox(screen)

    # HUD notification: show cabinet_message above inventory when in game
    if ui_state == "game" and cabinet_message:
        notif = high_res_inst_font.render(cabinet_message, True, (255, 220, 80), (0, 0, 0))
        nr = notif.get_rect(center=(WINDOW_RES[0] // 2, 60))
        nr.left  = max(4, nr.left)
        nr.right = min(WINDOW_RES[0] - 4, nr.right)
        screen.blit(notif, nr)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()