import pygame
import sys
import datetime
import calendar
import os
import random

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def draw_flashlight_icon(surface, center_x, center_y, size):
    # 畫一個精美的手電筒圖示
    body_w, body_h = size * 0.3, size * 0.6
    # 手電筒身體
    pygame.draw.rect(surface, (80, 80, 90), (center_x - body_w/2, center_y - body_h/3, body_w, body_h), border_radius=int(size*0.05))
    # 手電筒頭部
    pygame.draw.polygon(surface, (120, 120, 130), [
        (center_x - body_w/2, center_y - body_h/3),
        (center_x + body_w/2, center_y - body_h/3),
        (center_x + body_w/1.2, center_y - body_h/1.5),
        (center_x - body_w/1.2, center_y - body_h/1.5)
    ])
    # 光束
    pygame.draw.ellipse(surface, (255, 255, 200), (center_x - body_w/1.2, center_y - body_h/1.5 - body_w/4, body_w*1.66, body_w/2))
    # 開關
    pygame.draw.rect(surface, (200, 50, 50), (center_x - 3, center_y, 6, 10), border_radius=2)

def draw_key_icon(surface, center_x, center_y, size):
    # 畫一個復古金鑰匙圖示
    head_r = size * 0.15
    shaft_w, shaft_h = size * 0.08, size * 0.4
    pygame.draw.circle(surface, (255, 215, 0), (center_x, center_y - shaft_h/2 - head_r/2), head_r, max(1, int(size*0.05)))
    pygame.draw.rect(surface, (255, 215, 0), (center_x - shaft_w/2, center_y - shaft_h/2, shaft_w, shaft_h))
    pygame.draw.rect(surface, (255, 215, 0), (center_x, center_y + shaft_h/4, shaft_w*3, shaft_w*1.5))
    pygame.draw.rect(surface, (255, 215, 0), (center_x, center_y + shaft_h/2 - shaft_w, shaft_w*2, shaft_w*1.5))

# 初始化 Pygame
pygame.init()

# 設定畫面解析度
# 為了呈現復古 2D 畫質，我們使用較低的內部解析度，然後放大顯示 (顆粒感)
VIRTUAL_RES = (320, 240)
VIRTUAL_RES_1988 = (160, 120) # 1988年場景更低的解析度
WINDOW_RES = (960, 720) # 放大 3 倍

screen = pygame.display.set_mode(WINDOW_RES)
pygame.display.set_caption("Retro 2D Game")

# 建立一個虛擬畫布，所有的繪圖都在這個低解析度畫布上進行
display_surface = pygame.Surface(VIRTUAL_RES)
display_surface_1988 = pygame.Surface(VIRTUAL_RES_1988)

# 定義顏色
BLACK = (0, 0, 0)
MARBLE_COLOR_1 = (235, 235, 240)
MARBLE_COLOR_2 = (215, 215, 220)
PLAYER_COLOR = (200, 50, 50)
SHADOW_COLOR = (20, 100, 20)
DESK_COLOR = (139, 69, 19)
CABINET_COLOR = (120, 70, 30)
CALENDAR_BG = (30, 30, 30)
CALENDAR_TEXT_COLOR = (0, 255, 0)

# 玩家設定
player_size = 16
player_x = VIRTUAL_RES[0] // 2
player_y = VIRTUAL_RES[1] // 2
player_speed = 2

# 場景與物件設定
current_scene = "living_room" # "living_room" or "bedroom"

# 客廳物件
desk_rect = pygame.Rect(VIRTUAL_RES[0] // 2 - 40, 50, 80, 40)
calendar_rect = pygame.Rect(desk_rect.centerx - 30, desk_rect.centery - 10, 60, 20)
cabinet_rect = pygame.Rect(VIRTUAL_RES[0] - 60, 40, 40, 100)
living_door_rect = pygame.Rect(0, 40, 20, 60) # 左上角門

# 房間物件
bedroom_door_rect = pygame.Rect(VIRTUAL_RES[0] - 20, 40, 20, 60) # 右上角門
bookshelf_rect = pygame.Rect(0, 60, 40, 80)
computer_desk_rect = pygame.Rect(VIRTUAL_RES[0] // 2 - 50, VIRTUAL_RES[1] - 90, 100, 40)

calendar_date = datetime.date(2026, 6, 19)
font = pygame.font.Font(None, 16)
high_res_big_font = pygame.font.Font(None, 120)
high_res_inst_font = pygame.font.Font(None, 40)

ui_state = "game" # "game", "calendar", "tv", "cabinet", "computer"
calendar_selection = 0 # 0: Year, 1: Month, 2: Day
cabinet_selection = 0
cabinet_drawer1_open = False
cabinet_drawer2_open = False
has_flashlight = False
has_key = False
cabinet_message = ""
inventory = []
inv_font = pygame.font.Font(None, 24)

# 1988/6/22 場景狀態
DATE_1988 = datetime.date(1988, 6, 22)
selected_inv_slot = 0   # 目前選中的道具格 (0-4)
room_lights_on = False  # 電燈開關是否已開啟
# 電燈開關位置 (在桌子後方, 1988場景座標系)
light_switch_rect_1988 = pygame.Rect(VIRTUAL_RES_1988[0]//2 + 30, 14, 10, 8)

# 快打旋風迷你遊戲 (Real-Time Fighting)
fighter_player_wins = 0
fighter_enemy_wins = 0
fighter_state = "fighting"
fighter_message = "P1: Arrows+Space | CPU: Zangief AI"

rt_p1 = {}
rt_p2 = {}

def init_rt_fighter():
    global rt_p1, rt_p2, fighter_state, fighter_message
    rt_p1 = {"x": 200, "y": 470, "vy": 0, "hp": 100, "state": "idle", "dir": 1, "atk_timer": 0, "invul_timer": 0, "color": (50, 150, 255)}
    rt_p2 = {"x": WINDOW_RES[0] - 240, "y": 470, "vy": 0, "hp": 100, "state": "idle", "dir": -1, "atk_timer": 0, "invul_timer": 0, "color": (255, 100, 50)}
    fighter_state = "fighting"
    fighter_message = "P1: Arrows+Space | CPU: Zangief AI"

init_rt_fighter()

try:
    tv_image_path = get_resource_path(os.path.join("picture", "Back-To-The-Feture.jpg"))
    tv_image = pygame.image.load(tv_image_path)
except Exception as e:
    print(f"Could not load TV image: {e}")
    tv_image = None

clock = pygame.time.Clock()

def draw_desk_and_calendar(surface):
    # 畫桌子
    pygame.draw.rect(surface, DESK_COLOR, desk_rect)
    pygame.draw.rect(surface, (100, 50, 10), desk_rect, 2)
    
    # 畫日曆圖示 (左側)
    calendar_icon_rect = pygame.Rect(desk_rect.centerx - 32, desk_rect.centery - 12, 24, 24)
    # 白紙部分
    pygame.draw.rect(surface, (240, 240, 240), calendar_icon_rect)
    # 紅色頂部
    pygame.draw.rect(surface, (200, 50, 50), (calendar_icon_rect.x, calendar_icon_rect.y, calendar_icon_rect.width, 6))
    # 畫幾個點假裝是日期格
    for row in range(2):
        for col in range(3):
            dot_x = calendar_icon_rect.x + 4 + col * 6
            dot_y = calendar_icon_rect.y + 10 + row * 6
            pygame.draw.rect(surface, (150, 150, 150), (dot_x, dot_y, 4, 4))

    # 畫電視圖示 (右側)
    tv_icon_rect = pygame.Rect(desk_rect.centerx + 8, desk_rect.centery - 12, 24, 24)
    # 電視外殼
    pygame.draw.rect(surface, (40, 40, 40), tv_icon_rect)
    # 電視螢幕 (發出微弱藍光)
    pygame.draw.rect(surface, (100, 180, 255), (tv_icon_rect.x + 2, tv_icon_rect.y + 2, tv_icon_rect.width - 4, tv_icon_rect.height - 8))
    # 電視底座/按鈕區
    pygame.draw.rect(surface, (20, 20, 20), (tv_icon_rect.x, tv_icon_rect.y + tv_icon_rect.height - 6, tv_icon_rect.width, 6))
    # 電視電源燈
    pygame.draw.rect(surface, (255, 0, 0), (tv_icon_rect.x + tv_icon_rect.width - 6, tv_icon_rect.y + tv_icon_rect.height - 4, 2, 2))

def draw_fighter(surface, center_x, center_y, is_player, action, hp):
    # 畫人物 (簡單的方塊拼湊)
    color = (50, 150, 255) if is_player else (255, 100, 50)
    if hp <= 0:
        color = (100, 100, 100) # 死亡變灰
        action = "hurt"
        
    eye_dir = 1 if is_player else -1
    
    body_rect = pygame.Rect(center_x - 20, center_y - 40, 40, 80)
    
    if action == "hurt":
        # 身體後傾
        body_rect.x -= eye_dir * 20
        pygame.draw.rect(surface, (200, 50, 50), body_rect, border_radius=5)
        pygame.draw.circle(surface, (255, 150, 150), (center_x - eye_dir * 30, center_y - 60), 20)
        pygame.draw.rect(surface, (80, 80, 80), (center_x - 15 - eye_dir*20, center_y + 40, 12, 40)) 
        pygame.draw.rect(surface, (80, 80, 80), (center_x + 5 - eye_dir*20, center_y + 40, 12, 40))
        return

    pygame.draw.rect(surface, color, body_rect, border_radius=5)
    
    # 頭部
    pygame.draw.circle(surface, (255, 200, 150), (center_x, center_y - 60), 20)
    
    # 眼睛方向
    pygame.draw.circle(surface, (0, 0, 0), (center_x + eye_dir * 8, center_y - 65), 4)
    
    # 手腳
    if action == "idle":
        pygame.draw.rect(surface, color, (center_x - 25, center_y - 30, 12, 50)) # 左手
        pygame.draw.rect(surface, color, (center_x + 13, center_y - 30, 12, 50)) # 右手
        pygame.draw.rect(surface, (80, 80, 80), (center_x - 15, center_y + 40, 12, 40)) # 左腳
        pygame.draw.rect(surface, (80, 80, 80), (center_x + 3, center_y + 40, 12, 40)) # 右腳
    elif action == "Punch":
        # 一隻手伸直
        if eye_dir == 1:
            pygame.draw.rect(surface, color, (center_x + 20, center_y - 30, 50, 15))
            pygame.draw.rect(surface, color, (center_x - 25, center_y - 30, 12, 50))
        else:
            pygame.draw.rect(surface, color, (center_x - 70, center_y - 30, 50, 15))
            pygame.draw.rect(surface, color, (center_x + 13, center_y - 30, 12, 50))
        pygame.draw.rect(surface, (80, 80, 80), (center_x - 15, center_y + 40, 12, 40)) 
        pygame.draw.rect(surface, (80, 80, 80), (center_x + 3, center_y + 40, 12, 40))
    elif action == "Kick":
        # 一隻腳踢出
        pygame.draw.rect(surface, color, (center_x - 25, center_y - 30, 12, 50)) 
        pygame.draw.rect(surface, color, (center_x + 13, center_y - 30, 12, 50))
        if eye_dir == 1:
            pygame.draw.rect(surface, (80, 80, 80), (center_x - 15, center_y + 40, 12, 40)) # 站立腳
            pygame.draw.rect(surface, (80, 80, 80), (center_x + 3, center_y + 30, 60, 15)) # 踢出腳
        else:
            pygame.draw.rect(surface, (80, 80, 80), (center_x + 3, center_y + 40, 12, 40)) # 站立腳
            pygame.draw.rect(surface, (80, 80, 80), (center_x - 63, center_y + 30, 60, 15)) # 踢出腳
    elif action == "Block":
        # 雙手交叉在臉前
        pygame.draw.rect(surface, color, (center_x - 20, center_y - 50, 40, 12)) 
        pygame.draw.rect(surface, color, (center_x - 20, center_y - 35, 40, 12))
        pygame.draw.rect(surface, (80, 80, 80), (center_x - 15, center_y + 40, 12, 40)) 
        pygame.draw.rect(surface, (80, 80, 80), (center_x + 3, center_y + 40, 12, 40))

def draw_zangief(surface, x, y, direction, state, hp, invul_timer):
    if invul_timer % 4 > 1: return # flashing
    
    skin_color = (255, 180, 140)
    underwear_color = (200, 30, 30)
    boot_color = (180, 20, 20)
    hair_color = (80, 40, 20)
    scar_color = (200, 100, 100)
    
    if hp <= 0:
        skin_color = (100, 100, 100)
        underwear_color = (80, 80, 80)
        boot_color = (60, 60, 60)
    
    # Body base
    pygame.draw.rect(surface, skin_color, (x-5, y, 50, 80), border_radius=10)
    # Red underwear
    pygame.draw.rect(surface, underwear_color, (x-5, y+40, 50, 20), border_radius=5)
    # Red boots
    pygame.draw.rect(surface, boot_color, (x-5, y+65, 20, 15))
    pygame.draw.rect(surface, boot_color, (x+25, y+65, 20, 15))
    # Chest hair
    pygame.draw.line(surface, hair_color, (x+10, y+10), (x+20, y+25), 2)
    pygame.draw.line(surface, hair_color, (x+30, y+10), (x+20, y+25), 2)
    # Scars
    pygame.draw.line(surface, scar_color, (x+20, y+35), (x+35, y+25), 2)
    # Head
    pygame.draw.circle(surface, skin_color, (x+20, y-15), 18)
    # Mohawk
    pygame.draw.rect(surface, hair_color, (x+15, y-38, 10, 10))
    pygame.draw.rect(surface, hair_color, (x+12, y-35, 16, 5))
    # Beard
    if direction == 1:
        pygame.draw.rect(surface, hair_color, (x+25, y-10, 10, 8))
    else:
        pygame.draw.rect(surface, hair_color, (x+5, y-10, 10, 8))
    # Eyes
    eye_x = x+25 if direction == 1 else x+7
    pygame.draw.rect(surface, (255, 255, 255), (eye_x, y-20, 8, 8))
    pygame.draw.rect(surface, (0, 0, 0), (eye_x + (4 if direction==1 else 0), y-18, 4, 4))
    # Arms
    if state == "attacking":
        pygame.draw.rect(surface, skin_color, (x-30, y+5, 30, 15))
        pygame.draw.rect(surface, skin_color, (x+40, y+5, 30, 15))
    else:
        pygame.draw.rect(surface, skin_color, (x-15, y+5, 15, 30))
        pygame.draw.rect(surface, skin_color, (x+40, y+5, 15, 30))

def draw_retro_player(surface, x, y):
    # 畫陰影
    pygame.draw.ellipse(surface, SHADOW_COLOR, (x, y + player_size - 4, player_size, 8))
    # 畫身體 (簡單的方塊人)
    pygame.draw.rect(surface, PLAYER_COLOR, (x, y, player_size, player_size))
    # 畫眼睛
    pygame.draw.rect(surface, (255, 255, 255), (x + 2, y + 4, 4, 4))
    pygame.draw.rect(surface, (255, 255, 255), (x + 10, y + 4, 4, 4))
    pygame.draw.rect(surface, (0, 0, 0), (x + 4, y + 6, 2, 2))
    pygame.draw.rect(surface, (0, 0, 0), (x + 10, y + 6, 2, 2))

# 遊戲主迴圈
running = True
while running:
    # 1. 處理事件 (例如關閉視窗)
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    # 建立所有場景的感應區 (避免切換場景時遇到 NameError)
    calendar_proximity_rect = pygame.Rect(desk_rect.left, desk_rect.top, desk_rect.width // 2, desk_rect.height).inflate(24, 32)
    tv_proximity_rect = pygame.Rect(desk_rect.centerx, desk_rect.top, desk_rect.width // 2, desk_rect.height).inflate(24, 32)
    cabinet_proximity_rect = cabinet_rect.inflate(32, 32)
    living_door_prox = living_door_rect.inflate(32, 32)
    bedroom_door_prox = bedroom_door_rect.inflate(32, 32)
    bookshelf_prox = bookshelf_rect.inflate(32, 32)
    computer_prox = computer_desk_rect.inflate(32, 32)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if ui_state == "game":
                if event.key == pygame.K_1: selected_inv_slot = 0
                elif event.key == pygame.K_2: selected_inv_slot = 1
                elif event.key == pygame.K_3: selected_inv_slot = 2
                elif event.key == pygame.K_4: selected_inv_slot = 3
                elif event.key == pygame.K_5: selected_inv_slot = 4
                if event.key == pygame.K_SPACE:
                    if current_scene == "living_room":
                        if calendar_date == DATE_1988 and not room_lights_on:
                            # 1988黑暗場景: 只能靠手電筒找電燈開關
                            # 換算玩家位置到1988解析度座標
                            px_1988 = int(player_x * VIRTUAL_RES_1988[0] / VIRTUAL_RES[0])
                            py_1988 = int(player_y * VIRTUAL_RES_1988[1] / VIRTUAL_RES[1])
                            player_rect_1988 = pygame.Rect(px_1988, py_1988, max(4, player_size * VIRTUAL_RES_1988[0] // VIRTUAL_RES[0]), max(4, player_size * VIRTUAL_RES_1988[1] // VIRTUAL_RES[1]))
                            flashlight_active = (selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Flashlight")
                            if flashlight_active and player_rect_1988.inflate(16, 16).colliderect(light_switch_rect_1988):
                                room_lights_on = True
                        elif calendar_date == DATE_1988 and room_lights_on:
                            if player_rect.colliderect(calendar_proximity_rect):
                                ui_state = "calendar"
                        elif player_rect.colliderect(calendar_proximity_rect):
                            ui_state = "calendar"
                        elif player_rect.colliderect(tv_proximity_rect) and calendar_date == datetime.date(2026, 6, 22):
                            ui_state = "tv"
                        elif player_rect.colliderect(cabinet_proximity_rect) and calendar_date == datetime.date(2026, 6, 22):
                            ui_state = "cabinet"
                            cabinet_message = ""
                        elif player_rect.colliderect(living_door_prox) and calendar_date == datetime.date(2026, 6, 22):
                            current_scene = "bedroom"
                            player_x = bedroom_door_rect.left - player_size - 10
                            player_y = bedroom_door_rect.centery - player_size // 2
                    elif current_scene == "bedroom":
                        if player_rect.colliderect(bedroom_door_prox):
                            current_scene = "living_room"
                            player_x = living_door_rect.right + 10
                            player_y = living_door_rect.centery - player_size // 2
                        elif player_rect.colliderect(computer_prox):
                            ui_state = "computer"
                            init_rt_fighter()
            elif ui_state == "computer":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif fighter_state == "fighting":
                    if event.key == pygame.K_SPACE and rt_p1["state"] != "attacking":
                        rt_p1["state"] = "attacking"
                        rt_p1["atk_timer"] = 15
                    elif event.key == pygame.K_UP and rt_p1["y"] >= 470 and rt_p1["state"] != "attacking":
                        rt_p1["vy"] = -15
                        rt_p1["state"] = "jumping"
                elif fighter_state == "round_over":
                    if event.key == pygame.K_SPACE:
                        init_rt_fighter()
                elif fighter_state == "game_over":
                    if event.key == pygame.K_SPACE and fighter_enemy_wins == 2:
                        fighter_player_wins = 0
                        fighter_enemy_wins = 0
                        init_rt_fighter()
            elif ui_state == "tv":
                if event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                    ui_state = "game"
            elif ui_state == "cabinet":
                if event.key == pygame.K_ESCAPE:
                    ui_state = "game"
                elif event.key == pygame.K_UP:
                    cabinet_selection = 0
                    cabinet_message = ""
                elif event.key == pygame.K_DOWN:
                    cabinet_selection = 1
                    cabinet_message = ""
                elif event.key == pygame.K_SPACE:
                    if cabinet_selection == 0:
                        if not cabinet_drawer1_open:
                            cabinet_drawer1_open = True
                        else:
                            if not has_flashlight:
                                has_flashlight = True
                                inventory.append("Flashlight")
                                cabinet_message = "Got Flashlight!"
                            else:
                                cabinet_message = "Drawer is empty."
                    elif cabinet_selection == 1:
                        if not cabinet_drawer2_open:
                            if has_key:
                                cabinet_drawer2_open = True
                                cabinet_message = "Unlocked with key!"
                            else:
                                cabinet_message = "Locked! Need a key."
                        else:
                            cabinet_message = "Drawer is empty."
            elif event.key == pygame.K_ESCAPE:
                    if calendar_date == DATE_1988:
                        room_lights_on = False  # 離開1988場景時重置燈光
            elif ui_state == "calendar":
                if event.key in (pygame.K_SPACE, pygame.K_ESCAPE):
                    ui_state = "game"
                elif event.key == pygame.K_LEFT:
                    calendar_selection = (calendar_selection - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    calendar_selection = (calendar_selection + 1) % 3
                elif event.key == pygame.K_UP:
                    if calendar_selection == 2:
                        calendar_date += datetime.timedelta(days=1)
                    else:
                        y, m, d = calendar_date.year, calendar_date.month, calendar_date.day
                        if calendar_selection == 0: y += 1
                        elif calendar_selection == 1: m = m + 1 if m < 12 else 1
                        try: calendar_date = datetime.date(y, m, d)
                        except ValueError: calendar_date = datetime.date(y, m, calendar.monthrange(y, m)[1])
                elif event.key == pygame.K_DOWN:
                    if calendar_selection == 2:
                        calendar_date -= datetime.timedelta(days=1)
                    else:
                        y, m, d = calendar_date.year, calendar_date.month, calendar_date.day
                        if calendar_selection == 0: y -= 1
                        elif calendar_selection == 1: m = m - 1 if m > 1 else 12
                        try: calendar_date = datetime.date(y, m, d)
                        except ValueError: calendar_date = datetime.date(y, m, calendar.monthrange(y, m)[1])

    # 2. 處理玩家輸入 (鍵盤控制)
    keys = pygame.key.get_pressed()
    old_x, old_y = player_x, player_y
    
    if ui_state == "game":
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y -= player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y += player_speed

    elif ui_state == "computer" and fighter_state == "fighting":
        # P1 movement
        if rt_p1["state"] != "attacking":
            if keys[pygame.K_LEFT]:
                rt_p1["x"] -= 5
                rt_p1["dir"] = -1
                if rt_p1["y"] >= 470: rt_p1["state"] = "moving"
            elif keys[pygame.K_RIGHT]:
                rt_p1["x"] += 5
                rt_p1["dir"] = 1
                if rt_p1["y"] >= 470: rt_p1["state"] = "moving"
            else:
                if rt_p1["y"] >= 470: rt_p1["state"] = "idle"

        # P2 movement (Zangief CPU AI)
        if rt_p2["state"] != "attacking":
            dist_x = rt_p1["x"] - rt_p2["x"]
            if abs(dist_x) > 60:
                rt_p2["dir"] = 1 if dist_x > 0 else -1
                rt_p2["x"] += 3 * rt_p2["dir"]
                if rt_p2["y"] >= 470: rt_p2["state"] = "moving"
            else:
                if rt_p2["y"] >= 470: rt_p2["state"] = "idle"
                
            if abs(dist_x) <= 65 and rt_p2["atk_timer"] == 0 and random.random() < 0.05:
                rt_p2["dir"] = 1 if dist_x > 0 else -1
                rt_p2["state"] = "attacking"
                rt_p2["atk_timer"] = 25
                
            if rt_p2["y"] >= 470 and random.random() < 0.01:
                rt_p2["vy"] = -15
                rt_p2["state"] = "jumping"

        # Apply gravity & physics
        for p in [rt_p1, rt_p2]:
            p["vy"] += 0.8 # gravity
            p["y"] += p["vy"]
            if p["y"] > 470:
                p["y"] = 470
                p["vy"] = 0
            
            # Constraints
            p["x"] = max(50, min(p["x"], WINDOW_RES[0] - 90))

            if p["invul_timer"] > 0:
                p["invul_timer"] -= 1

            if p["atk_timer"] > 0:
                p["atk_timer"] -= 1
                if p["atk_timer"] == 0:
                    p["state"] = "idle"

        # Hit detection
        p1_rect = pygame.Rect(rt_p1["x"], rt_p1["y"], 40, 80)
        p2_rect = pygame.Rect(rt_p2["x"], rt_p2["y"], 40, 80)

        if rt_p1["state"] == "attacking":
            hx = rt_p1["x"] + 40 if rt_p1["dir"] == 1 else rt_p1["x"] - 60
            hitbox1 = pygame.Rect(hx, rt_p1["y"] + 20, 60, 20)
            if hitbox1.colliderect(p2_rect) and rt_p2["invul_timer"] == 0:
                rt_p2["hp"] -= 10
                rt_p2["invul_timer"] = 20
                rt_p2["x"] += 30 * rt_p1["dir"] # Knockback
                if rt_p2["hp"] <= 0:
                    fighter_player_wins += 1
                    if fighter_player_wins == 2:
                        fighter_state = "game_over"
                        if not has_key:
                            has_key = True
                            inventory.append("Key")
                            fighter_message = "P1 WINS MATCH! Got Key! (Press ESC)"
                        else:
                            fighter_message = "P1 WINS MATCH! (Press ESC)"
                    else:
                        fighter_state = "round_over"
                        fighter_message = "P1 Wins Round! (Press SPACE)"

        if rt_p2["state"] == "attacking":
            hx = rt_p2["x"] + 40 if rt_p2["dir"] == 1 else rt_p2["x"] - 60
            hitbox2 = pygame.Rect(hx, rt_p2["y"] + 20, 60, 20)
            if hitbox2.colliderect(p1_rect) and rt_p1["invul_timer"] == 0:
                rt_p1["hp"] -= 10
                rt_p1["invul_timer"] = 20
                rt_p1["x"] += 30 * rt_p2["dir"] # Knockback
                if rt_p1["hp"] <= 0:
                    fighter_enemy_wins += 1
                    if fighter_enemy_wins == 2:
                        fighter_state = "game_over"
                        fighter_message = "P2 WINS MATCH! (Press SPACE to restart)"
                    else:
                        fighter_state = "round_over"
                        fighter_message = "P2 Wins Round! (Press SPACE)"

    # 限制玩家不能走出畫面外
    player_x = max(0, min(player_x, VIRTUAL_RES[0] - player_size))
    player_y = max(0, min(player_y, VIRTUAL_RES[1] - player_size))
    
    # 物件碰撞偵測
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    collision = False
    if current_scene == "living_room":
        if player_rect.colliderect(desk_rect) or (calendar_date == datetime.date(2026, 6, 22) and (player_rect.colliderect(cabinet_rect) or player_rect.colliderect(living_door_rect))):
            collision = True
    elif current_scene == "bedroom":
        if player_rect.colliderect(bookshelf_rect) or player_rect.colliderect(computer_desk_rect) or player_rect.colliderect(bedroom_door_rect):
            collision = True
            
    if collision:
        player_x, player_y = old_x, old_y

    # 3. 畫面繪製

    # ===== 1988年特殊場景 =====
    if calendar_date == DATE_1988 and ui_state == "game" and current_scene == "living_room":
        V = VIRTUAL_RES_1988
        ds = display_surface_1988
        # 換算玩家位置到1988座標
        px_1988 = int(player_x * V[0] / VIRTUAL_RES[0])
        py_1988 = int(player_y * V[1] / VIRTUAL_RES[1])
        ps_1988 = max(4, player_size * V[0] // VIRTUAL_RES[0])
        flashlight_active = (selected_inv_slot < len(inventory) and inventory[selected_inv_slot] == "Flashlight")

        if not room_lights_on:
            # 全黑底
            ds.fill((0, 0, 0))
            if flashlight_active:
                # 手電筒光圈 (只照亮玩家周圍)
                fl_radius = 28
                for dy in range(-fl_radius, fl_radius + 1):
                    for dx in range(-fl_radius, fl_radius + 1):
                        dist = (dx*dx + dy*dy) ** 0.5
                        if dist <= fl_radius:
                            nx, ny = px_1988 + dx, py_1988 + dy
                            if 0 <= nx < V[0] and 0 <= ny < V[1]:
                                alpha = max(0, 1.0 - dist / fl_radius)
                                brightness = int(alpha * alpha * 200)
                                # 只繪製桌子/開關在光圈內
                                if light_switch_rect_1988.collidepoint(nx, ny):
                                    pygame.draw.rect(ds, (200, 200, 80), (nx, ny, 1, 1))
                                elif desk_rect.x * V[0] // VIRTUAL_RES[0] <= nx <= (desk_rect.right * V[0] // VIRTUAL_RES[0]) and \
                                     desk_rect.y * V[1] // VIRTUAL_RES[1] <= ny <= (desk_rect.bottom * V[1] // VIRTUAL_RES[1]):
                                    pygame.draw.rect(ds, (min(255, 80 + brightness), min(255, 40 + brightness//2), 0), (nx, ny, 1, 1))
                                else:
                                    pygame.draw.rect(ds, (brightness, brightness, int(brightness * 0.9)), (nx, ny, 1, 1))
            # 畫玩家 (微弱輪廓)
            pygame.draw.rect(ds, (60, 60, 80) if not flashlight_active else (180, 80, 80), (px_1988, py_1988, ps_1988, ps_1988))
            # 電燈開關標示 (在光圈範圍內才顯示)
            if flashlight_active:
                sx, sy = light_switch_rect_1988.x, light_switch_rect_1988.y
                dist_to_switch = ((px_1988 - sx)**2 + (py_1988 - sy)**2) ** 0.5
                if dist_to_switch <= 28:
                    pygame.draw.rect(ds, (220, 220, 60), light_switch_rect_1988)
        else:
            # 燈亮後: 畫出完整1988客廳 (低解析度, 舊色調)
            ds.fill((180, 160, 120))  # 泛黃舊底色
            # 地板格紋
            for i in range(0, V[0], 16):
                for j in range(0, V[1], 16):
                    if (i//16 + j//16) % 2 == 0:
                        pygame.draw.rect(ds, (160, 140, 100), (i, j, 16, 16))
                    pygame.draw.rect(ds, (140, 120, 90), (i, j, 16, 16), 1)
            # 桌子
            dx1 = desk_rect.x * V[0] // VIRTUAL_RES[0]
            dy1 = desk_rect.y * V[1] // VIRTUAL_RES[1]
            dw1 = desk_rect.width * V[0] // VIRTUAL_RES[0]
            dh1 = desk_rect.height * V[1] // VIRTUAL_RES[1]
            pygame.draw.rect(ds, (100, 55, 15), (dx1, dy1, dw1, dh1))
            pygame.draw.rect(ds, (70, 35, 5), (dx1, dy1, dw1, dh1), 1)
            # 電燈開關 (已開啟, 亮黃色)
            pygame.draw.rect(ds, (255, 255, 100), light_switch_rect_1988)
            pygame.draw.rect(ds, (180, 180, 40), light_switch_rect_1988, 1)
            # 日曆圖示 (桌子左半)
            cal_x = dx1 + 1
            cal_y = dy1 + 1
            pygame.draw.rect(ds, (200, 200, 200), (cal_x, cal_y, dw1//2 - 1, dh1 - 2))
            # 玩家
            pygame.draw.rect(ds, (180, 60, 60), (px_1988, py_1988, ps_1988, ps_1988))

        # 縮放1988畫布到視窗
        scaled_1988 = pygame.transform.scale(ds, WINDOW_RES)
        screen.blit(scaled_1988, (0, 0))

        # 提示文字 (高畫質)
        if not room_lights_on:
            if not flashlight_active:
                hint = high_res_inst_font.render("Press 1-5 to select item from inventory", True, (150, 150, 150))
            else:
                hint = high_res_inst_font.render("Find the light switch...", True, (120, 120, 80))
            screen.blit(hint, hint.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 200)))
        else:
            hint = high_res_inst_font.render("SPACE: Open Calendar | ESC: Exit 1988", True, (180, 160, 80))
            screen.blit(hint, hint.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 200)))

        # 物品欄
        inv_slot_size = 60
        inv_slots = 5
        inv_start_x = (WINDOW_RES[0] - (inv_slots * (inv_slot_size + 10))) // 2
        inv_y = WINDOW_RES[1] - 80
        for i in range(inv_slots):
            slot_rect = pygame.Rect(inv_start_x + i * (inv_slot_size + 10), inv_y, inv_slot_size, inv_slot_size)
            border_color = (255, 255, 0) if i == selected_inv_slot else (200, 200, 200)
            pygame.draw.rect(screen, (40, 40, 40), slot_rect)
            pygame.draw.rect(screen, border_color, slot_rect, 3 if i == selected_inv_slot else 2)
            if i < len(inventory):
                if inventory[i] == "Flashlight":
                    draw_flashlight_icon(screen, slot_rect.centerx, slot_rect.centery, 50)
                elif inventory[i] == "Key":
                    draw_key_icon(screen, slot_rect.centerx, slot_rect.centery, 50)
        pygame.display.flip()
        clock.tick(60)
        continue  # 跳過其餘的繪製流程
    # ===== 結束1988場景 =====

    # 畫背景 (大理石地板)
    display_surface.fill(MARBLE_COLOR_1)
    for i in range(0, VIRTUAL_RES[0], 32):
        for j in range(0, VIRTUAL_RES[1], 32):
            if (i // 32 + j // 32) % 2 == 0:
                pygame.draw.rect(display_surface, MARBLE_COLOR_2, (i, j, 32, 32))
            # 畫大理石接縫
            pygame.draw.rect(display_surface, (200, 200, 200), (i, j, 32, 32), 1)

    if current_scene == "living_room":
        # 畫桌子與日曆
        draw_desk_and_calendar(display_surface)

        if calendar_date == datetime.date(2026, 6, 22):
            # 畫櫃子 (精美版)
            pygame.draw.rect(display_surface, (100, 60, 30), cabinet_rect) # 本體深木色
            pygame.draw.rect(display_surface, (140, 90, 50), cabinet_rect.inflate(-4, -4)) # 淺木色面板
            # 櫃子頂板
            pygame.draw.rect(display_surface, (80, 40, 20), (cabinet_rect.x - 2, cabinet_rect.y - 2, cabinet_rect.width + 4, 6))
            # 畫櫃子門/抽屜線條 (分為上下兩格)
            pygame.draw.rect(display_surface, (60, 30, 10), (cabinet_rect.x + 4, cabinet_rect.y + 8, cabinet_rect.width - 8, 40), 2)
            pygame.draw.rect(display_surface, (60, 30, 10), (cabinet_rect.x + 4, cabinet_rect.y + 52, cabinet_rect.width - 8, 44), 2)
            # 畫櫃子把手 (金屬質感)
            pygame.draw.rect(display_surface, (220, 220, 180), (cabinet_rect.centerx - 10, cabinet_rect.y + 12, 20, 4))
            pygame.draw.rect(display_surface, (220, 220, 180), (cabinet_rect.centerx - 10, cabinet_rect.y + 56, 20, 4))
    
            # 畫門
            pygame.draw.rect(display_surface, (80, 40, 20), living_door_rect)
            pygame.draw.rect(display_surface, (120, 60, 30), living_door_rect.inflate(-4, -4))
            pygame.draw.rect(display_surface, (200, 180, 50), (living_door_rect.right - 6, living_door_rect.centery - 2, 4, 8))

    if current_scene == "living_room":
        # 畫玩家
        draw_retro_player(display_surface, player_x, player_y)
    elif current_scene == "bedroom":
        # 畫門
        pygame.draw.rect(display_surface, (80, 40, 20), bedroom_door_rect)
        pygame.draw.rect(display_surface, (120, 60, 30), bedroom_door_rect.inflate(-4, -4))
        pygame.draw.rect(display_surface, (200, 180, 50), (bedroom_door_rect.left + 2, bedroom_door_rect.centery - 2, 4, 8))
        
        # 畫書櫃
        pygame.draw.rect(display_surface, (90, 50, 20), bookshelf_rect)
        pygame.draw.rect(display_surface, (60, 30, 10), bookshelf_rect, 2)
        for i in range(1, 4):
            pygame.draw.line(display_surface, (60, 30, 10), (bookshelf_rect.x, bookshelf_rect.y + i*20), (bookshelf_rect.right, bookshelf_rect.y + i*20), 2)
        pygame.draw.rect(display_surface, (200, 50, 50), (bookshelf_rect.x + 5, bookshelf_rect.y + 5, 8, 15))
        pygame.draw.rect(display_surface, (50, 200, 50), (bookshelf_rect.x + 15, bookshelf_rect.y + 5, 10, 15))
        pygame.draw.rect(display_surface, (50, 50, 200), (bookshelf_rect.x + 8, bookshelf_rect.y + 25, 8, 15))

        # 定義畫電腦桌的函式以便根據玩家位置改變繪製順序
        def draw_bedroom_computer():
            # 畫電腦桌
            pygame.draw.rect(display_surface, (180, 180, 180), computer_desk_rect)
            pygame.draw.rect(display_surface, (120, 120, 120), computer_desk_rect, 2)
            # 螢幕支架與底座
            pygame.draw.rect(display_surface, (60, 60, 60), (computer_desk_rect.centerx - 4, computer_desk_rect.top + 10, 8, 5))
            pygame.draw.rect(display_surface, (80, 80, 80), (computer_desk_rect.centerx - 12, computer_desk_rect.top + 15, 24, 4))
            # 電腦螢幕 (顯示器)
            comp_screen_rect = pygame.Rect(computer_desk_rect.centerx - 20, computer_desk_rect.top - 15, 40, 25)
            pygame.draw.rect(display_surface, (40, 40, 40), comp_screen_rect)
            pygame.draw.rect(display_surface, (100, 255, 100), comp_screen_rect.inflate(-4, -4))
            # 電腦主機 (CPU)
            pygame.draw.rect(display_surface, (30, 30, 30), (computer_desk_rect.centerx + 25, computer_desk_rect.top - 5, 15, 25))
            pygame.draw.rect(display_surface, (50, 100, 255), (computer_desk_rect.centerx + 28, computer_desk_rect.top, 4, 4)) # 電源燈
            # 鍵盤
            pygame.draw.rect(display_surface, (220, 220, 220), (computer_desk_rect.centerx - 20, computer_desk_rect.top + 22, 30, 8))
            # 滑鼠
            pygame.draw.rect(display_surface, (200, 200, 200), (computer_desk_rect.centerx + 15, computer_desk_rect.top + 24, 6, 8))
            pygame.draw.rect(display_surface, (100, 100, 100), (computer_desk_rect.centerx + 15, computer_desk_rect.top + 24, 3, 4)) # 左鍵

        # 決定玩家和電腦桌的繪製順序
        if player_y + player_size - 4 < computer_desk_rect.top + 20: # 以玩家腳底與桌子邊緣比較
            draw_retro_player(display_surface, player_x, player_y)
            draw_bedroom_computer()
        else:
            draw_bedroom_computer()
            draw_retro_player(display_surface, player_x, player_y)

    # 4. 將低解析度畫布放大並貼到真實視窗上
    # 使用 scale 放大不會平滑化，保留像素顆粒感
    scaled_surface = pygame.transform.scale(display_surface, WINDOW_RES)
    screen.blit(scaled_surface, (0, 0))

    # 畫互動提示 (高畫質，畫在 screen 上)
    current_player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    if ui_state == "game":
        # 放大比例
        scale_x = WINDOW_RES[0] / VIRTUAL_RES[0]
        scale_y = WINDOW_RES[1] / VIRTUAL_RES[1]
        prompt_font = high_res_inst_font # 使用高畫質大字體
        
        prompt_text = ""
        if current_scene == "living_room":
            if current_player_rect.colliderect(calendar_proximity_rect):
                prompt_text = "SPACE to open Calendar"
            elif current_player_rect.colliderect(tv_proximity_rect) and calendar_date == datetime.date(2026, 6, 22):
                prompt_text = "SPACE to watch TV"
            elif current_player_rect.colliderect(cabinet_proximity_rect) and calendar_date == datetime.date(2026, 6, 22):
                prompt_text = "SPACE to open Cabinet"
            elif current_player_rect.colliderect(living_door_prox) and calendar_date == datetime.date(2026, 6, 22):
                prompt_text = "SPACE to enter Bedroom"
        elif current_scene == "bedroom":
            if current_player_rect.colliderect(bedroom_door_prox):
                prompt_text = "SPACE to enter Living Room"
            elif current_player_rect.colliderect(bookshelf_prox):
                prompt_text = "Bookshelf"
            elif current_player_rect.colliderect(computer_prox):
                prompt_text = "Computer"
                
        if prompt_text:
            prompt_surf = prompt_font.render(prompt_text, True, (255, 255, 255), (0, 0, 0))
            # 轉換到實際畫面上的座標
            screen_x = (player_x + player_size//2) * scale_x
            screen_y = (player_y - 5) * scale_y
            prompt_rect = prompt_surf.get_rect(midbottom=(screen_x, screen_y))
            screen.blit(prompt_surf, prompt_rect)

    # 畫大型電子日曆介面 (高畫質，直接畫在 screen 上)
    if ui_state == "calendar":
        overlay = pygame.Surface(WINDOW_RES)
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        inst_surf = high_res_inst_font.render("Left/Right: Select | Up/Down: Change | SPACE: Close", True, (200, 200, 200))
        inst_rect = inst_surf.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 130))
        screen.blit(inst_surf, inst_rect)
        
        y_str = str(calendar_date.year)
        m_str = f"{calendar_date.month:02d}"
        d_str = f"{calendar_date.day:02d}"
        
        color_normal = (100, 255, 100)
        color_selected = (255, 255, 0)
        
        y_color = color_selected if calendar_selection == 0 else color_normal
        m_color = color_selected if calendar_selection == 1 else color_normal
        d_color = color_selected if calendar_selection == 2 else color_normal
        
        y_surf = high_res_big_font.render(y_str, True, y_color)
        m_surf = high_res_big_font.render(m_str, True, m_color)
        d_surf = high_res_big_font.render(d_str, True, d_color)
        slash1 = high_res_big_font.render("/", True, color_normal)
        slash2 = high_res_big_font.render("/", True, color_normal)
        
        total_width = y_surf.get_width() + slash1.get_width() + m_surf.get_width() + slash2.get_width() + d_surf.get_width() + 40
        start_x = (WINDOW_RES[0] - total_width) // 2
        y_pos = WINDOW_RES[1] // 2 - 50
        
        screen.blit(y_surf, (start_x, y_pos))
        start_x += y_surf.get_width() + 10
        screen.blit(slash1, (start_x, y_pos))
        start_x += slash1.get_width() + 10
        screen.blit(m_surf, (start_x, y_pos))
        start_x += m_surf.get_width() + 10
        screen.blit(slash2, (start_x, y_pos))
        start_x += slash2.get_width() + 10
        screen.blit(d_surf, (start_x, y_pos))

    # 畫電視介面
    elif ui_state == "tv":
        overlay = pygame.Surface(WINDOW_RES)
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # 電視外框
        tv_rect_large = pygame.Rect(WINDOW_RES[0]//2 - 300, WINDOW_RES[1]//2 - 200, 600, 400)
        pygame.draw.rect(screen, (40, 40, 40), tv_rect_large)
        inner_rect = tv_rect_large.inflate(-20, -20)
        pygame.draw.rect(screen, (10, 10, 10), inner_rect)
        
        # 顯示圖片或預設文字
        if tv_image:
            scaled_img = pygame.transform.scale(tv_image, (inner_rect.width, inner_rect.height))
            screen.blit(scaled_img, inner_rect.topleft)
        else:
            tv_text = high_res_big_font.render("TV is ON", True, (255, 255, 255))
            tv_text_rect = tv_text.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1]//2 - 30))
            screen.blit(tv_text, tv_text_rect)
        
        inst_surf = high_res_inst_font.render("SPACE: Close TV", True, (200, 200, 200))
        inst_rect = inst_surf.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 130))
        screen.blit(inst_surf, inst_rect)

    # 畫櫃子介面
    elif ui_state == "cabinet":
        overlay = pygame.Surface(WINDOW_RES)
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # 畫大櫃子
        cab_w, cab_h = 400, 440
        cab_rect = pygame.Rect(WINDOW_RES[0]//2 - cab_w//2, WINDOW_RES[1]//2 - cab_h//2 - 40, cab_w, cab_h)
        pygame.draw.rect(screen, CABINET_COLOR, cab_rect)
        pygame.draw.rect(screen, (80, 40, 10), cab_rect, 5)
        
        # 抽屜 1
        d1_rect = pygame.Rect(cab_rect.x + 20, cab_rect.y + 30, cab_w - 40, 180)
        color1 = (255, 255, 0) if cabinet_selection == 0 else (180, 120, 50)
        pygame.draw.rect(screen, color1, d1_rect, 5)
        if cabinet_drawer1_open:
            pygame.draw.rect(screen, (50, 30, 10), d1_rect.inflate(-10, -10))
            if not has_flashlight:
                draw_flashlight_icon(screen, d1_rect.centerx, d1_rect.centery, 120)
        else:
            pygame.draw.rect(screen, (100, 60, 20), d1_rect.inflate(-10, -10))
            pygame.draw.rect(screen, (200, 150, 50), (d1_rect.centerx - 40, d1_rect.centery - 10, 80, 20)) # handle
            
        # 抽屜 2
        d2_rect = pygame.Rect(cab_rect.x + 20, cab_rect.y + 230, cab_w - 40, 180)
        color2 = (255, 255, 0) if cabinet_selection == 1 else (180, 120, 50)
        pygame.draw.rect(screen, color2, d2_rect, 5)
        if cabinet_drawer2_open:
            pygame.draw.rect(screen, (50, 30, 10), d2_rect.inflate(-10, -10))
        else:
            pygame.draw.rect(screen, (100, 60, 20), d2_rect.inflate(-10, -10))
            pygame.draw.rect(screen, (200, 150, 50), (d2_rect.centerx - 40, d2_rect.centery - 10, 80, 20)) # handle
            # 鎖頭
            pygame.draw.circle(screen, (50, 50, 50), (d2_rect.centerx, d2_rect.centery - 40), 15)
            pygame.draw.rect(screen, (50, 50, 50), (d2_rect.centerx - 5, d2_rect.centery - 40, 10, 25))
            
        # 顯示訊息
        if cabinet_message:
            msg_surf = high_res_inst_font.render(cabinet_message, True, (255, 100, 100))
            msg_rect = msg_surf.get_rect(center=(WINDOW_RES[0]//2, cab_rect.top - 20))
            screen.blit(msg_surf, msg_rect)
            
        inst_surf = high_res_inst_font.render("Up/Down: Select | SPACE: Open/Interact | ESC: Close", True, (200, 200, 200))
        # 放在櫃子與道具格子之間
        inst_rect = inst_surf.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 130))
        screen.blit(inst_surf, inst_rect)

    # 畫電腦迷你遊戲
    elif ui_state == "computer":
        overlay = pygame.Surface(WINDOW_RES)
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # 標題
        title_surf = high_res_big_font.render("STREET FIGHTER", True, (255, 50, 50))
        title_rect = title_surf.get_rect(center=(WINDOW_RES[0]//2, 100))
        screen.blit(title_surf, title_rect)
        
        # 血條與分數
        p_hp_rect = pygame.Rect(50, 200, 300, 30)
        e_hp_rect = pygame.Rect(WINDOW_RES[0] - 350, 200, 300, 30)
        pygame.draw.rect(screen, (255, 0, 0), p_hp_rect)
        pygame.draw.rect(screen, (255, 0, 0), e_hp_rect)
        if rt_p1["hp"] > 0:
            pygame.draw.rect(screen, (0, 255, 0), (50, 200, 3 * rt_p1["hp"], 30))
        if rt_p2["hp"] > 0:
            pygame.draw.rect(screen, (0, 255, 0), (WINDOW_RES[0] - 350 + (300 - 3 * rt_p2["hp"]), 200, 3 * rt_p2["hp"], 30))
        
        p_text = high_res_inst_font.render(f"PLAYER 1 (Wins: {fighter_player_wins})", True, (255, 255, 255))
        e_text = high_res_inst_font.render(f"Computer (Wins: {fighter_enemy_wins})", True, (255, 255, 255))
        screen.blit(p_text, (50, 160))
        screen.blit(e_text, (WINDOW_RES[0] - 350, 160))
        
        # 畫地板
        pygame.draw.rect(screen, (100, 100, 100), (0, 550, WINDOW_RES[0], 10))

        # 畫對戰人物
        for p, is_zangief in [(rt_p1, False), (rt_p2, True)]:
            if p["invul_timer"] % 4 > 1: # 閃爍無敵狀態
                continue
            
            if is_zangief:
                draw_zangief(screen, p["x"], p["y"], p["dir"], p["state"], p["hp"], p["invul_timer"])
                if p["state"] == "attacking":
                    hx = p["x"] + 40 if p["dir"] == 1 else p["x"] - 60
                    pygame.draw.rect(screen, (255, 255, 0), (hx, p["y"] + 20, 60, 20))
            else:
                color = p["color"]
                if p["hp"] <= 0: color = (100, 100, 100)
                
                pygame.draw.rect(screen, color, (p["x"], p["y"], 40, 80))
                
                eye_x = p["x"] + 25 if p["dir"] == 1 else p["x"] + 5
                pygame.draw.rect(screen, (255, 255, 255), (eye_x, p["y"] + 10, 10, 10))
                pygame.draw.rect(screen, (0, 0, 0), (eye_x + (4 if p["dir"]==1 else 2), p["y"] + 13, 4, 4))
                
                if p["state"] == "attacking":
                    hx = p["x"] + 40 if p["dir"] == 1 else p["x"] - 60
                    pygame.draw.rect(screen, (255, 255, 0), (hx, p["y"] + 20, 60, 20))
        
        # 顯示訊息
        msg_color = (255, 255, 0) if fighter_state == "fighting" else (100, 255, 100)
        msg_surf = high_res_inst_font.render(fighter_message, True, msg_color)
        msg_rect = msg_surf.get_rect(center=(WINDOW_RES[0]//2, 400))
        screen.blit(msg_surf, msg_rect)
        
        inst_surf = high_res_inst_font.render("ESC: Close Game", True, (200, 200, 200))
        inst_rect = inst_surf.get_rect(center=(WINDOW_RES[0]//2, WINDOW_RES[1] - 130))
        screen.blit(inst_surf, inst_rect)

    # 畫物品欄 (Inventory Bar)
    inv_slot_size = 60
    inv_slots = 5
    inv_start_x = (WINDOW_RES[0] - (inv_slots * (inv_slot_size + 10))) // 2
    inv_y = WINDOW_RES[1] - 80

    for i in range(inv_slots):
        slot_rect = pygame.Rect(inv_start_x + i * (inv_slot_size + 10), inv_y, inv_slot_size, inv_slot_size)
        border_color = (255, 255, 0) if i == selected_inv_slot else (200, 200, 200)
        pygame.draw.rect(screen, (40, 40, 40), slot_rect)
        pygame.draw.rect(screen, border_color, slot_rect, 3 if i == selected_inv_slot else 2)
        if i < len(inventory):
            if inventory[i] == "Flashlight":
                draw_flashlight_icon(screen, slot_rect.centerx, slot_rect.centery, 50)
            elif inventory[i] == "Key":
                draw_key_icon(screen, slot_rect.centerx, slot_rect.centery, 50)

    pygame.display.flip()
    
    # 控制更新頻率 (60 FPS)
    clock.tick(60)

pygame.quit()
sys.exit()
