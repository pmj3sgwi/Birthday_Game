# Retro Game — 開發者協作指南

> **適用版本**：Round 16 完成後（commit `4d2245c`）  
> **主程式**：`retro_game.py`（約 2300 行）  
> **引擎**：Python 3.8 + pygame 2.6.1

---

## 目錄

1. [專案結構](#1-專案結構)
2. [解析度系統](#2-解析度系統)
3. [全域狀態變數](#3-全域狀態變數)
4. [場景系統（current_scene）](#4-場景系統)
5. [物件碰撞與互動系統](#5-物件碰撞與互動系統)
6. [對話框系統（dialogue）](#6-對話框系統)
7. [時間旅行系統（calendar）](#7-時間旅行系統)
8. [謎題鏈與劇情流程](#8-謎題鏈與劇情流程)
9. [1988 場景的特殊架構](#9-1988-場景的特殊架構)
10. [UI 狀態機（ui_state）](#10-ui-狀態機)
11. [迷你遊戲](#11-迷你遊戲)
12. [道具欄（inventory）](#12-道具欄)
13. [資源清單（picture/）](#13-資源清單)
14. [建置與發行（PyInstaller）](#14-建置與發行)
15. [常見地雷與注意事項](#15-常見地雷與注意事項)
16. [新增物件 / 場景的標準流程](#16-新增物件--場景的標準流程)

---

## 1. 專案結構

```
Game/
├── retro_game.py          # 主程式（所有邏輯）
├── retro_game.spec        # PyInstaller 打包設定
├── dist/
│   └── retro_game.exe     # 最新發行版
└── picture/               # 所有圖片資源
    ├── 2026_客廳_T.png
    ├── 2026_客廳Original_T.png
    ├── 2026_廁所_T.png
    ├── 2026_房間_T.png
    ├── 1988_客廳_T.png
    ├── 1988_廁所_T.png
    ├── 1988_房間_T.png
    ├── Time_Travel.png
    ├── BB.png / BB_T.png / BB_去背.png ...  # 角色圖（BB = 主角）
    ├── BB_Digi.png / BB_Digi_T.png ...       # 數位版角色
    ├── 08_Back_to_Future.jpg                  # 電視畫面
    ├── SF2.jpg                                # SF2 卡匣圖示
    ├── TETRIS.jpg                             # Tetris 圖示
    └── NotUsing/                              # 舊版背景（不使用）
```

---

## 2. 解析度系統

程式使用**三層解析度**：

| 常數 | 值 | 用途 |
|------|-----|------|
| `VIRTUAL_RES` | `(320, 240)` | 所有碰撞 Rect 的虛擬座標空間（2026 年） |
| `VIRTUAL_RES_1080` | `(1920, 1080)` | 1988 場景背景渲染空間 |
| `WINDOW_RES` | `(960, 760)` | 實際視窗大小 |
| `_HIRES` | `(960, 700)` | 場景遊戲區（= 視窗扣掉 60px 給系統） |

### 座標轉換

```python
# 虛擬座標 → 視窗座標（2026 場景）
_SX = WINDOW_RES[0] / VIRTUAL_RES[0]          # = 3.0
_SY = (WINDOW_RES[1] - 60) / VIRTUAL_RES[1]   # ≈ 2.917

pixel_x = int(virtual_x * _SX)
pixel_y = int(virtual_y * _SY)
```

> **規則**：碰撞偵測一律用 `VIRTUAL_RES (320×240)` 的 `pygame.Rect`；繪製時才乘以 `_SX / _SY` 轉換到視窗座標。

### 道具欄佈局

```
bar_y = WINDOW_RES[1] - 92 = 668
黑底覆蓋區：y = 662 → 760
對話框 / 頭像下邊界：WINDOW_RES[1] - 98 = 662
```

---

## 3. 全域狀態變數

### 核心遊戲狀態

| 變數 | 初始值 | 說明 |
|------|--------|------|
| `player_x`, `player_y` | `(240-50, 150)` | 虛擬座標中的玩家位置 |
| `player_size` | `20` | 玩家碰撞方塊邊長 |
| `player_dir` | `"down"` | 朝向，決定播哪個走路動畫 |
| `player_moving` | `False` | 是否按住移動鍵 |
| `current_scene` | `"living_room"` | 當前場景 |
| `ui_state` | `"game"` | UI 模式（見第 10 節） |
| `calendar_date` | `2026-06-18` | 當前時間旅行日期 |
| `room_lights_on` | `False` | 1988 場景燈光開關 |

### 謎題進度

| 變數 | 值域 | 說明 |
|------|------|------|
| `iron_box_state` | 0–4 | 鐵箱謎題進度（見第 8 節） |
| `bookshelf_order` | list | 書架當前排序 |
| `bookshelf_unlocked` | bool | 書架謎題是否解開 |
| `tetris_cart_spawned` | bool | Tetris 卡匣是否在桌上 |
| `door_puzzle_state` | [F,F,F,F] | 大門謎題四個開關 |
| `cup_state` | 0–1 | 杯子狀態（0=完整，1=碎） |

### 對話框狀態

| 變數 | 說明 |
|------|------|
| `dialogue_active` | 是否顯示對話框 |
| `dialogue_object` | 當前對話對象的 key（如 `"tv"`） |
| `dialogue_text` | 對話框顯示的文字 |
| `dialogue_has_choices` | True = Yes/No；False = SPACE 繼續 |
| `dialogue_choice` | 0 = Yes，1 = No |
| `dialogue_triggered` | True = 觸發後進入 TV/cabinet UI，頭像持續顯示 |

---

## 4. 場景系統

### 場景列表

| `current_scene` | 場景名稱 | 可前往 |
|-----------------|---------|--------|
| `"living_room"` | 客廳 | bedroom（左門）、bathroom（右門） |
| `"bedroom"` | 臥室 | living_room（右門） |
| `"bathroom"` | 廁所 | living_room（左門） |

### 場景轉換

場景轉換透過 `_trigger_action()` 執行，轉換後會重設玩家位置到對應門口：

```python
# 例：進臥室
current_scene = "bedroom"
player_x = bedroom_door_rect.left - player_size - 10
player_y = bedroom_door_rect.centery - player_size // 2
```

### 碰撞 Rect 位置（虛擬座標 320×240）

**客廳**

| 物件 | Rect (x, y, w, h) | 說明 |
|------|--------------------|------|
| `desk_rect` | `(83, 14, 152, 39)` | 電視桌（含月曆/植物） |
| `tv_rect` | `(109, 14, 72, 35)` | 電視螢幕 |
| `cabinet_rect` | `(5, 14, 39, 43)` | 左側邊桌 |
| `living_door_rect` | `(0, 67, 12, 84)` | 左牆通臥室 |
| `bathroom_door_rect` | `(308, 67, 12, 84)` | 右牆通廁所 |
| `main_door_rect` | `(214, 0, 42, 19)` | 大門（頂部，y≈0） |
| `sofa_rect` | `(71, 180, 162, 44)` | 沙發 |

**臥室**

| 物件 | Rect (x, y, w, h) |
|------|--------------------|
| `bedroom_door_rect` | `(302, 142, 18, 65)` |
| `bookshelf_rect` | `(18, 12, 57, 97)` |
| `computer_desk_rect` | `(78, 12, 139, 90)` |

**廁所**

| 物件 | Rect (x, y, w, h) |
|------|--------------------|
| `bathroom_exit_rect` | `(0, 77, 17, 83)` |
| `pipe_rect` | `(87, 3, 94, 37)` |
| `sink_rect` | `(76, 37, 63, 55)` |
| `toilet_rect` | `(146, 40, 56, 55)` |

---

## 5. 物件碰撞與互動系統

### Proximity（近距感應）Rect

每幀在 `_do_proximity_check()` 計算。近距 Rect = 物件 Rect `.inflate(32, 32)`（每側擴大 16px）。

```python
cabinet_proximity_rect = cabinet_rect.inflate(32, 32)
living_door_prox       = living_door_rect.inflate(32, 32)
# ...
```

### 標籤顯示（`_draw_label`）

玩家進入近距範圍時，在物件上方（靠頂部時改為下方）顯示短名稱。

- 水平：clamp 在 `[half_w, WINDOW_RES[0] - half_w]`，不溢出邊緣
- 垂直：物件頂部 `< text_height + 10` 時改為顯示在物件下方（處理大門靠頂部的情況）

### 新增可互動物件的步驟

1. 在 `DIALOGUE_MAP`（約 line 272）加入 `"key": ("對話文字", has_yes_no)`
2. 在 `_do_proximity_check()`（約 line 1090）加入 proximity 判斷，設定 `prompt_label` 和 `prompt_label_rect`
3. 在 SPACE 鍵處理（約 line 1408）加入 `_obj = "key"` 的判斷
4. 在 `_trigger_action()`（約 line 1225）加入 `elif obj == "key":` 處理邏輯

---

## 6. 對話框系統

### 流程

```
玩家按 SPACE
  → 判斷最近物件 (_obj)
  → dialogue_active = True，設定 dialogue_text / dialogue_has_choices
  → draw_dialogue_ui() 渲染：右下角頭像（上半身 3× 放大） + 左側文字框
  → 玩家選擇（←/→ 切換 Yes/No，SPACE 確認，ESC 取消）
  → 選 Yes → _trigger_action(obj)
  → 選 No / ESC → dialogue_active = False（什麼都不做）
```

### `draw_dialogue_ui(surface)` 佈局

- **頭像**：右下角，距底部 `WINDOW_RES[1] - 98`（道具欄上方），只顯示上半身（裁切高度 × 3 放大）
- **文字框**：頭像左側，寬度 `min(400, 視窗寬 - 頭像寬 - margin×3)`，高度 165px

### `dialogue_triggered` 的作用

當玩家確認進入需要顯示 UI 的互動（TV、大門）時設為 `True`，使頭像在 UI 模式中持續顯示。  
執行立即完成的動作（移動房間、撿道具）時設為 `False`。

---

## 7. 時間旅行系統

### 日期管理

```python
calendar_date      # 當前日期（datetime.date）
prev_calendar_date # 上一幀的日期（用於偵測日期變更）
DATE_1988 = datetime.date(1988, 6, 22)
```

### 日期變更副作用（主迴圈開頭）

```python
if calendar_date != prev_calendar_date:
    if prev_calendar_date == DATE_1988 and calendar_date != DATE_1988:
        if iron_box_state == 2:
            iron_box_state = 3   # 鐵箱生鏽
    if calendar_date == DATE_1988:
        room_lights_on = False   # 1988 進入時燈是暗的
```

### 日曆 UI（`draw_grid_calendar_ui`）

三階段選擇：year → month → day，按 SPACE 進入下一階段，ESC 返回。

- 日曆方塊位置：`cal_x = (WINDOW_RES[0] - cal_w) // 2 + 130`（右移 130px）
- 文字中心：`_cal_cx = cal_x + cal_w // 2 = 610`
- 開啟日曆時道具欄隱藏：`if ui_state != "calendar": draw_inventory_bar()`

### 場景背景選擇邏輯

| `calendar_date` | 客廳背景 |
|-----------------|---------|
| `2026-06-22`（劇情觸發日） | `bg_living`（2026_客廳_T.png） |
| 其他 2026 日期 | `bg_living_orig`（2026_客廳Original_T.png） |
| `1988-06-22` | 1988 場景（特殊渲染路徑，見第 9 節） |

---

## 8. 謎題鏈與劇情流程

### 主線順序

```
起始：2026-06-18，客廳
  │
  ├─ 走近電視桌日曆 → SPACE → 日曆 UI → 設定日期 2026-06-22
  │   └─ 日期 = 2026-06-22 解鎖：TV、Cabinet、Front Door 互動
  │
  ├─ Cabinet（左側桌）
  │   └─ 抽屜1 = 手電筒（Flashlight）
  │   └─ 抽屜2 = 鑰匙（Key）
  │
  ├─ 臥室 → 書架謎題（Bookshelf）
  │   └─ 解鎖書架 → SF2 卡匣出現在某處
  │
  ├─ 臥室 → 電腦 + SF2 卡匣 → Street Fighter 迷你遊戲
  │   └─ 擊敗電腦 → 某道具獲得
  │
  ├─ 電視桌 → 日曆 → 1988-06-22（時間旅行）
  │   ├─ 1988 客廳：漆黑 → 找手電筒（cabinet 抽屜1）
  │   ├─ 找到電燈開關（light switch，電視右側牆） → room_lights_on = True
  │   ├─ 廁所 → toilet 旁 Iron Box → 撿起（iron_box_state = 1）
  │   └─ 廁所 → pipe 旁放鐵箱（iron_box_state = 2）
  │
  ├─ 日曆 → 回到 2026
  │   └─ iron_box_state 2 → 3（鐵箱生鏽）
  │
  ├─ 廁所 → toilet 旁鏽箱（iron_box_state = 3）→ 撬開
  │   └─ iron_box_state = 4，獲得 Strange Cube
  │
  └─ 大門（Front Door）→ 謎題 → 出口
```

### `iron_box_state` 值域

| 值 | 狀態 | 說明 |
|----|------|------|
| 0 | 廁所 toilet 旁（1988） | 未撿取 |
| 1 | 持有中（1988） | 已撿起 |
| 2 | 放在 pipe 下（1988） | 積水中 |
| 3 | 回到 2026 後（鏽） | 可撬開 |
| 4 | 已撬開 | 得到 Strange Cube |

---

## 9. 1988 場景的特殊架構

1988 場景使用完全不同的渲染路徑，**主迴圈結尾有 `continue`** 跳過 2026 渲染程式碼。

### 架構示意

```python
# 主迴圈中（約 line 1860）
if calendar_date == DATE_1988:
    # ... 1988 場景渲染（背景 1920×1080 縮放 → 視窗）
    screen.blit(render_1988_scene(...), (0, 0))
    # ... 角色 sprite 繪製
    
    _do_proximity_check()          # ← 必須在 continue 之前
    if prompt_label and prompt_label_rect:
        _draw_label(screen)        # ← 同上
    if dialogue_active:
        draw_dialogue_ui(screen)   # ← 同上
    draw_inventory_bar()           # ← 同上
    pygame.display.flip()
    clock.tick(60)
    continue   # ← 跳過所有 2026 渲染程式碼
```

> **陷阱**：在 1988 場景加入任何新的 UI 繪製，必須放在 `continue` 之前，否則不會顯示。

### 1988 光線系統

`render_1988_scene()` 函數：
- `room_lights_on = False`：套用遮罩，只有手電筒半徑（玩家周圍圓形）可見
- `room_lights_on = True`：不套遮罩，全場景可見

---

## 10. UI 狀態機

`ui_state` 控制當前顯示的介面：

| 值 | 說明 | 退出方式 |
|----|------|---------|
| `"game"` | 正常遊戲模式 | — |
| `"calendar"` | 日曆時間旅行 | SPACE（day 階段） |
| `"tv"` | 看電視 | SPACE / ESC |
| `"cabinet"` | 查看邊桌抽屜 | ESC |
| `"computer"` | 電腦（Street Fighter） | ESC |
| `"computer_idle"` | 電腦（無卡匣） | ESC |
| `"tetris"` | Tetris 迷你遊戲 | ESC |
| `"bookshelf"` | 書架謎題 | ESC |
| `"main_door"` | 大門謎題 | ESC |
| `"sink"` | 洗手台 | ESC |
| `"iron_box"` | 鐵箱查看 | ESC |

> `dialogue_active = True` 時，KEYDOWN 事件先被攔截，其他 `ui_state` 鍵盤邏輯不執行（`continue` 跳過）。

---

## 11. 迷你遊戲

### 書架謎題（Bookshelf）

- 初始順序：`["Red", "Blue", "Green"]`
- 正確順序：（待定，在 `bookshelf_unlocked` 設定處）
- 控制：左/右移動 `bookshelf_selection`，SPACE 選取或換位

### Tetris

- 10×20 格，需消 `TETRIS_LINES_WIN = 20` 行
- 落速：`tetris_fall_speed = 350ms`（固定難度）
- 勝利 → 獲得道具或解鎖進度
- `tetris_just_exited`：離開後短暫防止重複觸發

### Street Fighter（`ui_state = "computer"`）

- 需槽位選取 SF2 卡匣才能啟動
- P1：方向鍵移動、SPACE 攻擊、UP 跳躍
- 敵人（CPU）：自動追蹤
- 三局兩勝制（`fighter_player_wins` / `fighter_enemy_wins`）

---

## 12. 道具欄

```python
inventory = []           # 最多 5 個（num_slots = 5）
selected_inv_slot = 0    # 當前選取格（0–4）
```

### 道具 key（inventory 內的字串）

| 字串 | 圖示來源 | 說明 |
|------|---------|------|
| `"Flashlight"` | `draw_flashlight_icon()` | 手電筒 |
| `"Key"` | `draw_key_icon()` | 鑰匙 |
| `"SF2 Cartridge"` | `SF2.jpg` | 街霸2卡匣 |
| `"Tetris Cartridge"` | `draw_cartridge_icon()` 綠色 | 俄羅斯方塊卡匣 |
| `"Remote"` | 藍色方塊 | 遙控器 |
| `"MysteryCube"` | `draw_mystery_cube_icon()` | 神秘方塊 |
| `"Strange Cube 2"` | `draw_mystery_cube_icon()` | 鐵箱內的方塊 |

### 鍵盤切換

數字鍵 `1`–`5` 切換 `selected_inv_slot`（0-based）。

---

## 13. 資源清單

### 圖片命名規則

- `YYYY_場景_T.png`：透明底圖（T = transparent/top-down）
- `BB_*.png`：主角圖（BB = 主角名）
- `BB_Digi_*.png`：數位風格主角
- `_去背`：去背版本

### 角色 Sprite 對應

| 變數 | 圖片 | 說明 |
|------|------|------|
| `player_img_1988_idle` | `BB_T.png` | 1988 靜止 |
| `player_img_1988_walk_*` | `BB_T_去背.png` 等 | 1988 走路四方向 |
| `player_img_2026_idle` | `BB_Digi_T.png` | 2026 靜止 |
| `player_img_2026_walk_*` | `BB_Digi_T_去背.png` 等 | 2026 走路四方向 |

### 加入新圖片

1. 將圖片放入 `picture/`
2. 在程式初始化區（約 line 380）用 `get_resource_path()` 載入：
   ```python
   try:
       _raw = pygame.image.load(get_resource_path(os.path.join("picture", "新圖.png")))
       new_img = pygame.transform.scale(_raw, 目標尺寸)
   except Exception as e:
       print(f"Could not load: {e}")
       new_img = None
   ```
3. 重新打包 exe 時 `picture/` 資料夾會自動包含（`retro_game.spec` 已設定）。

---

## 14. 建置與發行

### 更新 exe

```bash
cd C:\Users\YACHI\Documents\Antigravity\Game
python -m PyInstaller retro_game.spec --noconfirm
```

輸出：`dist/retro_game.exe`

### retro_game.spec 重點設定

```python
datas=[('picture', 'picture')]   # 圖片資料夾打包進 exe
console=False                     # 不顯示命令視窗
upx=True                          # 壓縮
```

### get_resource_path()

用於在 exe 解壓縮暫存目錄（`sys._MEIPASS`）與開發目錄之間自動切換路徑。**所有圖片載入必須透過這個函數**，否則 exe 版本找不到圖片。

### 推送到 GitHub

```bash
git add retro_game.py
git commit -m "描述更新內容"
git push origin main
```

Repository：`https://github.com/pmj3sgwi/Birthday_Game.git`

---

## 15. 常見地雷與注意事項

### ❶ 1988 `continue` 陷阱

在 1988 渲染區塊之後、`continue` 之前的程式碼才會在 1988 場景執行。  
**新增 1988 場景 UI 一定要放在 `continue` 前。**

### ❷ 場景轉換只在 `calendar_date != DATE_1988` 時的 2026 路徑生效

臥室/廁所可以在 1988 進入，但 TV、cabinet、大門等只在 `calendar_date == 2026-06-22` 才有互動。

### ❸ dialogue_active 期間 KEYDOWN 被完全攔截

`if dialogue_active: ... continue` 在所有 `ui_state` 處理之前，導致對話框期間什麼 UI 操作都無效。這是設計行為。

### ❹ 道具欄在日曆開啟時隱藏

`if ui_state != "calendar": draw_inventory_bar()` 只在 2026 路徑。  
1988 路徑的 `draw_inventory_bar()` 永遠執行（1988 不可能進日曆）。

### ❺ 標籤水平邊界夾緊

`_draw_label` 中有：
```python
_half_w = txt.get_width() // 2 + 6
lx = max(_half_w, min(WINDOW_RES[0] - _half_w, lx))
```
靠邊物件（cabinet、bathroom_door、main_door）的標籤不會超出視窗。

### ❻ 大門標籤顯示在下方

`main_door_rect.top = 0`，所以標籤邏輯走「下方」分支（`_obj_top_px < _th + 10`）。

### ❼ 修改 WINDOW_RES 後需要同步更新

- `_HIRES = (WINDOW_RES[0], WINDOW_RES[1] - 60)`
- `bar_y = WINDOW_RES[1] - 92`
- 對話框 `_box_y = WINDOW_RES[1] - 98 - _box_h`
- 日曆 `cal_x = (WINDOW_RES[0] - cal_w) // 2 + 130`

這些都是硬算，改視窗大小要一起更新。

---

## 16. 新增物件 / 場景的標準流程

### 新增可互動物件

1. **定義 Rect**（全域，約 line 200）：
   ```python
   new_obj_rect = pygame.Rect(x, y, w, h)
   ```

2. **加入 DIALOGUE_MAP**（約 line 272）：
   ```python
   "newobj": ("對話文字", True),  # True = Yes/No
   ```

3. **`_do_proximity_check()`** 中加入判斷（約 line 1090）：
   ```python
   elif player_rect.colliderect(new_obj_rect.inflate(32, 32)):
       prompt_label = "New Object"
       prompt_label_rect = new_obj_rect
   ```

4. **SPACE 鍵處理**（約 line 1408）中加入：
   ```python
   elif player_rect.colliderect(new_obj_rect.inflate(32, 32)):
       _obj = "newobj"
   ```

5. **`_trigger_action()`**（約 line 1225）中加入：
   ```python
   elif obj == "newobj":
       # 執行動作
       dialogue_triggered = False
   ```

6. 若需要在 **1988 場景**也能使用：確認放入 `_do_proximity_check()` 時不被 2026-only 判斷擋住。

### 新增場景

1. 新增場景名稱字串到 `current_scene` 的可能值
2. 定義該場景的所有碰撞 Rect
3. 在 `_do_proximity_check()` 加入 `elif current_scene == "new_scene":` 分支
4. 在主迴圈背景選擇邏輯（約 line 1922）加入背景繪製
5. 加入進出場景的轉換動作（`_trigger_action` 中修改 `current_scene`）

---

*最後更新：Round 16 / commit `4d2245c`*
