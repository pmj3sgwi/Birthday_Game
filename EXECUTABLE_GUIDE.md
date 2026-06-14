# Retro 2D Game - Executable Guide

## 🎮 Quick Start

### Download
The standalone executable `Retro_2D_Game.exe` is available in the project directory:
- **Location:** `/dist/Retro_2D_Game/Retro_2D_Game.exe`
- **Size:** 3.61 MB
- **Type:** Fully standalone (no Python installation required)

### Installation (3 steps)

#### Step 1: Extract Files
Extract all files from the distribution package to your desired location.

Required structure:
```
Retro_2D_Game.exe        ← Main executable
picture/                 ← Game assets folder
├── 1988_客廳_T.png
├── 1988_黑白電視_去背.png
├── 1988_黑白電視_提示_去背.png
├── [other image files...]
└── ...
```

#### Step 2: Create Picture Folder
Ensure the `picture/` subfolder exists in the same directory as `Retro_2D_Game.exe`

#### Step 3: Run
Double-click `Retro_2D_Game.exe` to start playing!

---

## 📋 System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Windows 7 | Windows 10+ |
| Architecture | 64-bit | 64-bit |
| RAM | 512 MB | 2 GB+ |
| Disk Space | 4 MB | 10 MB |
| Display | 800×600 | 1920×1080 |
| Audio | Optional | Recommended |

---

## 🎯 Game Features (v2)

### Available in Both 1988 & 2026
- ✅ Living room TV system
- ✅ Cabinet with flashlight and remote control
- ✅ Bedroom with computer and iron cabinet
- ✅ Bathroom with mirror and bathtub
- ✅ Inventory system (10 slots)

### 1988-Specific Features
- 🕯️ Flashlight-based lighting system
- 📺 Black-and-white TV display
- 🔦 Selective item visibility (only with light)
- 🌙 Dark atmosphere mechanics

### 2026-Specific Features
- 💡 Always-lit rooms
- 📺 Color TV with 2 channels
- 🎮 All objects visible
- 🌅 Modern day atmosphere

---

## 🕹️ How to Play

### Starting the Game
1. Run `Retro_2D_Game.exe`
2. Game automatically detects current scenario
3. Use arrow keys to navigate

### Controls

| Input | Action |
|-------|--------|
| Arrow Keys | Move player |
| SPACE | Interact with objects/Confirm selections |
| ESC | Close windows/Return to game |
| Number Keys (1-10) | Select inventory items |
| F1 | Toggle collision/proximity debug view |
| F2 | Debug mode toggle |

### 1988 Scenario Walkthrough

#### Getting Started
1. You start in darkness (pitch black)
2. Objective: Find the flashlight
3. Navigate to the cabinet in the living room
4. Open cabinet drawer (SPACE when nearby)
5. Select flashlight (Number key 1) to activate light

#### Accessing TV
1. With flashlight selected and lights on
2. Approach the TV area
3. "TV" prompt appears
4. Press SPACE to turn on TV
5. Black-and-white static displays
6. Press SPACE or ESC to close

#### Exploration Tips
- Lights turn on automatically when flashlight is selected
- Dark areas are dangerous - always have flashlight ready
- Bedroom is especially dark without light
- Try obtaining the remote control for more TV options

### 2026 Scenario Walkthrough

#### Getting Started
1. You start in a fully lit living room
2. All rooms are well-lit
3. All objects are visible and accessible
4. Explore freely at your pace

#### Accessing TV
1. Approach the TV
2. "TV" prompt appears
3. Press SPACE to turn on
4. Use UP/DOWN arrow keys to switch channels
5. Select remote control for channel control
6. Press SPACE or ESC to close

#### Features
- Pick up remote control for TV interaction
- Explore the bedroom and bathroom
- Interact with computer and other objects
- No lighting limitations

---

## 🎬 In-Game Assets

### Included Image Files
The executable includes all game assets:
- Character sprites (1988 and 2026 variants)
- Room backgrounds
- Furniture and objects
- UI elements
- TV display variants
- Game icons

All images are properly optimized and integrated into the executable.

---

## 🐛 Troubleshooting

### Game Won't Start
**Problem:** "Cannot find picture folder"  
**Solution:** Create empty `picture/` folder in same directory as EXE

### Graphics Issues
**Problem:** Low resolution or pixelated display  
**Solution:** This is intentional! Game runs at 320×240 virtual resolution

### Sound Issues
**Problem:** No audio  
**Solution:** Check system volume; game includes minimal audio

### Performance Issues
**Problem:** Game runs slowly  
**Solution:**
- Close background applications
- Update graphics drivers
- Check disk space (at least 100 MB free)

### Cannot Find TV
**Problem:** TV prompt not appearing  
**Solution:** 
- In 1988: Ensure you have flashlight and it's selected
- In 2026: Just approach the TV area
- Check you're in the living room

---

## 🔍 Advanced Features

### Debug Mode
Press F1 to toggle collision rectangles and proximity areas  
Press F2 for additional debug information

### Inventory System
- 10 available slots
- Each slot displays item image
- Select with number keys 1-10
- Some items affect game mechanics

### State Persistence
Game remembers:
- Collected items
- Opened doors
- TV on/off state
- Current lighting state
- Inventory selections

---

## 📁 File Structure

```
Game Directory/
├── Retro_2D_Game.exe              ← Main executable
├── Retro_2D_Game/                 ← Support libraries
│   ├── pygame/
│   ├── numpy/
│   └── [dependencies...]
├── picture/                       ← Game assets
│   ├── [all image files]
│   └── [subfolders...]
└── [other config files]
```

---

## 🎨 Graphics Settings

| Setting | Value |
|---------|-------|
| Virtual Resolution | 320×240 pixels |
| Window Resolution | 960×760 pixels |
| Scale Factor | 3× (horizontal), 2.917× (vertical) |
| Color Depth | 32-bit RGBA |
| Rendering | Software (Pygame) |

The pixelated/retro appearance is intentional!

---

## 🔄 Updating

When new versions are released:
1. Download the latest `Retro_2D_Game.exe`
2. Replace the old executable
3. Keep the same `picture/` folder
4. No save data migration needed

Saves are fully compatible between v1 and v2+

---

## 📞 Support

### Common Issues
- See Troubleshooting section above
- Check Windows Event Viewer for error codes
- Ensure 64-bit Windows system

### Reporting Bugs
Include:
- Windows version
- What you were doing when it happened
- Screenshot if applicable
- Game version (displayed in window title)

---

## 📊 Version Information

| Property | Value |
|----------|-------|
| Current Version | v2.0 |
| Release Date | 2026-06-15 |
| Build Status | Stable |
| Tested On | Windows 11 Home |
| Python Base | 3.8.8 |
| Pygame Version | 2.6.1 |

---

## ⚖️ License & Credits

- Game Engine: Pygame
- Framework: Python 3.8
- Distribution: PyInstaller
- Assets: Custom created

---

## 🚀 Getting Started Checklist

- [ ] Download `Retro_2D_Game.exe`
- [ ] Extract to desired location
- [ ] Create `picture/` subfolder
- [ ] Place all image files in `picture/`
- [ ] Run `Retro_2D_Game.exe`
- [ ] Enjoy! 🎮

---

**Retro 2D Game v2.0**  
*An adventure through time - 1988 and 2026*

For source code and development info, see the main repository.
