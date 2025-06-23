import pygame
import os
import json 

os.chdir(os.path.dirname(__file__))

# Asset directories
ASSET_DIR = 'assets'
AUDIO_DIR = os.path.join(ASSET_DIR, 'audio')
SPRITE_DIR = os.path.join(ASSET_DIR, 'sprites')
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Define asset paths
CLASSIC_DAY_BASE = pygame.image.load(os.path.join(SPRITE_DIR, 'classic-day-base.png')).convert()
CLASSIC_DAY_PIPE = pygame.image.load(os.path.join(SPRITE_DIR, 'classic-day-pipe.png')).convert()
CLASSIC_NIGHT_BASE = pygame.image.load(os.path.join(SPRITE_DIR, 'classic-day-base.png')).convert()
CLASSIC_NIGHT_PIPE = pygame.image.load(os.path.join(SPRITE_DIR, 'classic-night-pipe.png')).convert()

# Background paths
CLASSIC_DAY_BACKGROUND_PATH = pygame.image.load(os.path.join(SPRITE_DIR, 'classic-day.png')).convert()
CLASSIC_NIGHT_BACKGROUND_PATH = pygame.image.load(os.path.join(SPRITE_DIR, 'classic-night.png')).convert()

# Scaling the images
CLASSIC_DAY_BACKGROUND_PATH = pygame.transform.scale(CLASSIC_DAY_BACKGROUND_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))
CLASSIC_NIGHT_BACKGROUND_PATH = pygame.transform.scale(CLASSIC_NIGHT_BACKGROUND_PATH, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Standalone Map Selection")

BUTTON_COLOR = (200, 200, 200)  # Gray for map placeholders
HOME_BUTTON = pygame.image.load(os.path.join(SPRITE_DIR, 'home.png')).convert_alpha()
HOME_BUTTON_RECT = pygame.Rect(5, 5, 55, 55)
HOME_BUTTON = pygame.transform.scale(HOME_BUTTON, (HOME_BUTTON_RECT.width, HOME_BUTTON_RECT.height))
BACKGROUND = pygame.image.load(os.path.join(SPRITE_DIR, 'classic-day.png')).convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
FONT_PATH = os.path.join(SPRITE_DIR, 'retro.ttf')

# Button dimensions and layout
MAP_BUTTON_WIDTH = 135
MAP_BUTTON_HEIGHT = 180
MAP_BUTTON_GAP = 40

# Define colors for map borders
INITIAL_BORDER_COLOR = (255, 255, 255)  # Light blue for initial border
HOVER_BORDER_COLOR = (100, 200, 100)    # Green for hover
SELECTED_BORDER_COLOR = (255, 215, 0)   # Gold for selected map

# Initialize border colors and selection state for each map
map_border_colors = {i: INITIAL_BORDER_COLOR for i in range(1, 8)}
selected_map_id = None

# Placeholder paths for assets
map_assets = {
    1: {"base": CLASSIC_DAY_BASE, "pipe": CLASSIC_DAY_PIPE, "background": CLASSIC_DAY_BACKGROUND_PATH},
    2: {"base": CLASSIC_NIGHT_BASE, "pipe": CLASSIC_NIGHT_PIPE, "background": CLASSIC_NIGHT_BACKGROUND_PATH},
}

def load_image(path, size=None):
    return pygame.transform.scale(path, size)

# Define map names
map_names = {
    1: "Classic Day",
    2: "Classic Night",
}
  
def save_selected_map_path(map_id):
    """Saves the selected map's asset paths and scaling information to a JSON file."""
    selected_map = map_assets[map_id]
    data = {
        "map_id": map_id,
        "name": map_names[map_id],
        "assets": {
            "base": f"{map_names[map_id].lower().replace(' ', '-')}-base.png",
            "pipe": f"{map_names[map_id].lower().replace(' ', '-')}-pipe.png",
            "background": f"{map_names[map_id].lower().replace(' ', '-')}.png"
        },
        # Scaling dimensions for each background
        "scaling" : {
            1: (SCREEN_WIDTH, SCREEN_HEIGHT),  # Classic Day
            2: (SCREEN_WIDTH, SCREEN_HEIGHT),  # Classic Night
        }[map_id]
    }
    
    with open("selected_map.json", "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"Map {map_id} paths saved to selected_map.json.")



def load_selected_map_path():
    """Loads the selected map's asset paths and scaling information from a JSON file."""
    with open("selected_map.json", "r") as file:
        data = json.load(file)
        print(f"Loaded map ID: {data['map_id']}, Name: {data['name']}")
        print("Assets:", data['assets'])
        print("Scaling:", data['scaling'])

# Example usage
save_selected_map_path(1)  # Save selected map details
load_selected_map_path()    # Load the details back
def run_map_selection():
    """Standalone map selection screen with actual images for maps."""
    selected_map_name = None
    selected_map_id = None
    selected_map_assets = None
    running = True
    scroll_offset = 0
    scroll_speed = 50
    key_pressed = None
    long_press_timer = 0
    long_press_delay = 300
    long_press_increment = 10

    map_images = {}
    for i in range(1, 3):
        base_path = map_assets[i]["background"]
        map_images[i] = load_image(base_path, (MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT))

    max_scroll_offset = (MAP_BUTTON_HEIGHT + MAP_BUTTON_GAP) * (7 // 2)
    font = pygame.font.Font(None, 24)

    while running:
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(HOME_BUTTON, HOME_BUTTON_RECT)

        if selected_map_name:
            selected_text = font.render(f"Selected: {selected_map_name}", True, (255, 255, 255))
            screen.blit(selected_text, (HOME_BUTTON_RECT.right + 10, HOME_BUTTON_RECT.y))

        if HOME_BUTTON_RECT.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            print("Home button clicked. Exiting map selection...")
            return selected_map_assets  # Return the selected map assets or None if no map selected

        for i in range(2):
            row = i // 2
            col = i % 2
            map_id = i + 1

            x = 60 + (col * (MAP_BUTTON_WIDTH + MAP_BUTTON_GAP))
            y = 100 + (row * (MAP_BUTTON_HEIGHT + MAP_BUTTON_GAP)) - scroll_offset

            map_rect = pygame.Rect(x, y, MAP_BUTTON_WIDTH, MAP_BUTTON_HEIGHT)

            if map_id == selected_map_id:
                border_color = SELECTED_BORDER_COLOR
            elif map_rect.collidepoint(pygame.mouse.get_pos()):
                border_color = HOVER_BORDER_COLOR
            else:
                border_color = map_border_colors[map_id]

            border_rect = map_rect.inflate(10, 10)
            pygame.draw.rect(screen, border_color, border_rect, 3, border_radius=5)

            if map_images[map_id]:
                screen.blit(map_images[map_id], (x, y))
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, map_rect)

            map_name = map_names[map_id]
            text_surface = font.render(map_name, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(x + MAP_BUTTON_WIDTH // 2, y + MAP_BUTTON_HEIGHT + 15))
            screen.blit(text_surface, text_rect)

            if map_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                selected_map_name = map_names[map_id]
                selected_map_id = map_id
                selected_map_assets = map_assets[map_id]
                save_selected_map_path(selected_map_id)  # Save the selected map details to a text file
                print(f"Map {selected_map_id} selected: {selected_map_name}")

        if key_pressed == pygame.K_UP:
            scroll_offset = max(0, scroll_offset - scroll_speed)
        elif key_pressed == pygame.K_DOWN:
            scroll_offset = min(max_scroll_offset, scroll_offset + scroll_speed)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key_pressed = pygame.K_UP
                    long_press_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_DOWN:
                    key_pressed = pygame.K_DOWN
                    long_press_timer = pygame.time.get_ticks()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    key_pressed = None

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    scroll_offset = max(0, scroll_offset - scroll_speed)
                elif event.y < 0:
                    scroll_offset = min(max_scroll_offset, scroll_offset + scroll_speed)

        if key_pressed is not None:
            current_time = pygame.time.get_ticks()
            if current_time - long_press_timer > long_press_delay:
                if current_time % 100 < long_press_increment:
                    if key_pressed == pygame.K_UP:
                        scroll_offset = max(0, scroll_offset - scroll_speed)
                    elif key_pressed == pygame.K_DOWN:
                        scroll_offset = min(max_scroll_offset, scroll_offset + scroll_speed)

    pygame.quit()
    print("Exited map selection screen.")
    return selected_map_assets  # If no map is selected, this will return None

if __name__ == "__main__":
    selected_assets = run_map_selection()
    if selected_assets:
        print("Selected Map Assets:", selected_assets)
    else:
        print("No map selected. Returning to main menu.")
