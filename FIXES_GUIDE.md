# 遊戲缺陷修復指南

## 問題1：Chi寶寶邊界超出限制

**症狀**：F1顯示綠色邊框正確，但Chi寶寶在邊框外移動

**根本原因**：邊界檢查代碼存在但邏輯可能有問題

**修復位置**：`retro_game.py` 第 2347-2368 行

**當前代碼結構**：
```python
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
```

**需要檢查的問題**：
1. [ ] `MIN_X, MAX_X, MIN_Y, MAX_Y` 是否正確從ROOM_BOUNDS獲取？
2. [ ] Chi寶寶移動代碼（設置chi_baby_x、chi_baby_y）是否在邊界檢查**之後**執行？
3. [ ] 邊界檢查是否需要加上player_rect的碰撞檢查邏輯（如玩家邊界檢查）？

**可能的修復**：
- 確認邊界檢查在Chi寶寶移動代碼之後執行
- 添加調試輸出確認邊界值
- 可能需要添加`_check_collision()`碰撞檢查

---

## 問題2：硬幣沒有被生成/收集

**症狀**：
- 沒看到控制台中的`[DEBUG] Chi baby interaction triggered`
- 沒有硬幣掉落
- 硬幣沒有添加到inventory

**根本原因**：Chi寶寶互動代碼可能未被觸發

**修復位置**：`retro_game.py` 第 1646-1662 行（Chi寶寶互動代碼）

**需要檢查的問題**：
1. [ ] 是否已進入1994年10月23日？（檢查 `calendar_date == DATE_1994_10_23`）
2. [ ] 是否持有Chi的奶嘴？（inventory中應有`'Chi的奶嘴_去背.png'`）
3. [ ] `chi_baby_has_pacifier`是否為False？
4. [ ] 是否靠近Chi寶寶並按正確的互動鍵？

**檢查互動觸發流程**：
1. 行 1323-1328：proximity檢查
   ```python
   if calendar_date == DATE_1994_10_23 and "Chi的奶嘴_去背.png" in inventory and not chi_baby_has_pacifier:
       # 顯示Chi Baby提示
   ```

2. 行 1868-1875：按Z鍵觸發互動
   ```python
   if event.key == pygame.K_z:  # 確認是Z鍵觸發
       if _obj and _obj in DIALOGUE_MAP:
           dialogue_active = True
           dialogue_object = _obj
   ```

3. 行 1646-1662：Chi寶寶互動代碼執行

**修復清單**：
1. [ ] 確認proximity檢查邏輯正確（第1323行條件）
2. [ ] 確認按Z鍵觸發互動（可能需要改為其他鍵，如SPACE）
3. [ ] 確認`_obj == "chi_baby"`被正確設置
4. [ ] 添加更多debug輸出追踪互動流程

**建議的Debug輸出位置**：
- 第1323行後：輸出proximity檢查結果
- 第1868行後：輸出鍵盤事件和_obj值
- 第1646行後：輸出互動是否被觸發

---

## 問題3：櫃子圖片沒改變

**症狀**：選擇下層後按上到上層，圖片沒有改變

**根本原因**：
- 櫃子狀態管理邏輯
- 或圖片加載失敗

**修復位置**：
- `retro_game.py` 第 2044-2046 行（drawer狀態管理）
- `retro_game.py` 第 1390-1405 行（_cab_current_img()邏輯）

**檢查項目**：
1. [ ] 當按上/下鍵導航時，`cabinet_selection`是否正確改變？
2. [ ] 當打開drawer2時，`cabinet_drawer1_open`是否被設為False？
3. [ ] `_cab_current_img()`是否返回正確的圖片？
4. [ ] `cab_img_l1`, `cab_img_l2`等圖片是否成功加載？

**測試流程**：
1. [ ] 打開櫃子UI
2. [ ] 選擇下層（drawer1）
3. [ ] 按上鍵到上層（drawer2）
4. [ ] **檢查顯示的圖片是否改變**

---

## 通用修復步驟

### 步驟1：添加Debug輸出
在以下位置添加print語句來追踪執行流程：

**位置1**：Chi寶寶proximity檢查（第1323行後）
```python
print(f"[DEBUG PROXIMITY] Date: {calendar_date}, Has pacifier: {'Chi的奶嘴_去背.png' in inventory}, Pacifier given: {chi_baby_has_pacifier}")
```

**位置2**：鍵盤事件處理（第1868行後）
```python
print(f"[DEBUG KEY] Key pressed: {event.key}, _obj: {_obj}, dialogue_active: {dialogue_active}")
```

**位置3**：Chi寶寶邊界檢查（第2347行前）
```python
print(f"[DEBUG BOUNDARY] Chi baby position: ({chi_baby_x}, {chi_baby_y}), Bounds: ({MIN_X}, {MAX_X}, {MIN_Y}, {MAX_Y})")
```

### 步驟2：運行遊戲並收集Debug輸出
1. 添加上述debug輸出
2. 進入1994年10月23日
3. 執行各個測試步驟
4. 複製控制台輸出並分析

### 步驟3：根據Debug輸出調整代碼
- 如果Chi baby interaction沒被觸發 → 檢查proximity/keyboard邏輯
- 如果Chi baby邊界沒限制 → 檢查邊界檢查邏輯或碰撞檢查

---

## 優先修復順序

**優先1**：Chi寶寶邊界（F1顯示邊框正確，但實際超出）
**優先2**：硬幣互動觸發（添加debug輸出確認觸發狀態）
**優先3**：櫃子圖片（驗證狀態管理邏輯）

---

## 測試驗收標準

### Chi寶寶邊界
- [ ] F1顯示綠色邊框
- [ ] Chi寶寶移動時不超出綠色邊框
- [ ] Chi寶寶在邊框內來回移動

### 硬幣系統
- [ ] 給Chi寶寶奶嘴後看到控制台`[DEBUG] Coin spawned`
- [ ] 硬幣掉落動畫顯示
- [ ] 走動碰到硬幣後看到`[DEBUG] Coin collected`
- [ ] 硬幣出現在inventory中

### 櫃子UI
- [ ] 選擇下層後按上到上層，圖片改變
- [ ] 根據手電筒/遙控器取得狀態，顯示正確圖片
