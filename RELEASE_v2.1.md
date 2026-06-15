# Release v2.1 - Bug Fixes and Game Flow Improvements

**Release Date:** 2026-06-15  
**Version:** v2.1 (Cartridge & UI Polish)  
**Build:** Retro_2D_Game.exe (3.61 MB)  
**Status:** ✅ Stable & Tested

---

## What's New in v2.1

### Major Fixes & Improvements

✨ **Tetris Cartridge System Enhanced**
- Cartridge text now displays **above the object** (won't block calendar)
- Changed cartridge pickup behavior to match game flow:
  - Press SPACE near cartridge → **pick up only** (adds to inventory)
  - Carry to bedroom computer
  - Select Tetris Cartridge from inventory
  - Press SPACE at computer → **launch game**
- Uses TV's collision/proximity rect for reliable detection (8/8 only)

✨ **1988 Year Background Fixes**
- **Bathroom:** Removed iron box overlay artifacts
- **Cabinet UI:** 
  - Removed dark background overlay
  - Now displays proper 1988 living room background
  - Shows correct visual environment
- **TV UI:**
  - Fixed background checkerboard pattern
  - Proper 1988 scene rendering behind TV interface

✨ **UI Polish**
- Calendar proximity rect restored to correct size
- Better separation between Tetris and Calendar triggers
- All background overlays completely removed for clarity

### Bug Fixes Summary

| Issue | Status | Solution |
|-------|--------|----------|
| 1988 cabinet background overlay | ✅ Fixed | Removed dark mask, added 1988_living bg |
| 1988 bathroom strange element | ✅ Fixed | Removed iron_box drawing code |
| 1988 TV checkerboard pattern | ✅ Fixed | Extended rendering to TV state |
| Cartridge text blocking calendar | ✅ Fixed | Text always displays above |
| Cartridge instant game launch | ✅ Fixed | Changed to pickup → inventory flow |
| Tetris hard to trigger | ✅ Fixed | Uses TV's proven collision rect |

---

## Game Flow: Getting Tetris Cartridge

### On 8/8 Date (Any Year)

```
Step 1: Find Cartridge
├─ Cartridge appears on desk
├─ "Cartridge" text shows above
└─ (Only visible on 8/8)

Step 2: Pick Up Cartridge
├─ Approach desk area
├─ Press SPACE → adds to inventory
├─ Message: "Got Tetris Cartridge from the desk!"
└─ tetris_cart_spawned = false

Step 3: Take to Computer
├─ Go to bedroom
├─ Approach computer
├─ (Computer available any year)

Step 4: Launch Game
├─ Select Tetris Cartridge from inventory
├─ Press SPACE at computer
└─ Tetris game starts!
```

---

## Technical Details

### Cartridge Behavior Changes
**Before v2.1:**
- Pressing SPACE directly launched Tetris game
- Cartridge not added to inventory first

**After v2.1:**
- Pressing SPACE adds "Tetris Cartridge" to inventory
- Game launches only when:
  - Cartridge selected in inventory
  - Player at computer
  - SPACE pressed

### Background Rendering Fixes
- Removed all semi-transparent overlays blocking game view
- 1988 cabinet now uses `bg_1988_living` instead of fallback
- TV UI renders over proper scene background
- Cabinet UI displays without masking

### Proximity Rect Configuration
```
calendar_proximity_rect: .inflate(5, 110)     # Original size
tv_proximity_rect:       .inflate(5, 100)     # Standard range
tetris_proximity_rect:   tv_proximity_rect    # On 8/8 only
```

---

## Tested Features

✅ **1988 Year**
- [x] Cabinet opens without overlay artifacts
- [x] TV displays proper background (no checkerboard)
- [x] Bathroom shows clean background
- [x] Tetris cartridge pickup on 8/8
- [x] Cartridge text position correct

✅ **2026 Year**
- [x] Cabinet shows proper background
- [x] TV displays with game scene visible
- [x] Calendar triggers normally
- [x] Computer shows cartridge if selected
- [x] All UI elements render cleanly

✅ **Tetris System**
- [x] Appears on 8/8
- [x] Cartridge text shows above
- [x] Pickup adds to inventory
- [x] Computer can launch if selected
- [x] TV rect detection works reliably

---

## File Changes

| File | Changes | Impact |
|------|---------|--------|
| retro_game.py | ~20 lines modified | Core game logic fixes |
| No other files | — | Asset structure unchanged |

**Key Modifications:**
- `_draw_label()`: Cartridge always displays above
- `render_1988_scene()`: Removed bathroom iron box code
- Cabinet UI: Uses year-specific backgrounds
- TV rect condition: `tetris_proximity_rect` on 8/8
- Cartridge trigger: Pickup only, not game launch

---

## Installation

### Using Executable (Recommended)
1. Download `Retro_2D_Game.exe` (3.61 MB)
2. Create `picture/` folder in same directory
3. Place all game assets in `picture/`
4. Run `Retro_2D_Game.exe`

### From Source
1. Clone repository
2. Install dependencies: `pip install pygame`
3. Run: `python retro_game.py`

---

## Release Notes

- **Build Time:** ~90 seconds
- **Executable Size:** 3.61 MB (optimized)
- **Dependencies:** Bundled (Pygame, NumPy)
- **Platform:** Windows 64-bit
- **Python Base:** 3.8.8 (bundled)

---

## Known Limitations

- Tetris cartridge only available on 8/8
- Computer required to play Tetris (by design)
- Calendar and Tetris share same rect area (mutually exclusive)

---

## What's Coming

**Potential Future Enhancements:**
- Animated TV static effect
- More interactive 1988 elements
- Extended Tetris game features
- Sound effects system

---

## Compatibility

✅ **Backwards Compatible**
- Save data compatible with v2.0
- All previous features preserved
- No breaking changes

---

**Version 2.1 - Polish & Refinement Complete ✅**

*A retro game journey through 1988 and 2026, now with improved gameplay flow and visual clarity.*

---

### Build Information
- **Version:** 2.1
- **Release Date:** 2026-06-15
- **Status:** Stable
- **Tested Platform:** Windows 11 Home
- **Build Tool:** PyInstaller 6.20.0

Ready for release! 🎮
