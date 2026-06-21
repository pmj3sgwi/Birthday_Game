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
cabinet_rect        = pygame.Rect(25, 35, 50, 90)          # 左側邊桌/抽屜
living_door_rect    = pygame.Rect(15, 130, 10, 50)         # 左牆門→臥室
sofa_rect           = pygame.Rect(90, 190, 130, 50)        # 沙發

# Bedroom (top-down view)
bedroom_door_rect   = pygame.Rect(280, 115, 18, 65)  # right wall door（下方，y=142-207）
bookshelf_rect      = pygame.Rect(20, 30, 57, 97)    # 左側書架（頂牆靠左）
computer_desk_rect  = pygame.Rect(78, 30, 110, 90)   # 電腦桌（頂牆中央）

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
high_res_inst_font = pygame.font.SysFont("consolas", 28)
cal_header_font    = pygame.font.SysFont("consolas", 30)
cal_day_font       = pygame.font.SysFont("consolas", 24)
inv_font           = pygame.font.SysFont("consolas", 22)
cal_inst_font      = pygame.font.SysFont("consolas", 18)

ui_state          = "title"
calendar_stage    = "year" # "year" | "month" | "day"

cabinet_selection = 0
cabinet_drawer1_open = False
cabinet_drawer2_open = False
cabinet_item_pending = None  # item visible in open drawer, not yet picked up
cabinet_l2_coin_taken = False  # whether the coin left behind in drawer 2 has been collected
has_flashlight    = False
has_key           = False
cabinet_message   = ""
_msg_timer        = 0    # frames until cabinet_message auto-clears
debug_rects       = False  # F1 to toggle collision rect overlay
debug_prox        = False  # F2 to toggle proximity rect overlay
inventory         = []

# Iron cabinet password lock
iron_cabinet_unlocked = False
iron_cabinet_coin_taken = False  # whether the coin left inside the unlocked cabinet has been collected
iron_cabinet_scare_start = 0  # tick when the 1988 jump-scare started
outdoor_message_shown = False  # whether the birthday message popup is showing
cabinet_password_input = ""  # Current input string
cabinet_password_target = "JETAIMEPLUSQUETOUT"  # Target password (18 chars, no spaces, no apostrophe)
cabinet_password_edit_pos = 0  # Current cursor position for editing
cabinet_password_feedback = ""  # Feedback message (correct/incorrect)
cabinet_password_feedback_timer = 0  # Timer for feedback message display

# Gashapon (coin-operated) prize system
GASHAPON_PRIZES = ["扭蛋_皮克敏_去背.png", "扭蛋_烏薩奇_去背.png", "扭蛋_恐龍_去背.png", "扭蛋_韓立_去背.png"]
gashapon_last_prize = None  # most recently drawn prize, used for the popup icon
gashapon_feedback = ""  # Feedback message (success/need coin)
gashapon_feedback_timer = 0  # Timer for feedback message display

DATE_1988         = datetime.date(1988, 6, 22)
DATE_2026         = datetime.date(2026, 6, 22)
DATE_1994_10_23   = datetime.date(1994, 10, 23)
selected_inv_slot = -1  # -1 means no selection
last_inv_slot_key = -1  # track last pressed number key for toggle behavior
tv_channel = 0  # current TV channel selection (0=normal, 1=TETRIS)
chi_baby_x = 150  # Chi baby X position
chi_baby_y = 160  # Chi baby Y position
chi_baby_dir_x = 1  # Chi baby X direction: 1=right, -1=left
chi_baby_dir_y = 0  # Chi baby Y direction: 1=down, -1=up, 0=stop
chi_baby_speed = 1  # Chi baby movement speed
chi_baby_img = None  # Chi baby image cache
chi_baby_change_dir_timer = 0  # Timer for random direction changes
chi_baby_has_pacifier = False  # Chi baby has received pacifier
chi_baby_img_with_pacifier = None  # Chi baby with pacifier image
coin_items = []  # List of coins that fell from Chi baby
coin_img = None  # Coin image cache
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
    "bed":          ("There's a notebook on the bed. Take a look?", True),
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
    "chi_baby":     ("Should I give this pacifier to Chi Baby?", True),
}

# Puzzle & Interaction States
bookshelf_order   = ["Red", "Blue", "Green"]
bookshelf_selection = 0
bookshelf_unlocked = False

iron_box_state    = 0  # 0: shelf, 1: holding, 2: under pipe, 3: rusty, 4: broken
cup_state         = 0  # 0: intact, 1: crushed
tetris_cart_spawned = False
tetris_cart_rect  = pygame.Rect(desk_rect.centerx - 9, desk_rect.y + 3, 18, 24)  # On the desk

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
tetris_coin_given  = False  # one-time Tetris win reward
tetris_move_dir    = 0   # -1 left, 1 right, 0 none — held direction for auto-repeat (DAS)
tetris_move_timer  = 0   # ms timestamp for the next auto-repeat shift
TETRIS_DAS_DELAY    = 200  # ms held before auto-repeat kicks in
TETRIS_DAS_INTERVAL = 50   # ms between repeated shifts once auto-repeat is active



















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
    rt_p2 = {"x": WINDOW_RES[0]-200, "y": 470, "vy": 0, "hp": 100, "state": "idle", "dir": -1, "atk_timer": 0, "color": (255, 100, 50)}
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

chi_tv_pacifier_img = None
try:
    chi_tv_pacifier_img = pygame.image.load(get_resource_path(os.path.join("picture", "找Chi_電視_奶嘴_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load Chi TV pacifier image: {e}")
    chi_tv_pacifier_img = None

chi_tv_nopacifier_img = None
try:
    chi_tv_nopacifier_img = pygame.image.load(get_resource_path(os.path.join("picture", "找Chi_電視_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load Chi TV no-pacifier image: {e}")
    chi_tv_nopacifier_img = None

tv_1988_no_remote = None
try:
    tv_1988_no_remote = pygame.image.load(get_resource_path(os.path.join("picture", "1988_黑白電視_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 1988_黑白電視_去背.png: {e}")

tv_1988_with_remote = None
try:
    tv_1988_with_remote = pygame.image.load(get_resource_path(os.path.join("picture", "1988_黑白電視_複雜提示_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 1988_黑白電視_複雜提示_去背.png: {e}")

try:
    sf2_icon = pygame.image.load(
        get_resource_path(os.path.join("picture", "快打旋風_遊戲帶_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 快打旋風_遊戲帶_去背.png: {e}")
    sf2_icon = None

tetris_cart_icon = None
try:
    tetris_cart_icon = pygame.image.load(
        get_resource_path(os.path.join("picture", "俄羅斯方塊_遊戲帶_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 俄羅斯方塊_遊戲帶_去背.png: {e}")

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
bg_bathroom_full = None
try:
    _raw = pygame.image.load(get_resource_path(os.path.join("picture", "2026_廁所_浴缸滿水_T.png"))).convert()
    bg_bathroom_full = pygame.transform.scale(_raw, _HIRES)
except Exception as e:
    print(f"Could not load 2026_廁所_浴缸滿水_T.png: {e}")
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
        get_resource_path(os.path.join("picture", "鏡子_全霧_B_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 鏡子_全霧_B_去背.png: {e}")
cab_img_closed = cab_img_l1 = cab_img_l2 = None
cab_img_l1_empty = cab_img_l2_empty = cab_img_l2_coin = None
for _cab_name, _cab_key in [("客廳櫃_去背.png", "closed"),
                              ("客廳櫃_L1_去背.png", "l1"),
                              ("客廳櫃_L2_去背.png", "l2"),
                              ("客廳櫃_L1_空_去背.png", "l1_empty"),
                              ("客廳櫃_L2_空_去背.png", "l2_empty"),
                              ("客廳櫃_L2_金幣_去背.png", "l2_coin")]:
    try:
        _cimg = pygame.image.load(
            get_resource_path(os.path.join("picture", _cab_name))).convert_alpha()
        if _cab_key == "closed": cab_img_closed = _cimg
        elif _cab_key == "l1":   cab_img_l1 = _cimg
        elif _cab_key == "l2":   cab_img_l2 = _cimg
        elif _cab_key == "l1_empty": cab_img_l1_empty = _cimg
        elif _cab_key == "l2_empty": cab_img_l2_empty = _cimg
        elif _cab_key == "l2_coin": cab_img_l2_coin = _cimg
    except Exception as e:
        print(f"Could not load {_cab_name}: {e}")
flashlight_img = None
flashlight_icon_img = None  # pre-rotated (90° clockwise) + 5x enlarged, for the HUD icon
try:
    flashlight_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "手電筒_去背.png"))).convert_alpha()
    _fl_base = 60 * 5
    flashlight_icon_img = pygame.transform.smoothscale(
        pygame.transform.rotate(flashlight_img, -90), (_fl_base, _fl_base))
except Exception as e:
    print(f"Could not load 手電筒_去背.png: {e}")
key_img = None
try:
    key_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "鑰匙_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 鑰匙_去背.png: {e}")
remote_img = None
try:
    remote_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "遙控器_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 遙控器_去背.png: {e}")

iron_cabinet_locked_img = None
try:
    iron_cabinet_locked_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "2026房間鐵櫃_鎖_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 2026房間鐵櫃_鎖_去背.png: {e}")

iron_cabinet_open_img = None
try:
    iron_cabinet_open_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "2026房間鐵櫃_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 2026房間鐵櫃_去背.png: {e}")

iron_cabinet_coin_img = None
try:
    iron_cabinet_coin_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "2026房間鐵櫃_金幣_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 2026房間鐵櫃_金幣_去背.png: {e}")

iron_cabinet_scare_img = None
try:
    iron_cabinet_scare_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "1988嚇人鐵櫃.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 1988嚇人鐵櫃.png: {e}")

notebook_img = None
try:
    notebook_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "筆記本_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 筆記本_去背.png: {e}")

outdoor_scene_img = None
try:
    outdoor_scene_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "戶外場景_chi.png"))).convert()
except Exception as e:
    print(f"Could not load 戶外場景_chi.png: {e}")

gashapon_img = None
try:
    gashapon_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "扭蛋機_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load 扭蛋機_去背.png: {e}")

gashapon_prize_images = {}
for _gp_name in GASHAPON_PRIZES:
    try:
        gashapon_prize_images[_gp_name] = pygame.image.load(
            get_resource_path(os.path.join("picture", _gp_name))).convert_alpha()
    except Exception as e:
        print(f"Could not load {_gp_name}: {e}")

chi_baby_img = None
try:
    chi_baby_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "Chi寶寶_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load Chi baby image: {e}")
    chi_baby_img = None

chi_pacifier_icon = None
try:
    chi_pacifier_icon = pygame.image.load(
        get_resource_path(os.path.join("picture", "Chi的奶嘴_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load Chi pacifier icon: {e}")
    chi_pacifier_icon = None


chi_baby_img_with_pacifier = None
try:
    chi_baby_img_with_pacifier = pygame.image.load(
        get_resource_path(os.path.join("picture", "Chi寶寶_奶嘴_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load Chi baby with pacifier image: {e}")
    chi_baby_img_with_pacifier = None

coin_img = None
try:
    coin_img = pygame.image.load(
        get_resource_path(os.path.join("picture", "扭蛋硬幣_去背.png"))).convert_alpha()
except Exception as e:
    print(f"Could not load coin image: {e}")
    coin_img = None

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

def draw_cart_icon(surface, rect, img, fallback_color):
    """Draw a cartridge using its real artwork if loaded, else the procedural icon."""
    if img:
        # smoothscale avoids the noisy/wrong-looking colors plain scale() produces
        # when shrinking a large source image down to a tiny rect like this.
        surface.blit(pygame.transform.smoothscale(img, (rect.width, rect.height)), (rect.x, rect.y))
    else:
        draw_cartridge_icon(surface, rect, fallback_color)

def draw_book_icon(surface, rect, color):
    """Draw a book spine with shading, a page edge, and decorative title bands."""
    shadow = tuple(max(0, c - 70) for c in color)
    highlight = tuple(min(255, c + 60) for c in color)
    outline = tuple(max(0, c - 100) for c in color)
    # Spine body
    pygame.draw.rect(surface, color, rect, border_radius=4)
    pygame.draw.rect(surface, shadow, (rect.right - 9, rect.y, 9, rect.height), border_radius=4)
    pygame.draw.rect(surface, highlight, (rect.x, rect.y, 7, rect.height), border_radius=4)
    pygame.draw.rect(surface, outline, rect, 2, border_radius=4)
    # Page edge peeking out at the top
    pygame.draw.rect(surface, (245, 238, 220), (rect.x + 5, rect.y, rect.width - 10, 5))
    pygame.draw.rect(surface, (200, 190, 165), (rect.x + 5, rect.y, rect.width - 10, 5), 1)
    # Decorative gold title bands across the spine
    band_color = (225, 195, 110)
    for frac in (0.22, 0.5, 0.78):
        by = rect.y + int(rect.height * frac)
        band = pygame.Rect(rect.x + 10, by, rect.width - 20, 5)
        pygame.draw.rect(surface, band_color, band)
        pygame.draw.rect(surface, tuple(max(0, c - 70) for c in band_color), band, 1)

def draw_bookshelf_bg(surface, rect):
    """Draw a wood-grain bookshelf frame with a recessed shelf the books stand on."""
    wood = (101, 60, 30)
    grain = (118, 73, 38)
    pygame.draw.rect(surface, wood, rect, border_radius=10)
    for gy in range(rect.y + 14, rect.bottom - 10, 14):
        pygame.draw.line(surface, grain, (rect.x + 12, gy), (rect.right - 12, gy), 1)
    # Recessed cubby where the books sit
    inner = rect.inflate(-32, -130)
    inner.center = (rect.centerx, rect.y + 175)
    pygame.draw.rect(surface, (62, 36, 16), inner, border_radius=6)
    pygame.draw.rect(surface, (40, 22, 10), inner, 3, border_radius=6)
    # Shelf board the books stand on
    shelf_board = pygame.Rect(inner.x, inner.bottom - 4, inner.width, 16)
    pygame.draw.rect(surface, (130, 82, 40), shelf_board)
    pygame.draw.rect(surface, (85, 52, 22), shelf_board, 2)
    pygame.draw.line(surface, (160, 105, 55), (shelf_board.x, shelf_board.y), (shelf_board.right, shelf_board.y), 2)
    # Outer frame
    pygame.draw.rect(surface, (55, 28, 10), rect, 5, border_radius=10)
    return inner

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
        draw_cart_icon(surface, tetris_cart_rect, tetris_cart_icon, (50, 200, 80))

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
    global tetris_move_dir, tetris_move_timer
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
    tetris_move_dir = 0
    tetris_move_timer = 0

def draw_tetris_ui(surface):
    """Render the full Tetris game screen."""
    # Fill the whole screen first — this UI state skips the normal background
    # redraw, so without this the side panel shows stale pixels from whatever
    # was on screen before Tetris started, making the progress text unreadable.
    surface.fill((10, 10, 32))
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
    surface.blit(sf.render(f"{min(tetris_lines_cleared, TETRIS_LINES_WIN)}/{TETRIS_LINES_WIN}", True, (200, 200, 255)), (PX, PY+10))
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
        surface.blit(high_res_inst_font.render("Got a coin! ESC to exit.", True, (200, 255, 200)),
                     high_res_inst_font.render("Got a coin! ESC to exit.", True, (200, 255, 200)).get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2+20)))
        if coin_img:
            _tw_coin = pygame.transform.scale(coin_img, (60, 60))
            surface.blit(_tw_coin, _tw_coin.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 - 120)))

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

def draw_fighter(surface, center_x, center_y, direction, action, hp):
    """Draw Player 1: a chubby otaku fighter — round belly, glasses, black hair.
    Matches the overworld player's look (see draw_retro_player). Faces `direction`."""
    skin   = (255, 200, 150) if hp > 0 else (150, 150, 150)
    shirt  = (80, 120, 200)  if hp > 0 else (95, 95, 105)
    shirt_dk = (60, 95, 170) if hp > 0 else (75, 75, 85)
    pants  = (35, 45, 100)   if hp > 0 else (60, 60, 70)
    hair   = (22, 15, 6)
    eye_dir = direction

    # Smooth triangular bounce while idle/walking so motion reads as continuous
    bounce = 0
    if action in ("idle", "moving"):
        period = 140 if action == "moving" else 380
        amp = 3 if action == "moving" else 1.5
        phase = (pygame.time.get_ticks() % period) / period
        bounce = -round(amp * (1 - abs(phase * 2 - 1)))

    cy = center_y + bounce
    lean = 7 if action == "moving" else (12 if action == "attacking" else 0)
    hx = center_x + eye_dir * lean  # torso/head lean toward facing direction

    # Legs (dark jeans), wider stride while walking
    spread = 9 if action == "moving" else 6
    pygame.draw.rect(surface, pants, (center_x - spread - 6, cy + 24, 13, 24), border_radius=4)
    pygame.draw.rect(surface, pants, (center_x + spread - 7, cy + 24, 13, 24), border_radius=4)

    # Round chubby torso + belly peeking out under the shirt
    pygame.draw.ellipse(surface, shirt, (hx - 27, cy - 38, 54, 64))
    pygame.draw.ellipse(surface, shirt_dk, (hx - 27, cy - 38, 54, 64), 2)
    pygame.draw.ellipse(surface, skin, (hx - 16, cy - 4, 32, 18))

    # Arms
    if action == "attacking":
        pygame.draw.rect(surface, shirt, (hx - 24, cy - 26, 14, 32), border_radius=6)
        pygame.draw.rect(surface, shirt, (hx - 6, cy - 22, 58 * eye_dir, 17), border_radius=7)
        pygame.draw.circle(surface, skin, (hx + 52 * eye_dir, cy - 14), 9)
    elif action == "jumping":
        pygame.draw.ellipse(surface, shirt, (hx - 34, cy - 30, 15, 30))
        pygame.draw.ellipse(surface, shirt, (hx + 19, cy - 30, 15, 30))
        pygame.draw.circle(surface, skin, (hx - 30, cy - 4), 6)
        pygame.draw.circle(surface, skin, (hx + 30, cy - 4), 6)
    else:
        pygame.draw.ellipse(surface, shirt, (hx - 33, cy - 22, 14, 32))
        pygame.draw.ellipse(surface, shirt, (hx + 19, cy - 22, 14, 32))
        pygame.draw.circle(surface, skin, (hx - 29, cy + 7), 6)
        pygame.draw.circle(surface, skin, (hx + 29, cy + 7), 6)

    # Head: round face, full black hair, thick glasses
    head_y = cy - (50 if action == "jumping" else 58)
    pygame.draw.ellipse(surface, skin, (hx - 17, head_y - 16, 34, 30))
    pygame.draw.ellipse(surface, hair, (hx - 18, head_y - 21, 36, 18))
    pygame.draw.rect(surface, hair, (hx - 18, head_y - 12, 7, 16))
    pygame.draw.rect(surface, hair, (hx + 11, head_y - 12, 7, 16))

    gx = hx + eye_dir * 2
    for gd in (-1, 1):
        lens = pygame.Rect(gx + gd * 13 - 5, head_y - 5, 11, 9)
        pygame.draw.rect(surface, (210, 230, 245), lens, border_radius=2)
        pygame.draw.rect(surface, (25, 25, 25), lens, 2, border_radius=2)
        pygame.draw.circle(surface, (0, 0, 0), (lens.centerx + eye_dir, lens.centery), 2)
    pygame.draw.line(surface, (25, 25, 25), (gx - 3, head_y - 1), (gx + 3, head_y - 1), 2)

    if action == "hurt":
        pygame.draw.line(surface, (220, 60, 60), (hx - 8, head_y + 7), (hx + 8, head_y + 10), 2)
        pygame.draw.line(surface, (220, 60, 60), (hx - 8, head_y + 10), (hx + 8, head_y + 7), 2)

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

        if tetris_cart_spawned and player_rect.colliderect(tetris_proximity_rect):
            prompt_label = "Cartridge"
            prompt_label_rect = tetris_cart_rect
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
            elif calendar_date != DATE_1988 and player_rect.colliderect(cabinet_proximity_rect):
                prompt_label = "Cabinet"
                prompt_label_rect = cabinet_rect
            elif calendar_date == DATE_2026:
                if player_rect.colliderect(main_door_rect.inflate(5, 100)):
                    prompt_label = "Front Door"
                    prompt_label_rect = main_door_rect

        # Chi baby interaction check (1994-10-23 specific)
        if calendar_date == DATE_1994_10_23 and "Chi的奶嘴_去背.png" in inventory and not chi_baby_has_pacifier:
            chi_baby_rect = pygame.Rect(chi_baby_x - 10, chi_baby_y - 10, 20, 20)
            chi_baby_proximity = chi_baby_rect.inflate(80, 80)  # 80 pixel proximity range
            if player_rect.colliderect(chi_baby_proximity):
                prompt_label = "Chi Baby"
                prompt_label_rect = chi_baby_rect

    elif current_scene == "bedroom":
        if player_rect.colliderect(bedroom_door_prox):
            prompt_label = "Living Room"
            prompt_label_rect = bedroom_door_rect
        elif player_rect.colliderect(bookshelf_prox):
            prompt_label = "Bookshelf"
            prompt_label_rect = bookshelf_rect
        elif calendar_date != DATE_1988 and player_rect.colliderect(computer_prox):
            prompt_label = "Computer"
            prompt_label_rect = computer_desk_rect
        elif calendar_date != DATE_1988 and player_rect.colliderect(bed_rect.inflate(16, 16)):
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
    # Cartridge always shows above to avoid blocking calendar
    if prompt_label == "Cartridge":
        ly = max(_th + 4, _obj_top_px - 6)
    elif _obj_top_px < _th + 10:
        # Object is near top — show label BELOW the object
        ly = _obj_bot_px + _th + 6
    else:
        ly = max(_th + 4, _obj_top_px - 6)
    bg = pygame.Surface((txt.get_width() + 8, _th + 4), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 160))
    surface.blit(bg, bg.get_rect(midbottom=(lx, ly)))
    surface.blit(txt, txt.get_rect(midbottom=(lx, ly - 2)))


def _cab_current_img():
    """Return the cabinet PNG matching the currently selected drawer's state."""
    has_flashlight_in_inv = "Flashlight" in inventory
    has_remote_in_inv = "Remote" in inventory

    if cabinet_selection == 0:
        if cabinet_drawer1_open:
            return (cab_img_l1_empty if has_flashlight_in_inv else cab_img_l1) or cab_img_closed
        return cab_img_closed
    else:
        if cabinet_drawer2_open:
            if not has_remote_in_inv:
                return cab_img_l2 or cab_img_closed
            elif not cabinet_l2_coin_taken:
                return cab_img_l2_coin or cab_img_l2_empty or cab_img_closed
            else:
                return cab_img_l2_empty or cab_img_closed
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

    # Chi Baby boundary (if applicable - green)
    if current_scene == "living_room" and calendar_date == DATE_1994_10_23:
        chi_bx0, chi_bx1, chi_by0, chi_by1 = ROOM_BOUNDS.get(current_scene, (40, 268, 75, 195))
        chi_bsr = (int(chi_bx0 * _SX), int(chi_by0 * _SY),
                   int((chi_bx1 - chi_bx0) * _SX), int((chi_by1 - chi_by0) * _SY))
        pygame.draw.rect(surface, (0, 255, 0), chi_bsr, 2)
        surface.blit(_font.render(f"Chi Baby bounds ({chi_bx0},{chi_bx1},{chi_by0},{chi_by1})", True, (0, 255, 0)),
                     (chi_bsr[0], chi_bsr[1] + chi_bsr[3] + 2))
        # Draw Chi Baby current position
        chi_pos_sr = (int(chi_baby_x * _SX), int(chi_baby_y * _SY))
        pygame.draw.circle(surface, (0, 255, 100), chi_pos_sr, 5)
        surface.blit(_font.render(f"Chi({chi_baby_x},{chi_baby_y})", True, (0, 255, 100)),
                     (chi_pos_sr[0] - 40, chi_pos_sr[1] - 16))

    # Legend
    pygame.draw.rect(surface, (255, 0, 0),    (8,  8, 12, 12), 2)
    surface.blit(_font.render("F1 collision", True, (255, 200, 0)), (24,  6))
    pygame.draw.rect(surface, (80, 140, 255), (8, 24, 12, 12), 2)
    surface.blit(_font.render("F1 bounds",    True, (80, 200, 255)), (24, 22))
    pygame.draw.rect(surface, (0, 255, 0),    (8, 40, 12, 12), 2)
    surface.blit(_font.render("F1 chi baby",  True, (0, 255, 100)), (24, 38))


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
        _content = _crop.get_bounding_rect()  # trim transparent padding baked into the source art
        if _content.width > 0 and _content.height > 0:
            _crop = _crop.subsurface(_content)
        _cw, _ch = _crop.get_size()
        _display_h = _ch * 9   # 3x larger than previous (which was _half_h * 3)
        _display_w = int(_cw * _display_h / _ch)
        _max_h = WINDOW_RES[1] - 60
        if _display_h > _max_h:
            _display_h = _max_h
            _display_w = int(_cw * _display_h / _ch)
        if _display_w > WINDOW_RES[0] // 2:
            _display_w = WINDOW_RES[0] // 2
            _display_h = int(_ch * _display_w / _cw)
        _bw = _display_w
        _bust = pygame.transform.scale(_crop, (_display_w, _display_h))
        _by = WINDOW_RES[1] - 98 - _display_h
        if _by < 0:
            _by = 0
        # Flush against the right edge now that padding is trimmed (closest to edge without exceeding it)
        surface.blit(_bust, (WINDOW_RES[0] - _display_w, _by))
    _margin = 15
    _box_w = min(400, WINDOW_RES[0] - _bw - _margin * 3)
    if _box_w < 200:
        _box_w = 200
    _box_x = WINDOW_RES[0] - _bw - _box_w - _margin
    if _box_x < _margin:
        _box_x = _margin

    # Word-wrap dialogue text so it always stays within the box bounds
    _avail_w = _box_w - 32
    _lines = []
    _cur = ""
    for _word in dialogue_text.split(" "):
        _test = (_cur + " " + _word).strip()
        if cal_day_font.size(_test)[0] <= _avail_w or not _cur:
            _cur = _test
        else:
            _lines.append(_cur)
            _cur = _word
    if _cur:
        _lines.append(_cur)
    _line_h = cal_day_font.get_linesize()
    _footer_h = 64  # room for the Yes/No or continue prompt
    _box_h = max(165, 20 + len(_lines) * _line_h + _footer_h)
    _box_y = WINDOW_RES[1] - 98 - _box_h

    pygame.draw.rect(surface, (20, 20, 35), (_box_x, _box_y, _box_w, _box_h), border_radius=10)
    pygame.draw.rect(surface, (120, 160, 220), (_box_x, _box_y, _box_w, _box_h), 2, border_radius=10)
    for _i, _line in enumerate(_lines):
        _txt = cal_day_font.render(_line, True, (220, 220, 255))
        surface.blit(_txt, (_box_x + 16, _box_y + 20 + _i * _line_h))
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
    global iron_cabinet_scare_start
    dialogue_triggered = True
    if obj == "tv":
        ui_state = "tv"
        dialogue_triggered = False
    elif obj == "cabinet":
        ui_state = "cabinet"
        dialogue_triggered = False
    elif obj == "calendar":
        ui_state = "calendar"
        dialogue_triggered = False
    elif obj == "cartridge":
        if "Tetris Cartridge" not in inventory:
            inventory.append("Tetris Cartridge")
            cabinet_message = "Got Tetris Cartridge from the desk!"; _msg_timer = 180
        tetris_cart_spawned = False
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
    elif obj == "bed":
        if calendar_date == DATE_2026:
            ui_state = "notebook"
        dialogue_triggered = False
    elif obj == "bookshelf":
        ui_state = "bookshelf"
        dialogue_triggered = False
    elif obj == "iron_cabinet":
        if calendar_date == DATE_1988:
            ui_state = "iron_cabinet_scare"
            iron_cabinet_scare_start = pygame.time.get_ticks()
        else:
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
    elif obj == "chi_baby":
        global chi_baby_has_pacifier, coin_items
        if "Chi的奶嘴_去背.png" in inventory:
            inventory.remove("Chi的奶嘴_去背.png")
            chi_baby_has_pacifier = True
            dialogue_triggered = False
            prompt_label = ""
            # Drop coin
            coin_data = {
                'x': chi_baby_x + 15,  # Chi baby side (right)
                'y': chi_baby_y,       # Chi baby height
                'vy': -3,              # Initial upward velocity
                'lifetime': 300,       # Coin existence time (frames)
                'name': '扭蛋硬幣_去背.png'  # Collectible item name
            }
            coin_items.append(coin_data)


# Inventory bar helper
# -------------------------------------------------------------------------

# Maps number-row keys to slot indices: 1-9 -> 0-8, 0 -> 9 (slot 10)
INV_SLOT_KEYS = {
    pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2, pygame.K_4: 3, pygame.K_5: 4,
    pygame.K_6: 5, pygame.K_7: 6, pygame.K_8: 7, pygame.K_9: 8, pygame.K_0: 9,
}

def _toggle_inv_slot(idx):
    """Toggle selection of an inventory slot (number-key press)."""
    global selected_inv_slot, last_inv_slot_key
    selected_inv_slot = idx if last_inv_slot_key != idx else -1
    last_inv_slot_key = idx if selected_inv_slot == idx else -1

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
                if key_img:
                    icon = pygame.transform.smoothscale(key_img, (slot_size + 10, slot_size - 8))
                    screen.blit(icon, (sr.x - 5, sr.y + 4))
                else:
                    draw_key_icon(screen, sr.centerx, sr.centery, 50)
            elif item == "MysteryCube":
                draw_mystery_cube_icon(screen, sr.centerx, sr.centery, 44)
            elif item == "SF2 Cartridge":
                draw_cart_icon(screen, sr.inflate(-10, -10), sf2_icon, (220, 80, 30))
            elif item == "Tetris Cartridge":
                draw_cart_icon(screen, sr.inflate(-10, -10), tetris_cart_icon, (50, 200, 80))
            elif item == "Remote":
                if remote_img:
                    icon = pygame.transform.scale(remote_img, (60, 60))
                    screen.blit(icon, (sr.centerx - 30, sr.centery - 30))
                else:
                    pygame.draw.rect(screen, (60, 60, 180), sr.inflate(-12, -8))
                    pygame.draw.rect(screen, (100, 100, 220), sr.inflate(-12, -8), 2)
            elif item in gashapon_prize_images:
                icon = pygame.transform.smoothscale(gashapon_prize_images[item], (slot_size + 10, slot_size - 8))
                screen.blit(icon, (sr.x - 5, sr.y + 4))
            elif item == "Chi的奶嘴_去背.png":
                if chi_pacifier_icon:
                    icon = pygame.transform.smoothscale(chi_pacifier_icon, (slot_size + 10, slot_size - 8))
                    screen.blit(icon, (sr.x - 5, sr.y + 4))
                else:
                    pygame.draw.circle(screen, (255, 200, 220), sr.center, 20)
                    pygame.draw.circle(screen, (200, 150, 180), sr.center, 20, 2)
            elif item == "扭蛋硬幣_去背.png":
                if coin_img:
                    icon = pygame.transform.smoothscale(coin_img, (slot_size + 10, slot_size - 8))
                    screen.blit(icon, (sr.x - 5, sr.y + 4))
                else:
                    pygame.draw.circle(screen, (255, 215, 0), sr.center, 20)
                    pygame.draw.circle(screen, (218, 165, 32), sr.center, 20, 2)
            elif item in ("Strange Cube 2", "MysteryCube"):
                draw_mystery_cube_icon(screen, sr.centerx, sr.centery, 44)
            else:
                pygame.draw.rect(screen, (150, 80, 200), sr.inflate(-14, -14))
        # Slot number label
        num_label = font.render(str(i + 1), True, (180, 180, 180))
        screen.blit(num_label, num_label.get_rect(centerx=sr.centerx, top=sr.bottom + 3))


# Pre-game screens
# -------------------------------------------------------------------------

def draw_title_screen(surface):
    surface.fill((10, 10, 25))
    pygame.draw.rect(surface, (60, 60, 120), (20, 20, WINDOW_RES[0] - 40, WINDOW_RES[1] - 40), 4, border_radius=12)

    title = high_res_big_font.render("RETRO 2D GAME", True, (255, 220, 80))
    surface.blit(title, title.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 - 80)))

    subtitle = high_res_inst_font.render("A Time-Traveling Story", True, (180, 200, 255))
    surface.blit(subtitle, subtitle.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 - 20)))

    if (pygame.time.get_ticks() // 500) % 2 == 0:
        prompt = high_res_inst_font.render("Press SPACE to Start", True, (255, 255, 255))
        surface.blit(prompt, prompt.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 + 80)))

def draw_instructions_screen(surface):
    surface.fill((10, 10, 25))
    pygame.draw.rect(surface, (60, 60, 120), (20, 20, WINDOW_RES[0] - 40, WINDOW_RES[1] - 40), 4, border_radius=12)

    heading = high_res_big_font.render("HOW TO PLAY", True, (255, 220, 80))
    surface.blit(heading, heading.get_rect(center=(WINDOW_RES[0]//2, 90)))

    controls = [
        ("Arrow Keys / WASD", "Move around"),
        ("SPACE", "Interact / Confirm / Select Yes"),
        ("1 - 9, 0", "Select an item in your inventory"),
        ("ESC", "Cancel / Close a menu"),
    ]
    _ly = 200
    for key, desc in controls:
        key_surf = cal_day_font.render(key, True, (255, 220, 100))
        desc_surf = cal_day_font.render(desc, True, (220, 220, 220))
        surface.blit(key_surf, (WINDOW_RES[0]//2 - 280, _ly))
        surface.blit(desc_surf, (WINDOW_RES[0]//2 - 20, _ly))
        _ly += 56

    if (pygame.time.get_ticks() // 500) % 2 == 0:
        prompt = high_res_inst_font.render("Press SPACE to Begin", True, (255, 255, 255))
        surface.blit(prompt, prompt.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 60)))

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
    # On 8/8, Tetris uses TV's collision/proximity rect (TV not available that day)
    tetris_proximity_rect   = tv_proximity_rect if (calendar_date.month == 8 and calendar_date.day == 8) else calendar_rect.inflate(5, 110)
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

        elif event.type == pygame.TEXTINPUT:
            # Handle text input for the iron cabinet password lock
            if ui_state == "iron_cabinet_password":
                if len(cabinet_password_input) < len(cabinet_password_target):
                    cabinet_password_input = cabinet_password_input[:cabinet_password_edit_pos] + event.text.upper() + cabinet_password_input[cabinet_password_edit_pos:]
                    cabinet_password_edit_pos += 1

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

            if ui_state == "title":
                if event.key == pygame.K_SPACE:
                    ui_state = "instructions"

            elif ui_state == "instructions":
                if event.key == pygame.K_SPACE:
                    ui_state = "game"

            elif ui_state == "game":
                if event.key in INV_SLOT_KEYS:
                    _toggle_inv_slot(INV_SLOT_KEYS[event.key])

                elif event.key == pygame.K_SPACE:
                    _obj = ""
                    if current_scene == "living_room":
                        is_1988_dark = calendar_date == DATE_1988 and not room_lights_on
                        has_flashlight_selected = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Flashlight"

                        if tetris_cart_spawned and player_rect.colliderect(tetris_proximity_rect):
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
                                elif calendar_date != DATE_1988 and player_rect.colliderect(cabinet_proximity_rect):
                                    _obj = "cabinet"
                            if calendar_date == DATE_2026:
                                if player_rect.colliderect(main_door_rect.inflate(5, 100)):
                                    _obj = "frontdoor"

                        # Chi baby interaction (1994-10-23 specific)
                        if calendar_date == DATE_1994_10_23 and "Chi的奶嘴_去背.png" in inventory and not chi_baby_has_pacifier:
                            chi_baby_rect = pygame.Rect(chi_baby_x - 10, chi_baby_y - 10, 20, 20)
                            chi_baby_proximity = chi_baby_rect.inflate(80, 80)
                            if player_rect.colliderect(chi_baby_proximity):
                                _obj = "chi_baby"

                    elif current_scene == "bedroom":
                        if player_rect.colliderect(bedroom_door_prox):
                            _obj = "livingroom"
                        elif player_rect.colliderect(bookshelf_prox):
                            _obj = "bookshelf"
                        elif calendar_date != DATE_1988 and player_rect.colliderect(computer_prox):
                            _obj = "computer"
                        elif calendar_date != DATE_1988 and player_rect.colliderect(bed_rect.inflate(16, 16)):
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
                    if _obj == "iron_cabinet" and iron_cabinet_unlocked:
                        # Already unlocked — go straight in, no need to re-confirm opening it
                        _trigger_action(_obj)
                    elif _obj and _obj in DIALOGUE_MAP and not dialogue_active:
                        dialogue_active = True
                        dialogue_object = _obj
                        dialogue_text, dialogue_has_choices = DIALOGUE_MAP[_obj]
                        dialogue_choice = 0
                        
            elif ui_state == "computer_idle":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif event.key in INV_SLOT_KEYS:
                    _toggle_inv_slot(INV_SLOT_KEYS[event.key])
                elif event.key == pygame.K_SPACE:
                    selected_item = inventory[selected_inv_slot] if selected_inv_slot >= 0 and selected_inv_slot < len(inventory) else None
                    if selected_item == "SF2 Cartridge":
                        ui_state = "computer"
                        init_rt_fighter()
                        fighter_message = ""
                    elif selected_item == "Tetris Cartridge":
                        ui_state = "tetris"
                        init_tetris()

            elif ui_state == "computer":
                # Always allow number key selection and escape
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif event.key in INV_SLOT_KEYS:
                    _toggle_inv_slot(INV_SLOT_KEYS[event.key])
                # Other keys depend on fighter state
                elif fighter_state == "fighting":
                    # Attacks/jumps only start when grounded — starting an attack
                    # mid-air used to leave the fighter stuck unable to move until
                    # landing, since recovery to "idle" required being grounded.
                    if event.key == pygame.K_SPACE and rt_p1["state"] not in ("attacking", "jumping") and rt_p1["y"] >= 470:
                        rt_p1["atk_timer"] = 15
                        rt_p1["state"] = "attacking"
                        # Damage is applied by the per-frame hitbox check below,
                        # not here — doing it in both places caused double damage.
                    elif event.key == pygame.K_UP and rt_p1["state"] != "attacking" and rt_p1["y"] >= 470:
                        rt_p1["vy"] = -15
                        rt_p1["state"] = "jumping"
                elif fighter_state == "round_over":
                    if event.key == pygame.K_SPACE:
                        rt_p1["hp"] = 100
                        rt_p2["hp"] = 100
                        rt_p1["state"] = "idle"
                        rt_p2["state"] = "idle"
                        rt_p1["x"] = 200
                        rt_p2["x"] = WINDOW_RES[0] - 200
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
                if event.key == pygame.K_SPACE:
                    if tv_channel == 2:  # Chi pacifier channel
                        if "Chi的奶嘴_去背.png" not in inventory:
                            inventory.append("Chi的奶嘴_去背.png")
                            print(f"[DEBUG] Got pacifier! Inventory now: {inventory}")
                    else:
                        ui_state = "game"
                        tv_channel = 0  # reset channel when closing
                elif event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                    tv_channel = 0  # reset channel when closing
                elif event.key in INV_SLOT_KEYS:
                    # Handle inventory slot selection even in TV UI
                    _toggle_inv_slot(INV_SLOT_KEYS[event.key])
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    # Only allow channel switching if remote is selected
                    selected_remote = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Remote"
                    if selected_remote:
                        if event.key == pygame.K_UP:
                            tv_channel = (tv_channel - 1) % 3
                        elif event.key == pygame.K_DOWN:
                            tv_channel = (tv_channel + 1) % 3

            elif ui_state == "cabinet":
                if event.key == pygame.K_ESCAPE:
                    cabinet_item_pending = None
                    ui_state = "game"
                    dialogue_triggered = False
                elif event.key in INV_SLOT_KEYS:
                    # Handle inventory slot selection even in cabinet UI
                    _toggle_inv_slot(INV_SLOT_KEYS[event.key])
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
                        elif cabinet_item_pending == "扭蛋硬幣_去背.png":
                            cabinet_l2_coin_taken = True
                        cabinet_message = "Got a coin!" if cabinet_item_pending == "扭蛋硬幣_去背.png" else f"Got {cabinet_item_pending}!"
                        _msg_timer = 180
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
                        # Must select key in inventory to open drawer 2 (only needed the first time)
                        if not cabinet_drawer2_open:
                            has_key_selected = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Key"
                            if not has_key:
                                cabinet_message = "This drawer is locked. Need a key."; _msg_timer = 180
                            elif not has_key_selected:
                                cabinet_message = "Need to select the key in inventory!"; _msg_timer = 180
                            else:
                                cabinet_drawer2_open = True
                                inventory.remove("Key")
                                selected_inv_slot = -1
                                last_inv_slot_key = -1
                        if cabinet_drawer2_open:
                            if "Remote" not in inventory:
                                cabinet_item_pending = "Remote"
                                cabinet_message = "There's a remote inside! SPACE to take it."; _msg_timer = 180
                            elif not cabinet_l2_coin_taken:
                                cabinet_item_pending = "扭蛋硬幣_去背.png"
                                cabinet_message = "There's a coin inside! SPACE to take it."; _msg_timer = 180
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
                elif event.key in INV_SLOT_KEYS:
                    # Handle inventory slot selection in tetris (always allowed)
                    _toggle_inv_slot(INV_SLOT_KEYS[event.key])
                elif tetris_game_over or tetris_won:
                    if event.key == pygame.K_SPACE:
                        init_tetris()
                else:
                    if event.key == pygame.K_LEFT:
                        if tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x - 1, tetris_piece_y):
                            tetris_piece_x -= 1
                        tetris_move_dir = -1
                        tetris_move_timer = pygame.time.get_ticks() + TETRIS_DAS_DELAY
                    elif event.key == pygame.K_RIGHT:
                        if tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x + 1, tetris_piece_y):
                            tetris_piece_x += 1
                        tetris_move_dir = 1
                        tetris_move_timer = pygame.time.get_ticks() + TETRIS_DAS_DELAY
                    elif event.key == pygame.K_UP:
                        nr = tetris_piece_rot + 1
                        # Simple wall kick: nudge sideways if rotating in place would
                        # push the piece out of bounds (fixes "can't rotate near a wall").
                        for _kick_dx in (0, 1, -1, 2, -2):
                            if tetris_valid(tetris_board, tetris_piece_type, nr, tetris_piece_x + _kick_dx, tetris_piece_y):
                                tetris_piece_rot = nr
                                tetris_piece_x += _kick_dx
                                break
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
                            if not tetris_coin_given:
                                tetris_coin_given = True
                                inventory.append("扭蛋硬幣_去背.png")
                        else:
                            tetris_piece_type = tetris_next_type
                            tetris_next_type = random.randint(0, len(TETRIS_SHAPES)-1)
                            tetris_piece_rot = 0
                            tetris_piece_x = TETRIS_W // 2 - 2
                            tetris_piece_y = 0
                            if not tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y):
                                tetris_game_over = True
                        tetris_fall_time = pygame.time.get_ticks()

            elif ui_state == "notebook":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"

            elif ui_state == "outdoor":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                    outdoor_message_shown = False
                elif event.key == pygame.K_SPACE:
                    outdoor_message_shown = True

            elif ui_state == "iron_cabinet_scare":
                if event.key in (pygame.K_ESCAPE, pygame.K_SPACE):
                    ui_state = "game"

            elif ui_state == "iron_cabinet":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif event.key == pygame.K_SPACE and not iron_cabinet_unlocked:
                    # Start password entry to unlock the cabinet
                    cabinet_password_input = ""
                    cabinet_password_edit_pos = 0
                    cabinet_password_feedback = ""
                    ui_state = "iron_cabinet_password"
                    # Reset SDL's text-input composition state — without this, the
                    # very last keystroke typed can silently fail to fire a TEXTINPUT
                    # event (a known SDL/IME quirk) unless another key is pressed first.
                    pygame.key.stop_text_input()
                    pygame.key.start_text_input()
                elif event.key == pygame.K_SPACE and iron_cabinet_unlocked and not iron_cabinet_coin_taken:
                    # Take the coin left inside the cabinet
                    inventory.append("扭蛋硬幣_去背.png")
                    iron_cabinet_coin_taken = True
                    cabinet_message = "Got a coin!"; _msg_timer = 180
                elif event.key == pygame.K_UP and iron_cabinet_unlocked and iron_cabinet_coin_taken:
                    ui_state = "gashapon"
                elif event.key in INV_SLOT_KEYS:
                    # Handle inventory slot selection in iron cabinet
                    _toggle_inv_slot(INV_SLOT_KEYS[event.key])

            elif ui_state == "iron_cabinet_password":
                if event.key == pygame.K_ESCAPE:
                    cabinet_password_edit_pos = 0
                    ui_state = "iron_cabinet"
                elif event.key == pygame.K_BACKSPACE:
                    # Delete character before cursor
                    if cabinet_password_edit_pos > 0:
                        cabinet_password_input = cabinet_password_input[:cabinet_password_edit_pos-1] + cabinet_password_input[cabinet_password_edit_pos:]
                        cabinet_password_edit_pos -= 1
                elif event.key == pygame.K_DELETE:
                    # Delete character at cursor
                    if cabinet_password_edit_pos < len(cabinet_password_input):
                        cabinet_password_input = cabinet_password_input[:cabinet_password_edit_pos] + cabinet_password_input[cabinet_password_edit_pos+1:]
                elif event.key == pygame.K_LEFT:
                    cabinet_password_edit_pos = max(0, cabinet_password_edit_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    cabinet_password_edit_pos = min(len(cabinet_password_input), cabinet_password_edit_pos + 1)
                elif event.key == pygame.K_RETURN:
                    if cabinet_password_input == cabinet_password_target:
                        iron_cabinet_unlocked = True
                        cabinet_password_input = ""
                        cabinet_password_edit_pos = 0
                        cabinet_message = "Cabinet unlocked!"; _msg_timer = 180
                        ui_state = "iron_cabinet"
                    else:
                        cabinet_password_feedback = "Incorrect! Try again."
                        cabinet_password_feedback_timer = 120  # 2 seconds
                        cabinet_password_input = ""
                        cabinet_password_edit_pos = 0

            elif ui_state == "gashapon":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "iron_cabinet"
                elif event.key in INV_SLOT_KEYS:
                    _toggle_inv_slot(INV_SLOT_KEYS[event.key])
                elif event.key == pygame.K_SPACE:
                    # Insert the selected coin to dispense a random prize (no duplicates)
                    coin_selected = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "扭蛋硬幣_去背.png"
                    if coin_selected:
                        _remaining_prizes = [p for p in GASHAPON_PRIZES if p not in inventory]
                        if _remaining_prizes:
                            inventory.pop(selected_inv_slot)
                            selected_inv_slot = -1
                            last_inv_slot_key = -1
                            gashapon_last_prize = random.choice(_remaining_prizes)
                            inventory.append(gashapon_last_prize)
                            gashapon_feedback = "Got it!"
                            gashapon_feedback_timer = 180
                        else:
                            gashapon_feedback = "You already have them all!"
                            gashapon_feedback_timer = 120
                    elif "扭蛋硬幣_去背.png" in inventory:
                        gashapon_feedback = "Select a coin first!"
                        gashapon_feedback_timer = 120
                    else:
                        gashapon_feedback = "Need a coin! Insert one to play."
                        gashapon_feedback_timer = 120

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

                    if bookshelf_order == ["Green", "Blue", "Red"] and not bookshelf_unlocked:
                        bookshelf_unlocked = True

            elif ui_state == "main_door":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif event.key == pygame.K_SPACE:
                    if all(door_puzzle_state):
                        ui_state = "outdoor"
                    else:
                        # Insert one of the 4 gashapon prizes into its matching slot
                        for i, _prize in enumerate(GASHAPON_PRIZES):
                            if not door_puzzle_state[i] and _prize in inventory:
                                inventory.remove(_prize)
                                door_puzzle_state[i] = True
                                break
                        if all(door_puzzle_state):
                            ui_state = "outdoor"

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

    # Pre-game screens (no world/player to update yet)
    if ui_state == "title":
        draw_title_screen(screen)
        pygame.display.flip()
        clock.tick(60)
        continue
    if ui_state == "instructions":
        draw_instructions_screen(screen)
        pygame.display.flip()
        clock.tick(60)
        continue

    # Player movement
    keys = pygame.key.get_pressed()
    old_x, old_y = player_x, player_y

    if ui_state == "game" and not dialogue_active:
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
    elif dialogue_active:
        player_moving = False

    # Chi baby movement (only on 1994-10-23, living_room, and not has pacifier)
    if current_scene == "living_room" and calendar_date == DATE_1994_10_23 and not chi_baby_has_pacifier:
        chi_baby_change_dir_timer -= 1
        if chi_baby_change_dir_timer <= 0:
            chi_baby_dir_x = random.choice([-1, 0, 1])
            chi_baby_dir_y = random.choice([-1, 0, 1])
            chi_baby_change_dir_timer = random.randint(30, 80)

        # Update position
        chi_baby_x += chi_baby_dir_x * chi_baby_speed
        chi_baby_y += chi_baby_dir_y * chi_baby_speed

        # Use ROOM_BOUNDS for boundary check (same as player character)
        MIN_X, MAX_X, MIN_Y, MAX_Y = ROOM_BOUNDS.get(current_scene, (40, 268, 75, 195))

        # X boundary check
        if chi_baby_x <= MIN_X:
            chi_baby_x = MIN_X
            chi_baby_dir_x = 1
        elif chi_baby_x >= MAX_X:
            chi_baby_x = MAX_X
            chi_baby_dir_x = -1

        # Y boundary check
        if chi_baby_y <= MIN_Y:
            chi_baby_y = MIN_Y
            chi_baby_dir_y = 1
        elif chi_baby_y >= MAX_Y:
            chi_baby_y = MAX_Y
            chi_baby_dir_y = -1

    # Recalculate player_rect for coin collision detection (must be done before coin update)
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # Update coin items
    if current_scene == "living_room" and calendar_date == DATE_1994_10_23:
        for coin in coin_items[:]:
            coin['y'] += coin['vy']
            coin['vy'] += 0.2  # Gravity
            coin['lifetime'] -= 1

            coin_rect = pygame.Rect(coin['x'] - 8, coin['y'] - 8, 16, 16)
            collected = player_rect.colliderect(coin_rect)
            expired = coin['lifetime'] <= 0 or coin['y'] >= 190

            # Coin always ends up in inventory, whether caught mid-fall or not
            if collected or expired:
                inventory.append(coin['name'])
                coin_items.remove(coin)

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
                if dist > 0: rt_p2["x"] += 3; rt_p2["dir"] = 1
                else: rt_p2["x"] -= 3; rt_p2["dir"] = -1
                if rt_p2["y"] >= 470: rt_p2["state"] = "moving"
            elif abs(dist) <= 65 and rt_p2["atk_timer"] == 0 and rt_p2["y"] >= 470 and random.random() < 0.07:
                rt_p2["atk_timer"] = 16
                rt_p2["state"] = "attacking"
                # Damage is applied by the per-frame hitbox check below, not here.
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
                if p["atk_timer"] == 0:
                    # Always resolve to a valid state so an attack can never get
                    # stuck mid-animation (e.g. if knocked airborne while attacking).
                    p["state"] = "idle" if p["y"] >= 470 else "jumping"
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
                    if not tetris_coin_given:
                        tetris_coin_given = True
                        inventory.append("扭蛋硬幣_去背.png")
                else:
                    tetris_piece_type = tetris_next_type
                    tetris_next_type = random.randint(0, len(TETRIS_SHAPES)-1)
                    tetris_piece_rot = 0
                    tetris_piece_x = TETRIS_W // 2 - 2
                    tetris_piece_y = 0
                    if not tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x, tetris_piece_y):
                        tetris_game_over = True
            tetris_fall_time = now

    # Tetris left/right auto-repeat while a direction key is held down (DAS)
    if ui_state == "tetris" and not tetris_game_over and not tetris_won and tetris_move_dir != 0:
        _tetris_keys = pygame.key.get_pressed()
        if tetris_move_dir == -1 and not _tetris_keys[pygame.K_LEFT]:
            tetris_move_dir = 0
        elif tetris_move_dir == 1 and not _tetris_keys[pygame.K_RIGHT]:
            tetris_move_dir = 0
        elif pygame.time.get_ticks() >= tetris_move_timer:
            if tetris_valid(tetris_board, tetris_piece_type, tetris_piece_rot, tetris_piece_x + tetris_move_dir, tetris_piece_y):
                tetris_piece_x += tetris_move_dir
            tetris_move_timer = pygame.time.get_ticks() + TETRIS_DAS_INTERVAL

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

    # Tetris cartridge spawn (Any year, 8/8 — requires the Remote first)
    if calendar_date.month == 8 and calendar_date.day == 8:
        if "Tetris Cartridge" not in inventory and "Remote" in inventory:
            tetris_cart_spawned = True
        else:
            tetris_cart_spawned = False
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

        if fl_active and flashlight_icon_img:
            _fl_size = flashlight_icon_img.get_width()
            _fl_x, _fl_y = 15, WINDOW_RES[1] - _fl_size - 115
            _fl_bg = pygame.Surface((_fl_size + 10, _fl_size + 10), pygame.SRCALPHA)
            _fl_bg.fill((0, 0, 0, 140))
            screen.blit(_fl_bg, (_fl_x - 5, _fl_y - 5))
            screen.blit(flashlight_icon_img, (_fl_x, _fl_y))

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

        # Handle TV UI overlay for 1988
        if ui_state == "tv":
            current_tv_img = None
            selected_remote = selected_inv_slot >= 0 and selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Remote"
            if selected_remote and tv_1988_with_remote:
                current_tv_img = tv_1988_with_remote
            elif tv_1988_no_remote:
                current_tv_img = tv_1988_no_remote

            if current_tv_img:
                _tw = int(current_tv_img.get_width() * 0.3)
                _th = int(current_tv_img.get_height() * 0.3)
                _tx = (WINDOW_RES[0] - _tw) // 2
                _ty = (WINDOW_RES[1] - _th) // 2
                screen.blit(pygame.transform.scale(current_tv_img, (_tw, _th)), (_tx, _ty))

                if selected_remote and remote_img:
                    _rw = int(remote_img.get_width() * 0.2)
                    _rh = int(remote_img.get_height() * 0.2)
                    _rx = WINDOW_RES[0] - _rw
                    _ry = WINDOW_RES[1] // 2 - _rh // 2
                    screen.blit(pygame.transform.scale(remote_img, (_rw, _rh)), (_rx, _ry))

            if selected_remote:
                inst = high_res_inst_font.render("Up/Down: Change Channel | SPACE/ESC: Close", True, (200, 200, 200))
            else:
                inst = high_res_inst_font.render("SPACE or ESC to close  (選擇遙控器可轉台)", True, (200, 200, 200))
            screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

        pygame.display.flip()
        clock.tick(60)
        continue

    # ---- BACKGROUND PHASE ----
    _use_hires_bg = None
    if current_scene == "living_room":
        if calendar_date == DATE_2026 and bg_living:
            _use_hires_bg = bg_living
        elif calendar_date == DATE_1988 and bg_1988_living:
            _use_hires_bg = bg_1988_living
        elif calendar_date != DATE_1988 and bg_living_orig:
            _use_hires_bg = bg_living_orig
    elif current_scene == "bedroom" and bg_bedroom:
        _use_hires_bg = bg_bedroom
    elif current_scene == "bathroom" and bathtub_state != 0 and bg_bathroom_full:
        _use_hires_bg = bg_bathroom_full
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
                draw_cart_icon(display_surface, tetris_cart_rect, tetris_cart_icon, (50, 200, 80))
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

    # High-res Chi baby (only on 1994-10-23 in living room)
    if current_scene == "living_room" and calendar_date == DATE_1994_10_23:
        display_img = chi_baby_img_with_pacifier if chi_baby_has_pacifier else chi_baby_img
        if display_img:
            _SX = WINDOW_RES[0] / VIRTUAL_RES[0]
            _SY = (WINDOW_RES[1] - 60) / VIRTUAL_RES[1]
            _baby_scaled_w = int(display_img.get_width() * 0.18)  # Scale down to 18% of original
            _baby_scaled_h = int(display_img.get_height() * 0.18)
            _baby_scaled = pygame.transform.scale(display_img, (_baby_scaled_w, _baby_scaled_h))

            # Position: fixed in center if has pacifier, else use chi_baby_x, chi_baby_y
            # (chi_baby_x/y is the center point, matching the collision rect anchor)
            if chi_baby_has_pacifier:
                _baby_screen_x = int(160 * _SX)  # Living room center X
                _baby_screen_y = int(150 * _SY)  # Living room center Y
            else:
                _baby_screen_x = int(chi_baby_x * _SX)
                _baby_screen_y = int(chi_baby_y * _SY)

            screen.blit(_baby_scaled, (_baby_screen_x - _baby_scaled_w // 2, _baby_screen_y - _baby_scaled_h // 2))

    # Render coin items
    if current_scene == "living_room" and calendar_date == DATE_1994_10_23 and coin_items:
        _SX = WINDOW_RES[0] / VIRTUAL_RES[0]
        _SY = (WINDOW_RES[1] - 60) / VIRTUAL_RES[1]

        for coin in coin_items:
            if coin_img:
                _coin_scaled_w = int(coin_img.get_width() * 0.04)
                _coin_scaled_h = int(coin_img.get_height() * 0.04)
                _coin_scaled = pygame.transform.scale(coin_img, (_coin_scaled_w, _coin_scaled_h))
                _coin_screen_x = int(coin['x'] * _SX)
                _coin_screen_y = int(coin['y'] * _SY)
                screen.blit(_coin_scaled, (_coin_screen_x, _coin_screen_y))

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
            elif tv_channel == 2:
                if "Chi的奶嘴_去背.png" not in inventory:
                    current_tv_img = chi_tv_pacifier_img
                else:
                    current_tv_img = chi_tv_nopacifier_img

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
        # Cabinet dialog box (displayed over existing background)
        _dw, _dh = 440, 560
        _dx = (WINDOW_RES[0] - _dw) // 2
        _dy = (WINDOW_RES[1] - _dh) // 2 - 20

        # Draw cabinet image directly over existing background
        # (background already rendered by main loop)
        _ci_popup = _cab_current_img()
        if _ci_popup:
            screen.blit(pygame.transform.scale(_ci_popup, (_dw, _dh)), (_dx, _dy))

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
            _cab_is_warning = cabinet_message in ("This drawer is locked. Need a key.", "Need to select the key in inventory!")
            _cab_msg_color = (255, 120, 120) if _cab_is_warning else (255, 230, 150)
            msg = high_res_inst_font.render(cabinet_message, True, _cab_msg_color)
            screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0] // 2, _dy - 40)))
        inst = high_res_inst_font.render("Up/Dn: Select | SPACE: Open/Interact | ESC: Close", True, (220, 220, 220))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0] // 2, WINDOW_RES[1] - 110)))

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
        hint_ic = font.render("Select a cartridge (1-9, 0) then SPACE to insert  |  ESC: close", True, (0, 180, 40))
        screen.blit(hint_ic, hint_ic.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 + 40)))
        pygame.draw.rect(screen, (50, 50, 50), (WINDOW_RES[0]//2 - 30, mon_r.bottom, 60, 20))
        draw_inventory_bar()

    elif ui_state == "computer":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        c_rect = pygame.Rect(100, 100, WINDOW_RES[0] - 200, WINDOW_RES[1] - 200)
        pygame.draw.rect(screen, (35, 30, 55), c_rect, border_radius=10)

        # Floor panel aligned to where the fighters actually stand (was a thin
        # line floating ~90px below their feet, making them look airborne)
        _fighter_ground_y = 470
        _floor_top = _fighter_ground_y + 42
        _floor_rect = pygame.Rect(c_rect.x + 4, _floor_top, c_rect.width - 8, c_rect.bottom - _floor_top - 4)
        pygame.draw.rect(screen, (70, 55, 42), _floor_rect)
        pygame.draw.rect(screen, (115, 92, 60), (_floor_rect.x, _floor_rect.y, _floor_rect.width, 4))

        pygame.draw.rect(screen, (150, 150, 150), c_rect, 4, border_radius=10)

        # Title with a drop shadow for legibility
        _title_txt = "STREET FIGHTER II"
        _title_shadow = high_res_big_font.render(_title_txt, True, (60, 0, 0))
        screen.blit(_title_shadow, _title_shadow.get_rect(center=(c_rect.centerx + 3, c_rect.y + 38)))
        _title = high_res_big_font.render(_title_txt, True, (255, 70, 70))
        screen.blit(_title, _title.get_rect(center=(c_rect.centerx, c_rect.y + 35)))

        # Win indicator pips (left = player, right = enemy)
        for i in range(2):
            col_p = (255, 215, 0) if i < fighter_player_wins else (75, 75, 85)
            pygame.draw.circle(screen, col_p, (c_rect.x + 50 + i * 24, c_rect.y + 78), 8)
            pygame.draw.circle(screen, (20, 20, 20), (c_rect.x + 50 + i * 24, c_rect.y + 78), 8, 2)
            col_e = (255, 215, 0) if i < fighter_enemy_wins else (75, 75, 85)
            pygame.draw.circle(screen, col_e, (c_rect.right - 50 - i * 24, c_rect.y + 78), 8)
            pygame.draw.circle(screen, (20, 20, 20), (c_rect.right - 50 - i * 24, c_rect.y + 78), 8, 2)

        # Health bars: bevelled, color-coded by remaining HP%
        def _hp_bar_color(_hp):
            _pct = max(0, _hp) / 100
            if _pct > 0.5:
                return (80, 220, 90)
            elif _pct > 0.25:
                return (240, 200, 60)
            return (230, 70, 60)

        _bar_w = 300
        for _is_p1 in (True, False):
            _bx = c_rect.x + 50 if _is_p1 else c_rect.right - 350
            _by = c_rect.y + 120
            _hp = rt_p1["hp"] if _is_p1 else rt_p2["hp"]
            name_surf = font.render("PLAYER 1" if _is_p1 else "COMPUTER", True, (255, 255, 255))
            screen.blit(name_surf, (_bx, _by - 22))
            pygame.draw.rect(screen, (60, 20, 20), (_bx, _by, _bar_w, 20), border_radius=4)
            _fill_w = int(_bar_w * max(0, _hp) / 100)
            if _fill_w > 0:
                _fill_rect = pygame.Rect(_bx, _by, _fill_w, 20) if _is_p1 else pygame.Rect(_bx + _bar_w - _fill_w, _by, _fill_w, 20)
                pygame.draw.rect(screen, _hp_bar_color(_hp), _fill_rect)
            pygame.draw.rect(screen, (220, 220, 220), (_bx, _by, _bar_w, 20), 2, border_radius=4)

        _p1_action = "hurt" if rt_p1.get("invul_timer", 0) > 0 and rt_p1["state"] != "attacking" else rt_p1["state"]
        draw_fighter(screen, rt_p1["x"], rt_p1["y"], rt_p1["dir"], _p1_action, rt_p1["hp"])
        draw_zangief(screen, rt_p2["x"], rt_p2["y"], rt_p2["dir"], rt_p2["state"], rt_p2["hp"], rt_p2.get("invul_timer", 0))

        if fighter_message:
            msg = high_res_inst_font.render(fighter_message, True, (255, 255, 0))
            screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, c_rect.y + 200)))

        inst = high_res_inst_font.render("Arrows: Move/Jump | SPACE: Attack | ESC: Close", True, (200, 200, 200))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

        # Draw inventory bar in computer UI
        draw_inventory_bar()

    elif ui_state == "notebook":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, 0))

        # Display notebook image
        if notebook_img:
            _w = int(notebook_img.get_width() * 0.4)
            _h = int(notebook_img.get_height() * 0.4)
            _x = (WINDOW_RES[0] - _w) // 2
            _y = (WINDOW_RES[1] - _h) // 2
            screen.blit(pygame.transform.scale(notebook_img, (_w, _h)), (_x, _y))

        inst = high_res_inst_font.render("ESC: Close", True, (220, 220, 220))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

        draw_inventory_bar()

    elif ui_state == "outdoor":
        # First-person outdoor view — no player sprite, just the scene
        if outdoor_scene_img:
            # Scale to cover the window while preserving aspect ratio (no stretching),
            # then crop the overflow evenly instead of squashing it to fit exactly.
            _ow, _oh = outdoor_scene_img.get_size()
            _oscale = max(WINDOW_RES[0] / _ow, WINDOW_RES[1] / _oh)
            _osw, _osh = int(_ow * _oscale), int(_oh * _oscale)
            _oscaled = pygame.transform.smoothscale(outdoor_scene_img, (_osw, _osh))
            screen.blit(_oscaled, ((WINDOW_RES[0] - _osw) // 2, (WINDOW_RES[1] - _osh) // 2))
        else:
            screen.fill((120, 170, 220))

        if not outdoor_message_shown:
            caption = high_res_inst_font.render("You stepped outside. SPACE: ... | ESC: Back inside", True, (255, 255, 255))
            cap_bg = pygame.Surface((caption.get_width() + 20, caption.get_height() + 12), pygame.SRCALPHA)
            cap_bg.fill((0, 0, 0, 140))
            screen.blit(cap_bg, cap_bg.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 50)))
            screen.blit(caption, caption.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 50)))
        else:
            # Birthday message, centered on screen
            _bm_txt = high_res_big_font.render("HAPPY BIRTHDAY!", True, (255, 220, 100))
            _bm_box_w = _bm_txt.get_width() + 60
            _bm_box_h = _bm_txt.get_height() + 40
            _bm_box_x = (WINDOW_RES[0] - _bm_box_w) // 2
            _bm_box_y = (WINDOW_RES[1] - _bm_box_h) // 2
            pygame.draw.rect(screen, (20, 20, 35), (_bm_box_x, _bm_box_y, _bm_box_w, _bm_box_h), border_radius=10)
            pygame.draw.rect(screen, (120, 160, 220), (_bm_box_x, _bm_box_y, _bm_box_w, _bm_box_h), 2, border_radius=10)
            screen.blit(_bm_txt, _bm_txt.get_rect(center=(WINDOW_RES[0] // 2, WINDOW_RES[1] // 2)))

    elif ui_state == "iron_cabinet_scare":
        # 1988 jump scare: the cabinet image snaps open and rapidly zooms toward the player
        screen.fill((0, 0, 0))
        _scare_elapsed = pygame.time.get_ticks() - iron_cabinet_scare_start
        _scare_t = min(1.0, _scare_elapsed / 200)  # fast ~0.2s snap
        _scare_scale = 0.15 + 1.25 * _scare_t  # grows from 0.15x to 1.4x (overshoots screen)
        if iron_cabinet_scare_img:
            _siw, _sih = iron_cabinet_scare_img.get_size()
            _ssw = max(1, int(WINDOW_RES[0] * _scare_scale))
            _ssh = max(1, int(_ssw * _sih / _siw))
            _scare_scaled = pygame.transform.smoothscale(iron_cabinet_scare_img, (_ssw, _ssh))
            screen.blit(_scare_scaled, (WINDOW_RES[0]//2 - _ssw//2, WINDOW_RES[1]//2 - _ssh//2))
        if _scare_t >= 1.0:
            _scare_hint = high_res_inst_font.render("ESC / SPACE to continue", True, (220, 220, 220))
            screen.blit(_scare_hint, _scare_hint.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 40)))

    elif ui_state == "iron_cabinet":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, 0))

        # Display iron cabinet image (locked / has coin / empty)
        if not iron_cabinet_unlocked:
            _ci_img = iron_cabinet_locked_img
        elif not iron_cabinet_coin_taken:
            _ci_img = iron_cabinet_coin_img
        else:
            _ci_img = iron_cabinet_open_img
        if _ci_img:
            _w = int(_ci_img.get_width() * 0.4)
            _h = int(_ci_img.get_height() * 0.4)
            _x = (WINDOW_RES[0] - _w) // 2
            _y = (WINDOW_RES[1] - _h) // 2
            screen.blit(pygame.transform.scale(_ci_img, (_w, _h)), (_x, _y))

        if not iron_cabinet_unlocked:
            inst = high_res_inst_font.render("SPACE: Enter Password | ESC: Close", True, (220, 220, 220))
        elif not iron_cabinet_coin_taken:
            inst = high_res_inst_font.render("SPACE: Take Coin | ESC: Close", True, (220, 220, 220))
        else:
            inst = high_res_inst_font.render("UP: Open Gashapon | ESC: Close", True, (220, 220, 220))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

        if cabinet_message:
            msg = high_res_inst_font.render(cabinet_message, True, (100, 255, 100))
            screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 - 200)))

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

        # Show the prize image briefly after a successful coin insert
        if gashapon_feedback == "Got it!" and gashapon_feedback_timer > 0 and gashapon_last_prize in gashapon_prize_images:
            _prize_img = gashapon_prize_images[gashapon_last_prize]
            _pw = int(_prize_img.get_width() * 0.3)
            _ph = int(_prize_img.get_height() * 0.3)
            _px = (WINDOW_RES[0] - _pw) // 2
            _py = (WINDOW_RES[1] - _ph) // 2 - 100
            screen.blit(pygame.transform.scale(_prize_img, (_pw, _ph)), (_px, _py))

        if gashapon_feedback and gashapon_feedback_timer > 0:
            feedback_color = (100, 255, 100) if gashapon_feedback == "Got it!" else (255, 180, 80)
            feedback_surf = high_res_inst_font.render(gashapon_feedback, True, feedback_color)
            screen.blit(feedback_surf, feedback_surf.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 + 140)))

        inst = high_res_inst_font.render("SPACE: Insert Coin | ESC: Back to Cabinet", True, (220, 220, 220))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

        draw_inventory_bar()

    elif ui_state == "iron_cabinet_password":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, 0))

        # Display input boxes for the cabinet password with word grouping
        box_width = 40
        box_height = 40
        word_spacing_small = 45    # Spacing within words (reduced from 55)
        word_spacing_large = 60    # Spacing between words (reduced from 85)
        start_x = 20               # Start position (reduced from 80 to fit in window)
        start_y = WINDOW_RES[1] // 2 - 100

        # Define word groups (apostrophe removed from TAIME)
        words = ["JE", "TAIME", "PLUS", "QUE", "TOUT"]

        # Calculate character positions
        char_positions = []
        current_x = start_x
        for word in words:
            for char in word:
                char_positions.append((char, current_x))
                current_x += word_spacing_small
            current_x += word_spacing_large - word_spacing_small

        # Draw input boxes
        apostrophe_pos = None  # Track position for apostrophe visual hint
        for i in range(len(cabinet_password_target)):
            if i >= len(char_positions):
                break
            char, box_x = char_positions[i]
            box_y = start_y

            # Draw box border
            pygame.draw.rect(screen, (200, 200, 200), (box_x, box_y, box_width, box_height), 2)

            # Draw character if input exists at this position
            if i < len(cabinet_password_input):
                input_char = cabinet_password_input[i]
                char_font = pygame.font.SysFont("arial", 24, bold=True)
                char_surf = char_font.render(input_char, True, (200, 200, 200))
                char_rect = char_surf.get_rect(center=(box_x + box_width // 2, box_y + box_height // 2))
                screen.blit(char_surf, char_rect)

            # Highlight cursor position with green border
            if i == cabinet_password_edit_pos:
                pygame.draw.rect(screen, (0, 255, 0), (box_x, box_y, box_width, box_height), 3)

            # Mark position for apostrophe (between T and A in TAIME)
            if i == 2:  # T is at position 2
                apostrophe_pos = box_x + box_width

        # Draw visual apostrophe hint between T and A
        if apostrophe_pos:
            apostrophe_font = pygame.font.SysFont("arial", 28, bold=True)
            apostrophe_surf = apostrophe_font.render("'", True, (200, 200, 200))
            apostrophe_rect = apostrophe_surf.get_rect(center=(apostrophe_pos + 7, start_y + 25))
            screen.blit(apostrophe_surf, apostrophe_rect)

        # Display feedback message if available
        if cabinet_password_feedback and cabinet_password_feedback_timer > 0:
            feedback_surf = high_res_inst_font.render(cabinet_password_feedback, True, (255, 100, 100))
            screen.blit(feedback_surf, feedback_surf.get_rect(center=(WINDOW_RES[0]//2, start_y - 50)))

        # Instructions (shortened to fit in window)
        inst = high_res_inst_font.render("Type the password | ENTER: Check | ESC: Cancel | BS: Delete", True, (200, 200, 200))
        screen.blit(inst, inst.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

    elif ui_state == "bookshelf":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        b_rect = pygame.Rect(WINDOW_RES[0]//2 - 200, WINDOW_RES[1]//2 - 150, 400, 300)
        _shelf_inner = draw_bookshelf_bg(screen, b_rect)
        _shelf_top = _shelf_inner.bottom - 4

        colors = {"Red": (190, 55, 50), "Blue": (50, 75, 165), "Green": (55, 140, 70)}

        if calendar_date == DATE_1988:
            display_order = ["Green", "Blue", "Red"]
        else:
            display_order = bookshelf_order

        for i, b in enumerate(display_order):
            book_r = pygame.Rect(b_rect.x + 80 + i*90, _shelf_top - 150, 60, 150)
            draw_book_icon(screen, book_r, colors[b])
            if i == bookshelf_selection and calendar_date != DATE_1988:
                pygame.draw.rect(screen, (255, 255, 0), book_r.inflate(6, 6), 3, border_radius=6)
                
        if bookshelf_unlocked and "SF2 Cartridge" not in inventory:
            # Draw cartridge sitting between books
            cart_r = pygame.Rect(b_rect.centerx - 48, b_rect.y + 30, 96, 60)
            draw_cart_icon(screen, cart_r, sf2_icon, (220, 80, 30))
            msg = high_res_inst_font.render("SPACE to take SF2 Cartridge!", True, (255, 220, 0))
        elif bookshelf_unlocked:
            msg = high_res_inst_font.render("SF2 Cartridge taken.", True, (150, 255, 100))
        elif calendar_date == DATE_1988:
            msg = high_res_inst_font.render("Books are stuck...", True, (200, 200, 200))
        else:
            msg = high_res_inst_font.render("L/R: Select | U/D: Swap | ESC: Close", True, (200, 200, 200))
        screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

    elif ui_state == "main_door":
        overlay = pygame.Surface(WINDOW_RES, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        d_rect = pygame.Rect(WINDOW_RES[0]//2 - 200, WINDOW_RES[1]//2 - 200, 400, 400)
        pygame.draw.rect(screen, (100, 50, 50), d_rect, border_radius=10)
        
        # 4 slots, one per gashapon prize
        for i in range(4):
            slot_r = pygame.Rect(d_rect.x + 30 + i*90, d_rect.centery - 40, 80, 80)
            pygame.draw.rect(screen, (20, 20, 20), slot_r)
            if door_puzzle_state[i]:
                _prize_img = gashapon_prize_images.get(GASHAPON_PRIZES[i])
                if _prize_img:
                    icon = pygame.transform.smoothscale(_prize_img, (slot_r.width + 14, slot_r.height - 4))
                    screen.blit(icon, (slot_r.x - 7, slot_r.y + 2))
                else:
                    pygame.draw.rect(screen, (255, 100, 255), slot_r.inflate(-10, -10))

        if all(door_puzzle_state):
            msg = high_res_inst_font.render("DOOR OPENED! YOU ESCAPED!", True, (0, 255, 0))
        else:
            msg = high_res_inst_font.render("SPACE: Insert Gashapon | ESC: Close", True, (200, 200, 200))
        screen.blit(msg, msg.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]-130)))

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
            msg = high_res_inst_font.render("Chi Baby is crying... give them a pacifier!", True, (200, 200, 200))
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

    # Update gashapon feedback timer
    if gashapon_feedback_timer > 0:
        gashapon_feedback_timer -= 1
    else:
        gashapon_feedback = ""

    # Update cabinet password feedback timer
    if cabinet_password_feedback_timer > 0:
        cabinet_password_feedback_timer -= 1
    else:
        cabinet_password_feedback = ""

    # Dates before 1988/6/22 are shown in black & white
    if calendar_date < DATE_1988:
        screen.blit(pygame.transform.grayscale(screen), (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()