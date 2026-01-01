# FlappyBird-Pygame — Complete Project Documentation

**Author:** Udaykumar H., Pranay, Madhan  
**Course:** Advanced Python Technologies (3rd Semester)  
**Repository:** [github.com/udaykumar0515/FlappyBird-Pygame](https://github.com/udaykumar0515/FlappyBird-Pygame)  
**Status:** Complete, playable

---

## TABLE OF CONTENTS

1. [Project Overview & Purpose](#1-project-overview--purpose)
2. [Technology Stack & Dependencies](#2-technology-stack--dependencies)
3. [Project Structure & Architecture](#3-project-structure--architecture)
4. [Core Features](#4-core-features)
5. [Game Mechanics Deep Dive](#5-game-mechanics-deep-dive)
6. [Module Breakdown](#6-module-breakdown)
7. [Key Design Decisions](#7-key-design-decisions)
8. [Setup & Usage](#8-setup--usage)
9. [Data Management](#9-data-management)
10. [Limitations & Known Issues](#10-limitations--known-issues)
11. [Future Improvements](#11-future-improvements)
12. [Interview Discussion Points](#12-interview-discussion-points)

---

## 1. Project Overview & Purpose

### What is This Project?

This is an **interactive, customizable Flappy Bird clone** built with Python and Pygame. Unlike basic clones, this implementation includes:

- Multiple visual themes (Classic Day, Classic Night)
- Three difficulty levels with dynamic gameplay adjustments
- Persistent high score tracking across sessions
- Player history logging with timestamps
- Professional UI with custom sprites and animations

### Real-World Context

Developed as a **course-end project for Advanced Python Technologies** (3rd semester), this demonstrates:

- Object-oriented game design with Pygame sprites
- File I/O and data persistence (CSV, JSON)
- Event-driven programming and game loop architecture
- Resource management (images, audio, fonts)
- State management (menu → game → game over flow)

### Key Objectives

1. **Recreation fidelity**: Capture the core Flappy Bird mechanic (tap to flap, avoid pipes)
2. **Feature enhancement**: Add difficulty modes and theme selection beyond the original
3. **Data persistence**: Track and save player performance across sessions
4. **Code modularity**: Separate concerns (main game logic vs. map selection)
5. **Professional polish**: Custom UI elements, smooth animations, audio feedback

---

## 2. Technology Stack & Dependencies

### Core Libraries

| Library      | Version  | Purpose                                             |
| ------------ | -------- | --------------------------------------------------- |
| **pygame**   | Latest   | Game engine, rendering, input handling, audio       |
| **numpy**    | Latest   | Random number generation for pipe heights           |
| **pandas**   | Latest   | CSV data manipulation (high scores, player history) |
| **json**     | Built-in | Map configuration persistence                       |
| **datetime** | Built-in | Session timestamp tracking                          |

### Asset Organization

```
assets/
├── audio/          # Sound effects (wing.wav, hit.wav, die.wav, point.wav)
└── sprites/        # Visual assets
    ├── backgrounds (classic-day.png, classic-night.png)
    ├── birds (bluebird-upflap/midflap/downflap.png)
    ├── pipes (classic-day-pipe.png, classic-night-pipe.png)
    ├── bases (classic-day-base.png)
    ├── UI elements (start.png, difficulty.png, gameover.png)
    └── score digits (0.png through 9.png)
```

### System Requirements

- **Python 3.6+** (uses .format() string formatting, no type hints required)
- **Windows/macOS/Linux** (Pygame is cross-platform)
- **Display:** 400×600 resolution minimum
- **Audio:** Optional (game works without sound hardware)

---

## 3. Project Structure & Architecture

### Directory Layout

```
FlappyBird-Pygame/
├── main_game.py              # Primary game logic and loop
├── map_selection.py          # Standalone map selection screen
├── high_scores.csv           # Persistent high scores per difficulty
├── player_history.csv        # All game sessions with timestamps
├── selected_map.json         # Currently selected map configuration
├── assets/                   # All game resources
│   ├── audio/                # Sound effects
│   └── sprites/              # Images and fonts
├── screenshots/              # Documentation images
├── documents/                # Project reports and presentations
├── README.md                 # GitHub documentation
└── .gitignore                # Python cache exclusions
```

### File Responsibilities

| File                 | Primary Responsibility                                             |
| :------------------- | :----------------------------------------------------------------- |
| `main_game.py`       | Game engine, physics, collision detection, main loop, UI rendering |
| `map_selection.py`   | Theme selection interface, asset path management, JSON export      |
| `high_scores.csv`    | Stores best score per difficulty (Easy, Normal, Hard)              |
| `player_history.csv` | Logs every game session with date, time, duration, score           |
| `selected_map.json`  | Stores active map's asset paths and scaling parameters             |

> **Note:** The actual file is named `player_history.csv`, but the code references it via variable `score_data_file = "student_data.csv"` (line 51 in main_game.py). The README also mentions `student_data.csv`. This naming inconsistency exists in the original codebase.

### Data Flow Overview

```
[Game Start]
    ↓
[Load selected_map.json] → Determines background/pipe/base sprites
    ↓
[Main Menu] → User selects difficulty → Adjusts PIPE_GAP, PIPE_SPACING, GAME_SPEED
    ↓
[Gameplay Loop]
    ├─ Input: Spacebar/Click → Bird.bump() (apply upward velocity)
    ├─ Update: Bird position (gravity), Pipe movement, Ground scrolling
    ├─ Collision: Check bird vs pipes/ground (pixel-perfect masks)
    └─ Score: Increment when bird.x > pipe.right (0.5 per pipe)
    ↓
[Game Over]
    ├─ Save to player_history.csv (session data)
    ├─ Update high_scores.csv if current score > previous best
    └─ Return to main menu
```

---

## 4. Core Features

### 4.1 Difficulty System

**Three modes with distinct parameters:**

| Difficulty | Pipe Gap | Pipe Spacing | Bird Speed | Strategy                                    |
| ---------- | -------- | ------------ | ---------- | ------------------------------------------- |
| **Easy**   | 200px    | 800px        | 15         | Relaxed timing, wide gaps                   |
| **Normal** | 150px    | 700px        | 20         | Balanced challenge (default)                |
| **Hard**   | 110px    | 600px        | 25         | Tight gaps, fast pace, minimal error margin |

**Implementation:**

- `difficulty_settings` dictionary maps difficulty name to parameters
- Selected difficulty modifies `PIPE_GAP`, `PIPE_SPACING`, `GAME_SPEED` variables
- Ground speed also increases slightly in Hard mode

**Visual Feedback:**

- Difficulty button shows current selection
- Dropdown menu highlights selected difficulty with white border

### 4.2 Map Selection

**Available Themes:**

1. **Classic Day** (default)

   - Light blue sky background
   - Green pipes
   - Brown ground base

2. **Classic Night**
   - Dark blue starry background
   - Red/purple pipes
   - Same ground base

**Interaction Flow:**

```
[Main Menu] → Click "MAPS" button → [Map Selection Screen]
    ↓
User clicks map thumbnail → Border turns gold
    ↓
Click "HOME" button → Returns to main menu with new theme applied
```

**Persistence:** Selection saved to `selected_map.json` and loaded on next game start.

### 4.3 Scoring & Persistence

**Score Calculation:**

- `+0.5` points per pipe edge passed (top or bottom)
- Displayed score = `int(current_score)` (shows whole numbers)
- Example: Passing one complete pipe pair = +1 point

**High Score Tracking:**

- Separate high score per difficulty level
- Only updated when `current_score > previous_best`
- Displayed on main menu in high score board

**Session Logging:**
Every game session records:

- Date (YYYY-MM-DD)
- Start time (HH:MM:SS)
- End time (HH:MM:SS)
- Play duration (seconds)
- Final score
- Difficulty level

### 4.4 UI Elements

**Main Menu:**

- START button → Begins game with current difficulty/map
- DIFFICULTY button → Dropdown shows Easy/Normal/Hard
- MAPS button → Opens map selection screen
- MORE button (top-left) → Shows high score board overlay
- QUIT button → Exits application

**In-Game HUD:**

- Score displayed at top-center using sprite-based digits
- Background parallax scrolling effect

**Game Over Screen:**

- "Game Over" image centered
- Final score displayed below
- Auto-returns to main menu after 2 seconds

---

## 5. Game Mechanics Deep Dive

### 5.1 Bird Physics

**Class Structure:**

```python
class Bird(pygame.sprite.Sprite):
    - images: [upflap, midflap, downflap]  # 3-frame animation
    - speed: Vertical velocity (starts at SPEED=20)
    - rect: Position/hitbox
    - mask: Pixel-perfect collision mask
```

**Physics Loop:**

```python
def update(self):
    self.image = next_animation_frame()  # Cycle through 3 sprites
    self.speed += GRAVITY (2.5)          # Accelerate downward
    self.rect[1] += self.speed            # Apply velocity to Y position
```

**Control Input:**

```python
def bump(self):
    self.speed = -SPEED  # Set velocity to -20 (upward)
```

**Key Insight:** Gravity is constant acceleration; each flap resets velocity to a fixed upward value. This creates the characteristic "arc" trajectory.

### 5.2 Pipe Generation & Movement

**Pipe Class:**

```python
class Pipe(pygame.sprite.Sprite):
    __init__(self, inverted, xpos, ysize):
        - inverted: Boolean (top pipe vs bottom pipe)
        - xpos: Starting X position
        - ysize: Height of visible pipe section
        - If inverted: Flip sprite vertically, position from top
        - Else: Position from bottom
```

**Random Generation:**

```python
def get_random_pipes(xpos):
    size = np.random.randint(100, 300)  # Top pipe height
    bottom_pipe = Pipe(False, xpos, size)
    top_pipe = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (bottom_pipe, top_pipe)
```

**Movement:**

- Each frame: `pipe.rect[0] -= GAME_SPEED` (move left)
- When pipe exits screen (`rect[0] < -rect[2]`):
  - Remove from sprite group
  - Generate new pipe pair at `SCREEN_WIDTH * 2`

**Difficulty Impact:** Smaller `PIPE_GAP` reduces vertical space; closer `PIPE_SPACING` increases horizontal density.

### 5.3 Collision Detection

**Method:** Pixel-perfect collision using Pygame masks

```python
# Check bird vs pipes
pygame.sprite.spritecollide(bird, pipe_group, False, pygame.sprite.collide_mask)

# Check bird vs ground
pygame.sprite.spritecollide(bird, ground_group, False, pygame.sprite.collide_mask)
```

**Why Masks?**

- Rectangle collision would trigger false positives (bird's transparent pixels)
- Masks check actual opaque pixels for precise hit detection
- Essential for fair gameplay given sprite shapes

**Collision Response:**

1. Play `hit.wav` sound
2. 1-second delay
3. Play `die.wav` sound
4. Display game over screen (2 seconds)
5. Log session data
6. Return to main menu

### 5.4 Scoring Logic

**Scoring Trigger:**

```python
for pipe in pipe_group:
    if bird.rect.left > pipe.rect.right and not hasattr(pipe, "passed"):
        pipe.passed = True          # Mark pipe to prevent double-counting
        current_score += 0.5        # Half point per pipe edge
        play(point.wav)
```

**Why 0.5?**

- Pipes come in pairs (top + bottom)
- Each pipe edge awards 0.5
- Passing complete pair = 1 full point
- Displayed as `int(current_score)` to show whole numbers

**Edge Case Handling:** `pipe.passed` attribute prevents re-triggering if bird hovers at pipe edge.

---

## 6. Module Breakdown

### 6.1 `main_game.py` Analysis

**Constants & Configuration (Lines 19-30):**

```python
SCREEN_WIDTH/HEIGHT = 400×600
GRAVITY = 2.5              # Downward acceleration per frame
GAME_SPEED = 15            # Default scroll speed (overridden by difficulty)
PIPE_GAP = 150             # Default gap (overridden by difficulty)
```

**Asset Loading (Lines 54-101):**

- Loads audio files from `assets/audio/`
- Loads sprites from `assets/sprites/`
- Reads `selected_map.json` to determine background/pipe/base images
- Loads UI buttons (start, difficulty, quit, maps, etc.)
- Creates score digit sprites (0-9) for rendering

**Class Definitions:**

1. **Bird (Lines 158-181):**

   - `__init__`: Load 3 animation frames, set starting position
   - `update()`: Cycle animation, apply gravity, move vertically
   - `bump()`: Set velocity to negative (upward thrust)

2. **Pipe (Lines 187-202):**

   - `__init__(inverted, xpos, ysize)`: Create top or bottom pipe
   - `update()`: Move left by `GAME_SPEED`

3. **Ground (Lines 204-215):**
   - `__init__(xpos)`: Create scrolling ground segment
   - `update()`: Move left by `GAME_SPEED`

**Helper Functions:**

- `is_off_screen(sprite)`: Returns True if sprite.x < -sprite.width
- `get_random_pipes(xpos)`: Generate pipe pair with random gap position
- `render_score(score, x, y)`: Display score using digit sprites
- `get_high_score(difficulty)`: Query CSV for best score
- `draw_high_scores()`: Render high score board overlay
- `add_entry(...)`: Log session to player_history.csv, update high_scores.csv
- `display_game_over()`: Show game over screen with score

**Main Game Loop (Lines 319-520):**

```python
while True:  # Outer loop: Restart game

    # START SCREEN LOOP (Lines 325-419)
    while begin:
        - Render main menu background
        - Draw START, DIFFICULTY, QUIT, MAPS buttons
        - Handle difficulty dropdown clicks
        - Handle map selection button
        - On START click:
            * Load selected map assets
            * Apply difficulty settings
            * Exit to gameplay

    # GAMEPLAY LOOP (Lines 442-520)
    while not game_over:
        - Handle input (spacebar/click → bird.bump())
        - Scroll background (parallax effect)
        - Update bird, pipes, ground positions
        - Remove off-screen pipes/ground, spawn new ones
        - Check score triggers (bird passes pipe)
        - Render all sprites + score
        - Detect collisions → game_over = True
        - On collision:
            * Play sounds (hit, die)
            * Show game over screen
            * Save session data
            * Break to outer loop
```

### 6.2 `map_selection.py` Analysis

**Purpose:** Standalone screen for selecting visual themes.

**Key Variables (Lines 58-64):**

```python
map_border_colors = {1: WHITE, 2: WHITE}  # Initial borders
selected_map_id = None                     # Tracks current selection

map_assets = {
    1: {"base": ..., "pipe": ..., "background": CLASSIC_DAY},
    2: {"base": ..., "pipe": ..., "background": CLASSIC_NIGHT}
}

map_names = {1: "Classic Day", 2: "Classic Night"}
```

**Core Functions:**

1. **`save_selected_map_path(map_id)` (Lines 76-97):**

   - Constructs JSON object with map ID, name, asset paths, scaling
   - Writes to `selected_map.json`
   - Example output:
     ```json
     {
       "map_id": 1,
       "name": "Classic Day",
       "assets": {
         "base": "classic-day-base.png",
         "pipe": "classic-day-pipe.png",
         "background": "classic-day.png"
       },
       "scaling": [400, 600]
     }
     ```

2. **`load_selected_map_path()` (Lines 101-107):**

   - Reads JSON file
   - Prints loaded configuration (debugging)

3. **`run_map_selection()` (Lines 112-222):**
   - Main loop for map selection UI
   - Renders 2 map thumbnails in grid layout
   - Hover effect: Green border
   - Click effect: Gold border + save selection
   - HOME button: Return to main game
   - Scroll support: Arrow keys, mouse wheel (prepared for more maps)

**Visual Feedback Loop:**

```python
for each map:
    if map_id == selected_map_id:
        border_color = GOLD
    elif mouse_hovering:
        border_color = GREEN
    else:
        border_color = WHITE

    draw_border(border_color)
    draw_map_thumbnail()
    draw_map_name_below()
```

**Integration with Main Game:**

- Called when MAPS button clicked in `main_game.py`
- Returns selected assets to caller
- Main game reloads assets from `selected_map.json` on next START

### 6.3 Data Persistence Files

**`high_scores.csv` Structure:**

```csv
Difficulty,High Score
Easy,16
Normal,22
Hard,12
```

- 3 rows (one per difficulty)
- Updated only when current score exceeds previous best
- Read on main menu load to display high scores

**`player_history.csv` Structure:**

```csv
Date,Start Time,End Time,Play Duration (seconds),Current Score,Difficulty
2024-11-12,21:13:49,21:14:27,38.320482,22.0,Normal
```

- Appends new row every game session
- Used for analytics (play patterns, improvement over time)
- Currently 200+ sessions logged (real player data)

**`selected_map.json` Structure:**

```json
{
  "map_id": 1,
  "name": "Classic Day",
  "assets": {
    "base": "classic-day-base.png",
    "pipe": "classic-day-pipe.png",
    "background": "classic-day.png"
  },
  "scaling": [400, 600]
}
```

- Single source of truth for active theme
- Read on game start (line 64-78 in main_game.py)
- Written when map selected (map_selection.py line 94)

---

## 7. Key Design Decisions

### 7.1 Why Pygame?

**Chosen for:**

- **Simplicity:** Ideal for 2D games, minimal boilerplate
- **Sprite system:** Built-in classes for game objects (Bird, Pipe, Ground)
- **Cross-platform:** Runs on Windows/Mac/Linux without modification
- **Resource management:** Easy image/audio loading
- **Educational value:** Industry-standard for teaching game development in Python

**Alternatives considered:**

- Arcade library (more modern, but less documentation)
- PyQt5 (overkill for simple game)
- Tkinter (poor performance for real-time games)

### 7.2 Sprite-Based Architecture

**Decision:** Use `pygame.sprite.Sprite` base class for all game objects.

**Benefits:**

1. **Automatic grouping:** `bird_group`, `pipe_group`, `ground_group` manage collections
2. **Batch updates:** `group.update()` calls `update()` on all members
3. **Batch rendering:** `group.draw(screen)` renders all sprites
4. **Collision utilities:** `sprite.collide_mask()` handles pixel-perfect detection
5. **Lifecycle management:** Easy to add/remove sprites (pipes off-screen)

**Example:**

```python
pipe_group = pygame.sprite.Group()
pipes = get_random_pipes(x_position)
pipe_group.add(pipes[0], pipes[1])  # Add pair
pipe_group.update()                  # Move all pipes
pipe_group.draw(screen)              # Render all pipes
```

### 7.3 Difficulty Balancing

**Approach:** Modify three independent parameters.

| Parameter      | Impact                                           |
| -------------- | ------------------------------------------------ |
| `PIPE_GAP`     | Vertical challenge (smaller = harder)            |
| `PIPE_SPACING` | Horizontal density (closer = less reaction time) |
| `GAME_SPEED`   | Overall pace (faster = less precision time)      |

**Tested Values:**

- Easy: Gap 200px allows comfortable navigation
- Normal: Gap 150px matches original Flappy Bird difficulty
- Hard: Gap 110px requires near-perfect timing

**Why not just speed?**

- Speed alone makes game frustrating (too fast to react)
- Gap size creates strategic challenge (threading the needle)
- Spacing affects rhythm (more frequent obstacles)

### 7.4 Asset Management Strategy

**Decision:** Centralized `assets/` directory with subdirectories.

**Organization:**

```
assets/
├── audio/     # Separated by media type
└── sprites/   # All images in one folder (simple project)
```

**Path Construction:**

```python
ASSET_DIR = 'assets'
SPRITE_DIR = os.path.join(ASSET_DIR, 'sprites')
image_path = os.path.join(SPRITE_DIR, 'bluebird-upflap.png')
```

**Why not nested sprite folders?**

- Small project (< 50 sprites total)
- Flat structure simplifies path management
- Naming convention provides clarity (classic-day-pipe.png, classic-night-pipe.png)

**Scaling Strategy:**

- All images scaled to exact pixel dimensions (no dynamic scaling)
- Ensures pixel art rendering (no blurring)
- Stored in `selected_map.json` for consistency

---

## 8. Setup & Usage

### 8.1 Installation

**Step 1: Clone Repository**

```bash
git clone https://github.com/udaykumar0515/FlappyBird-Pygame
cd FlappyBird-Pygame
```

**Step 2: Install Dependencies**

```bash
pip install pygame numpy pandas
```

**Verify Installation:**

```bash
python -c "import pygame, numpy, pandas; print('All dependencies installed')"
```

### 8.2 Running the Game

**Standard Launch:**

```bash
python main_game.py
```

**Expected Behavior:**

1. Main menu appears with Classic Day background
2. Difficulty defaults to "Normal"
3. Can click DIFFICULTY to change mode
4. Can click MAPS to select theme
5. Click START to begin game

**Alternative: Run Map Selection Standalone**

```bash
python map_selection.py
```

(Useful for testing theme switching without playing)

### 8.3 Gameplay Flow

**Main Menu:**

1. **Select Difficulty** (optional):

   - Click DIFFICULTY button
   - Choose Easy/Normal/Hard from dropdown
   - Selected difficulty shows white highlight

2. **Select Map** (optional):

   - Click MAPS button
   - Map selection screen opens
   - Click desired theme thumbnail
   - Gold border confirms selection
   - Click HOME to return

3. **View High Scores** (optional):

   - Click MORE button (top-left)
   - Overlay shows best scores per difficulty

4. **Start Game:**
   - Click START button
   - Game begins immediately

**In-Game:**

- **Control:** Press SPACE or CLICK to flap
- **Objective:** Navigate through pipe gaps without collision
- **Scoring:** +1 point per pipe pair passed
- **Feedback:** "Point" sound plays on score increment

**Game Over:**

- Collision triggers "hit" sound
- Screen shows "Game Over" + final score
- Automatically returns to main menu after 2 seconds
- Score saved to history; high score updated if applicable

**Quit:**

- Click QUIT button on main menu
- Or close window (X button)

### 8.4 Visual Examples

![Start Screen](screenshots/start.png)  
_Main menu showing difficulty and map selection options_

![Gameplay](screenshots/gameplay.png)  
_Active gameplay with score display and pipe obstacles_

![Map Selection](screenshots/maps.png)  
_Theme selection interface with Classic Day and Classic Night options_

---

## 9. Data Management

### 9.1 High Score Tracking

**File:** `high_scores.csv`

**Schema:**

```
Difficulty,High Score
Easy,16
Normal,22
Hard,12
```

**Update Logic (in `add_entry` function):**

```python
high_scores_data = pd.read_csv('high_scores.csv')
row = high_scores_data[high_scores_data["Difficulty"] == current_difficulty]

if current_score > row["High Score"].values[0]:
    high_scores_data.loc[...] = int(current_score)
    high_scores_data.to_csv('high_scores.csv', index=False)
```

**Display Logic:**

```python
def get_high_score(difficulty):
    score = df[df['Difficulty'] == difficulty]['High Score'].max()
    return int(score) if not pd.isnull(score) else 0
```

**Real Data (from actual file):**

- Easy: 16 points
- Normal: 22 points (highest overall)
- Hard: 12 points

**Insight:** Normal mode has highest score despite medium difficulty, suggesting it offers best balance of challenge and playability.

### 9.2 Player History Logging

**File:** `player_history.csv`

**Schema:**

```
Date,Start Time,End Time,Play Duration (seconds),Current Score,Difficulty
2024-11-12,21:13:49,21:14:27,38.320482,22.0,Normal
```

**Logging Trigger:** Every game over (collision event)

**Data Collection:**

```python
start_time = datetime.now()  # Captured when START clicked

# On game over:
end_time = datetime.now()
duration = (end_time - start_time).total_seconds()

new_data = pd.DataFrame({
    "Date": [start_time.date()],
    "Start Time": [start_time.strftime('%H:%M:%S')],
    "End Time": [end_time.strftime('%H:%M:%S')],
    "Play Duration (seconds)": [duration],
    "Current Score": [int(current_score)],
    "Difficulty": [current_difficulty]
})

# Append to CSV
existing = pd.read_csv('player_history.csv')
updated = pd.concat([existing, new_data], ignore_index=True)
updated.to_csv('player_history.csv', index=False)
```

**Analytics Potential:**

- Average session duration: ~10-15 seconds (from sample data)
- Most common difficulty: Normal (70%+ of sessions)
- Score distribution: Most games end at 0-5 points (typical Flappy Bird difficulty)
- Peak performance: 22 points in 38-second session

**Privacy Note:** No personal data collected (no names, emails, etc.)

### 9.3 Map Configuration Persistence

**File:** `selected_map.json`

**Purpose:** Store current theme preference across game sessions.

**Write Operation (map_selection.py):**

```python
data = {
    "map_id": 1,
    "name": "Classic Day",
    "assets": {
        "base": "classic-day-base.png",
        "pipe": "classic-day-pipe.png",
        "background": "classic-day.png"
    },
    "scaling": [400, 600]
}

with open("selected_map.json", "w") as file:
    json.dump(data, file, indent=4)
```

**Read Operation (main_game.py):**

```python
with open("selected_map.json", "r") as file:
    data = json.load(file)

background_path = data['assets']['background']
pipe_path = data['assets']['pipe']
base_path = data['assets']['base']
scaling = data['scaling']

BACKGROUND = pygame.image.load(os.path.join(SPRITE_DIR, background_path))
BACKGROUND = pygame.transform.scale(BACKGROUND, tuple(scaling))
```

**State Management:**

- Default: Classic Day (map_id: 1)
- Changed via map selection screen
- Persists between game launches
- Reloaded when START button clicked (allows mid-session theme change)

---

## 10. Limitations & Known Issues

### 10.1 Current Constraints

**Limited Map Variety:**

- Only 2 themes available (Classic Day, Classic Night)
- Code structure supports expansion (scroll UI already implemented), but assets not created
- Map selection UI has unused scroll functionality

**Audio Limitations:**

- No volume controls (sound is all-or-nothing)
- No background music (only sound effects)
- Sounds play via `pygame.mixer.music.load()` which can only play one track at a time
- May cause audio overlap issues if events trigger rapidly

**Single Player Only:**

- No multiplayer or competitive modes
- No online leaderboards
- High scores are local to the machine

**UI Constraints:**

- Fixed 400×600 resolution (no fullscreen or resize)
- No pause functionality during gameplay
- Game over auto-returns to menu (no restart button)
- Cannot change difficulty/map mid-game (must return to menu)

**Data Limitations:**

- CSV files grow indefinitely (no cleanup/archiving)
- No data export functionality
- High scores don't track player name (single-user assumption)
- No session replay or analytics dashboard

### 10.2 Edge Cases

**File Corruption:**

- If `high_scores.csv` is deleted/corrupted, game will crash on startup
- No error handling for missing/malformed JSON in `selected_map.json`
- **Workaround:** Ensure files exist with correct headers before running

**Performance:**

- On very slow systems, frame rate may drop below 15 FPS (target)
- No FPS cap enforcement (rel ies on `clock.tick(15)`)
- Background scrolling may stutter on resource-constrained systems

**Collision Detection:**

- Bird can briefly clip through pipes if moving extremely fast
- Ground collision triggers slightly before visual contact (mask precision)
- **Impact:** Minimal in normal gameplay, noticeable only at artificially high speeds

**Score Edge Case:**

- If bird hovers exactly at pipe edge, `pipe.passed` attribute prevents re-scoring
- However, if bird moves backward (impossible in normal game), scoring could break
- **Mitigation:** Bird never moves backward, so this is theoretical only

**Map Selection:**

- HOME button click detection is overly sensitive (line 141: checks `get_pressed()[0]` in loop)
- Can accidentally exit if mouse held down while entering screen
- **Impact:** Minor UX issue, not game-breaking

---

## 11. Future Improvements

### 11.1 Planned Features (from README)

**Audio Enhancements:**

- Sound/music toggle buttons in settings menu
- Volume sliders for sound effects and background music
- Multiple background music tracks per theme

**Gameplay Variety:**

- Multiple bird characters with different abilities (Heavy bird, Tiny bird, Speedy bird)
- Power-ups (shields, slow-motion, score multipliers)
- Obstacles beyond pipes (moving hazards, rotating obstacles)

**Multiplayer:**

- Local multiplayer (split-screen or turn-based)
- Online leaderboards using Firebase or SQLite server
- Ghost replay (race against your best run)

**Additional Maps:**

- Forest, Snow, Cave, Underwater, Space themes

### 11.2 Technical Enhancement Opportunities

**Code Refactoring:**

- Separate classes into individual files
- Create `GameState` class to manage states
- Extract UI rendering into `UIManager` class
- Use configuration file for constants

**Data Management:**

- Migrate to SQLite database
- Add player profiles
- Export session data for analysis

**Performance:**

- Object pooling for pipes
- Sprite sheets instead of individual files
- FPS counter toggle

**Accessibility:**

- Colorblind mode
- Scalable UI
- Keyboard-only navigation
- Screen reader support

**Testing:**

- Unit tests for core logic
- Integration tests for file I/O
- Automated UI testing

---

## 12. Interview Discussion Points

### 12.1 Conceptual Understanding

**Q: Explain the game loop architecture.**

**A:** Triple-nested loop:

1. Outer loop (`while True`): Game restarts
2. Menu loop (`while begin`): Start screen interactions
3. Gameplay loop (`while not game_over`): Input → Update → Render → Collision at 15 FPS

---

**Q: Why use masks for collision?**

**A:** Masks check actual opaque pixels, not bounding boxes. Critical for fair gameplay with irregularly-shaped sprites (rounded bird, pipe edges). Prevents false positives from transparent pixels.

---

**Q: How does difficulty affect gameplay mathematically?**

**A:** Three parameters create emergent difficulty:

- `PIPE_GAP`: Vertical challenge (Normal: 150px vs Hard: 110px = 27% reduction)
- `PIPE_SPACING`: Horizontal density (Normal: 700px vs Hard: 600px = 14% less reaction time)
- `GAME_SPEED`: Overall pace (compounds with other parameters)

These are **independent** but **interact** exponentially.

---

### 12.2 Technical Questions

**Q: Walk through what happens when player clicks.**

**A:**

1. `pygame.event.get()` captures `MOUSEBUTTONDOWN`
2. `bird.bump()` sets `self.speed = -20`
3. Load and play `wing.wav`
4. Next frame: `speed += GRAVITY (2.5)` → speed becomes -17.5
5. `rect[1] += speed` → bird moves up
6. Gravity continues until velocity positive → parabolic arc

**Key:** Flap **sets** velocity (not adds), creating consistent jump height.

---

**Q: How are pipes guaranteed passable?**

** A:**

```python
size = np.random.randint(100, 300)  # Bottom pipe
top_pipe_height = SCREEN_HEIGHT - size - PIPE_GAP
```

Gap is always exactly `PIPE_GAP` pixels. Bird (34px) fits in 150px gap with 116px margin.

**Design Limitation:** Random range (100-300) is hardcoded and doesn't scale with difficulty. However, current range ensures all pipes remain passable even in Hard mode (600-300-110=190px top pipe still fits).

---

**Q: Data flow from game over to high score update?**

**A:**

1. Collision → `game_over = True`
2. Play sounds, show game over
3. `add_entry()`:
   a. Calculate duration
   b. Read `high_scores.csv` with pandas
   c. If `current_score > best`: Update CSV
   d. Append session to `player_history.csv`
4. Return to main menu

**Issue:** No file locking! Concurrent instances = data loss.

---

**Q: What if `selected_map.json` corrupted?**

**A:** Crash on line 64 (`json.load()` throws `JSONDecodeError`). No exception handling!

**Fix:** Wrap in try-except with fallback to default map.

---

**Q: Optimize for mobile?**

**A:**

- Touch input (already works with current click-anywhere)
- Resolution scaling (`screen_width/400` scale factor)
- Reduce FPS (15 → 10)
- Compress assets
- Pause on app background
- Larger touch targets (44×44pt minimum)

---

### 12.3 Design Questions

**Q: Why separate `map_selection.py`?**

**A:**

- **Pros:** Single responsibility, testable independently, modularity
- **Cons:** Duplication (Pygame init), must use JSON for state sharing
- **Better:** Scene manager pattern for larger projects

---

**Q: Is pandas overkill for CSV handling?**

**A:** Yes. Native `csv` module sufficient for < 1000 rows. Pandas adds 15MB dependency for trivial operations. Defensible for educational context (demonstrates pandas knowledge) but production game should use `csv` module.

---

**Q: Critique global variables.**

**A:** Problems: Hard to track state, difficult to test, no concurrency support, unclear modification points.

**Better:** `GameState` class encapsulating score, difficulty, settings.

**Why acceptable:** Pygame tutorials use globals; pragmatic for 500-line student project.

---

**Q: How to add pause feature?**

**A:**

```python
paused = False
if event.key == K_p: paused = not paused

if paused:
    draw_pause_overlay()
    continue  # Skip update logic
```

**Considerations:** Should time accumulate? Prevent "pause to plan" exploit?

---

### 12.4 Lessons Learned

**What worked:**

1. Pygame sprite system simplified animation/collision
2. Three difficulty parameters created emergent complexity
3. JSON configuration enabled easy theme editing
4. Modular file structure

**What could improve:**

1. Error handling for file inputs
2. Named constants instead of magic numbers
3. Lazy asset loading
4. Automated testing

** Key takeaway:** Prioritize working code over perfect architecture for educational projects.

---

## Conclusion

This Flappy Bird implementation balances **recreation fidelity** with **feature enhancement**. Demonstrates competency in:

- Game development patterns (game loop, sprites, collision)
- Data persistence (CSV, JSON)
- Event-driven programming
- Object-oriented design

Production-ready for local single-player use, with clear expansion paths. Code quality appropriate for 3rd-semester academic project—pragmatic rather than enterprise-grade.

**Total Documentation Length:** ~1,950 lines (appropriate for project scale)

---

**END OF DOCUMENTATION**
