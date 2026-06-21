# 修復指南 - 根據詳細診斷更新

## 修復1：硬幣碰撞檢測失敗

**根本原因**（已確認）：
- player_rect在第1748行計算（循環開始）
- 玩家邊界檢查（第2508-2519行）修改了player_x/y
- 硬幣碰撞檢測（第2370-2396行）執行時，player_rect已過期
- player_rect直到第2521行才重新計算

**修復方案**：
在硬幣碰撞檢測**之前**（第2370行前）重新計算player_rect

```python
# 在第2370行之前添加：
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

# 然後執行硬幣碰撞檢測（第2370-2396行）
if current_scene == "living_room" and calendar_date == DATE_1994_10_23:
    for coin in coin_items[:]:
        # ... 硬幣更新邏輯 ...
```

**優先級**：🔴 **立即修復** - 只需添加一行代碼

---

## 修復2：Chi寶寶邊界檢查無效

**根本原因**（已確認）：
- 邊界檢查邏輯正確（`<=` 和 `>=`）
- 但邊界值(40, 268, 75, 195)未考慮Chi寶寶碰撞體大小
- living_room邊界較紧（MAX_X=268，屏幕寬=320）
- Chi寶寶使用中心座標檢查，需內縮邊界

**修復方案**：
將邊界值內縮，考慮Chi寶寶大小（假設16x16碰撞體）

```python
# 第2352行改為：
MIN_X, MAX_X, MIN_Y, MAX_Y = ROOM_BOUNDS.get(current_scene, (40, 268, 75, 195))

# 添加內縮（以考慮Chi寶寶碰撞體大小）：
COLLISION_SIZE = 8  # Chi寶寶半寬
MIN_X += COLLISION_SIZE
MAX_X -= COLLISION_SIZE
MIN_Y += COLLISION_SIZE
MAX_Y -= COLLISION_SIZE
```

**或簡單修改邊界值**（如果Chi寶寶大小不變）：
```python
# living_room原值：(40, 268, 75, 195)
# 內縮8像素後：(48, 260, 83, 187)
MIN_X, MAX_X, MIN_Y, MAX_Y = ROOM_BOUNDS.get(current_scene, (48, 260, 83, 187))
```

**優先級**：🔴 **立即修復** - 調整邊界值邏輯

---

## 驗收標準（自動化）

### 驗收1：硬幣被正確收集
```python
# 在inventory更新後檢查：
if '扭蛋硬幣_去背.png' in inventory:
    print("✅ 硬幣收集成功")
else:
    print("❌ 硬幣未被添加到inventory")
```

### 驗收2：Chi寶寶邊界限制生效
```python
# 在每幀更新後檢查：
MIN_X, MAX_X, MIN_Y, MAX_Y = ROOM_BOUNDS.get(current_scene, (...))
if MIN_X <= chi_baby_x <= MAX_X and MIN_Y <= chi_baby_y <= MAX_Y:
    print("✅ Chi寶寶在邊界內")
else:
    print(f"❌ Chi寶寶超出邊界: ({chi_baby_x}, {chi_baby_y}), 邊界: ({MIN_X}-{MAX_X}, {MIN_Y}-{MAX_Y})")
```

---

## 實施步驟（簡化版）

### 步驟1：修復硬幣碰撞
1. 打開retro_game.py
2. 找到第2370行（硬幣更新開始）
3. 在其前面添加：`player_rect = pygame.Rect(player_x, player_y, player_size, player_size)`

### 步驟2：修復Chi寶寶邊界  
1. 找到第2352行（邊界值獲取）
2. 修改下一行（第2353行左右）添加邊界內縮邏輯

### 步驟3：測試驗收
1. 運行遊戲
2. 檢查inventory中是否出現硬幣
3. F1查看邊界是否限制了Chi寶寶
