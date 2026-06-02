# 碰撞位置定義表 — retro_game.py

> 每次新增或修改物件時同步更新此檔。  
> **修改後請把新數值貼給 Claude，Claude 會更新 `retro_game.py` 並 commit。**  
> 直接改這個檔案不會自動同步到程式。

---

## 各房間玩家移動邊界（`ROOM_BOUNDS`）

> 對應 `retro_game.py` 中的 `ROOM_BOUNDS` dict。  
> 座標空間：虛擬 **320 × 240**，`player_size = 20`  
> - `max_x` 上限 = 320 − 20 = 300（右牆內縮越多數值越小）  
> - `max_y` 上限 = 240 − 20 = 220（底牆內縮越多數值越小）

| 房間 | min_x | max_x | min_y | max_y | 說明 |
|------|------:|------:|------:|------:|------|
| `living_room` | 15 | 280 | 30 | 200 | x 還原，y 保留 |
| `bedroom`     | 12 | 288 | 12 | 208 | 待校正 |
| `bathroom`    | 12 | 288 | 12 | 208 | 待校正 |

---

## 座標系統

| 項目 | 值 |
|------|-----|
| 虛擬空間 | `320 × 240`（所有 Rect 數字均在此空間） |
| 視窗大小 | `960 × 760`（遊戲區 960 × 700） |
| 換算 x | 虛擬 x × **3.0** = 視窗 x |
| 換算 y | 虛擬 y × **2.917** ≈ 視窗 y |
| Rect 格式 | `(x, y, width, height)` = 左上角座標 + 寬高 |

---

## 牆面邊界常數

> 定義透視視角的後牆線位置，物件貼齊 `_ROOM_VPT` 這條線才符合視覺。

| 常數 | 目前值 | 說明 |
|------|--------|------|
| `_ROOM_VPT` | `26` | 後牆頂部 y（天花板接縫，物件應 ≥ 此值） |
| `_ROOM_VPY` | `70` | 後牆底部 y（地板起點） |
| `_ROOM_LWX` | `60` | 後牆左側 x |
| `_ROOM_RWX` | `260` | 後牆右側 x |
| `_PLAYER_MIN_Y` | `12` | 玩家可走到的最上方 y |

---

## 客廳（Living Room）

### 物件碰撞 Rect

| 變數 | 目前值 `(x, y, w, h)` | x 範圍 | y 範圍 | 說明 |
|------|----------------------|--------|--------|------|
| `desk_rect` | `(83, 28, 132, 30)` | 83–215 | 28–58 | 電視桌（月曆觸發使用此 centerx；h≤38 才可觸發） |
| `tv_rect` | `(110, 28, 55, 28)` | 110–165 | 28–56 | 電視螢幕 |
| `cabinet_rect` | `(20, 35, 28, 50)` | 20–48 | 35–85 | 左側抽屜桌 |
| `living_door_rect` | `(15, 80, 10, 80)` | 15–25 | 80–160 | 左牆門 → 臥室 |
| `bathroom_door_rect` | `(288, 80, 10, 80)` | 288–298 | 80–160 | 右牆門 → 廁所 |
| `main_door_rect` | `(140, 0, 52, 18)` | 140–192 | 0–18 | 上牆大門（y=0 固定） |
| `sofa_rect` | `(100, 210, 100, 50)` | 100–200 | 210–260 | 沙發 |

### 電燈開關（1988 場景專用）

| 變數 | 目前值 | x 範圍 | y 範圍 | 說明 |
|------|--------|--------|--------|------|
| `_SW_NX, _SW_NY` | `258, 18` | — | — | 開關左上角座標 |
| `_SW_NW, _SW_NH` | `11, 12` | 258–269 | 18–30 | 開關寬高 |
| `light_switch_prox` | `(238, 18, 51, 50)` | 238–289 | 18–68 | 感應範圍 = `(NX-20, NY, NW+40, 50)` |

### 感應範圍（Proximity Rect）

> `cx` = `rect.centerx`，`cy` = `rect.centery`（pygame Rect 中心座標屬性）

| 物件 | 計算方式 | 感應核心 | inflate |
|------|---------|---------|---------|
| 月曆（desk） | `Rect(desk_rect.centerx-12, desk_rect.centery-12, 24, 24).inflate(12, 16)` | 24×24 | +12, +16 |
| 電視（tv） | `Rect(tv_rect.centerx-12, tv_rect.centery-12, 24, 24).inflate(12, 16)` | 24×24 | +12, +16 |
| cabinet | `cabinet_rect.inflate(16, 16)` | — | +16, +16 |
| living_door | `living_door_rect.inflate(20, 20)` | — | +20, +20 |
| bathroom_door | `bathroom_door_rect.inflate(20, 20)` | — | +20, +20 |
| main_door | `main_door_rect.inflate(16, 16)` | — | +16, +16 |

---

## 臥室（Bedroom）

### 物件碰撞 Rect

| 變數 | 目前值 `(x, y, w, h)` | x 範圍 | y 範圍 | 說明 |
|------|----------------------|--------|--------|------|
| `bedroom_door_rect` | `(302, 142, 18, 65)` | 302–320 | 142–207 | 右牆門 → 客廳 |
| `bookshelf_rect` | `(18, 12, 57, 97)` | 18–75 | 12–109 | 左側書架 |
| `computer_desk_rect` | `(78, 12, 139, 90)` | 78–217 | 12–102 | 電腦桌（上牆中央） |

### 感應範圍（Proximity Rect）

| 物件 | inflate |
|------|---------|
| bedroom_door | `inflate(20, 20)` |
| bookshelf | `inflate(16, 16)` |
| computer | `inflate(16, 16)` |

---

## 廁所（Bathroom）

### 物件碰撞 Rect

| 變數 | 目前值 `(x, y, w, h)` | x 範圍 | y 範圍 | 說明 |
|------|----------------------|--------|--------|------|
| `bathroom_exit_rect` | `(0, 77, 17, 83)` | 0–17 | 77–160 | 左牆門 → 客廳 |
| `pipe_rect` | `(87, 3, 94, 37)` | 87–181 | 3–40 | 上牆漏水管 |
| `sink_rect` | `(76, 37, 63, 55)` | 76–139 | 37–92 | 洗手台 |
| `toilet_rect` | `(146, 40, 56, 55)` | 146–202 | 40–95 | 馬桶（鐵箱/架子位置） |
| `mirror_rect` | `(55, 12, 90, 35)` | 55–145 | 12–47 | 鏡子（2026 only）待 F1 校正 |
| `bathtub_rect` | `(230, 60, 75, 80)` | 230–305 | 60–140 | 浴缸（2026 only）待 F1 校正 |

### 感應範圍（Proximity Rect）

| 物件 | inflate |
|------|---------|
| bathroom_exit | `inflate(20, 20)` |
| mirror | `inflate(24, 80)` |
| bathtub | `inflate(16, 16)` |
| sink | `inflate(16, 16)` |
| pipe | `inflate(12, 12)` |
| toilet | `inflate(16, 16)` |

---

## 更新規則

新增或修改物件時，**必須同步更新**：

1. `retro_game.py` 中的 `pygame.Rect(...)` 定義
2. `_do_proximity_check()` 中的 proximity 判斷條件
3. SPACE 鍵處理器中的 `colliderect` 判斷
4. `DIALOGUE_MAP` 新增對應對話文字
5. `_trigger_action()` 新增動作邏輯
6. **本 `COLLISIONS.md` 對應表格**

---

*最後更新：Round 17 / commit `900a052`*
