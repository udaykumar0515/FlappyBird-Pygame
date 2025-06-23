import pygame, time, os
from pygame.locals import *
import numpy as np
from datetime import datetime
import pandas as pd
import json
from map_selection import run_map_selection

# Start tracking time   
start_time = datetime.now()
# Set working directory to the script's folder
os.chdir(os.path.dirname(__file__))

# Asset directories
ASSET_DIR = 'assets'
AUDIO_DIR = os.path.join(ASSET_DIR, 'audio')
SPRITE_DIR = os.path.join(ASSET_DIR, 'sprites')

# VARIABLES
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150
GROUND_GAP = -5

# Button variables
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_COLOR = (255, 165, 0)


# Highlight color for selected options
HIGHLIGHT_COLOR = (255, 255, 255)

pipes_passed_count = 0  # Counter for pipes passed
current_score = 0

pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')


#paths for the csv files
score_data_file = os.path.join("student_data.csv")
high_scores_file = os.path.join("high_scores.csv")
 
# Load sounds
wing = os.path.join(AUDIO_DIR, 'wing.wav')
hit = os.path.join(AUDIO_DIR, 'hit.wav')
die = os.path.join(AUDIO_DIR, 'die.wav')
point = os.path.join(AUDIO_DIR, 'point.wav')

#main background
BACKGROUND_MAIN = pygame.image.load(os.path.join(SPRITE_DIR, 'classic-day.png')).convert()
BACKGROUND_MAIN = pygame.transform.scale(BACKGROUND_MAIN, (SCREEN_WIDTH, SCREEN_HEIGHT))

with open("selected_map.json", "r") as file:
    data = json.load(file)

# Extract paths and scaling data
selected_background_path = data['assets']['background']
selected_pipe_path = data['assets']['pipe']
selected_base_path = data['assets']['base']
scaling = data['scaling']

# Load and scale images
global BACKGROUND, PIPE_IMAGE, BASE_IMAGE
BACKGROUND = pygame.image.load(os.path.join(SPRITE_DIR,selected_background_path)).convert()
PIPE_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, selected_pipe_path)).convert()
BASE_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, selected_base_path)).convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the buttons image
BEGIN_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, 'message.png')).convert_alpha()
START_BUTTON_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, 'start.png')).convert_alpha()
DIFFICULTY_BUTTON_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, 'difficulty.png')).convert_alpha()
EASY_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, 'easy.png')).convert_alpha()
NORMAL_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, 'normal.png')).convert_alpha()
HARD_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, 'hard.png')).convert_alpha()
GAME_OVER_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, 'gameover.png')).convert_alpha()
QUIT_BUTTON_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, 'quit.png')).convert_alpha()
HIGHSCORE_BOARD_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, 'highscore.png')).convert_alpha()
HIGH_SCORE_BUTTON = pygame.image.load(os.path.join(SPRITE_DIR,'more.png')).convert_alpha()
HOME_BUTTON = pygame.image.load(os.path.join(SPRITE_DIR,'home.png')).convert_alpha()
MAPS_BUTTON = pygame.image.load(os.path.join(SPRITE_DIR,'maps.png')).convert_alpha()
FONT_PATH = os.path.join(SPRITE_DIR,'retro.ttf')



# Score assets
score_images = []
for i in range(10):
    img = pygame.image.load(os.path.join(SPRITE_DIR, f'{i}.png')).convert_alpha()
    score_images.append(img)

# Define the size and position of the button
DIFFICULTY_BUTTON_RECT = pygame.Rect(122, 470, 150, 60)
EASY_RECT = pygame.Rect(40, 540, BUTTON_WIDTH, BUTTON_HEIGHT)
NORMAL_RECT = pygame.Rect(150, 540, BUTTON_WIDTH, BUTTON_HEIGHT) 
HARD_RECT = pygame.Rect(260, 540, BUTTON_WIDTH, BUTTON_HEIGHT) 
START_BUTTON_RECT = pygame.Rect(25, 360, 120, 50) 
QUIT_BUTTON_RECT = pygame.Rect(250, 360, 120, 50)
HIGHSCORE_BOARD_RECT = pygame.Rect(70,5,0,0)  
HIGH_SCORE_BUTTON_RECT = pygame.Rect(5, 5, 55, 55) 
MAPS_BUTTON_RECT = pygame.Rect(245, 5, 150, 60) 

# Scale the image to fit the button size
# BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
START_BUTTON_IMAGE = pygame.transform.scale(START_BUTTON_IMAGE, (START_BUTTON_RECT.width, START_BUTTON_RECT.height))
MAPS_BUTTON = pygame.transform.scale(MAPS_BUTTON, (MAPS_BUTTON_RECT.width, MAPS_BUTTON_RECT.height))
DIFFICULTY_BUTTON_IMAGE = pygame.transform.scale(DIFFICULTY_BUTTON_IMAGE, (DIFFICULTY_BUTTON_RECT.width, DIFFICULTY_BUTTON_RECT.height))
EASY_IMAGE = pygame.transform.scale(EASY_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))
NORMAL_IMAGE = pygame.transform.scale(NORMAL_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))
HARD_IMAGE = pygame.transform.scale(HARD_IMAGE, (BUTTON_WIDTH, BUTTON_HEIGHT))
QUIT_BUTTON_IMAGE = pygame.transform.scale(QUIT_BUTTON_IMAGE, (QUIT_BUTTON_RECT.width, QUIT_BUTTON_RECT.height))
HIGHSCORE_BOARD_IMAGE = pygame.transform.scale(HIGHSCORE_BOARD_IMAGE, (200,170))
HIGH_SCORE_BUTTON = pygame.transform.scale(HIGH_SCORE_BUTTON, (HIGH_SCORE_BUTTON_RECT.width, HIGH_SCORE_BUTTON_RECT.height))


clock = pygame.time.Clock()
pixel_font = pygame.font.Font(FONT_PATH, 24)  # Adjust the font size as needed

# Define difficulty settings with pipe gap, pipe spacing, and bird speed
difficulty_settings = {
    "Easy": {
        "pipe_gap": 200,       # Larger gap for easier play
        "pipe_spacing": 800,   # Wider spacing between pipes
        "bird_speed": 15       # Slower speed for easier control
    },
    "Normal": {
        "pipe_gap": 150,       # Medium gap
        "pipe_spacing": 700,   # Medium spacing
        "bird_speed": 20       # Moderate speed
    },
    "Hard": {
        "pipe_gap": 110,       # Smaller gap for harder play
        "pipe_spacing": 600,   # Closer spacing between pipes
        "bird_speed": 25       # Faster speed
    }
}

# Difficulty Button variables
dropdown_open = False  # Tracks if dropdown is open
more_open = False  # Tracks if more is open
difficulty_options = ["Easy", "Normal", "Hard"]
current_difficulty = "Normal"  # Default difficulty

game_over_x = (SCREEN_WIDTH - GAME_OVER_IMAGE.get_width()) // 2
game_over_y = (SCREEN_HEIGHT - GAME_OVER_IMAGE.get_height()) // 2

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(os.path.join(SPRITE_DIR, 'bluebird-upflap.png')).convert_alpha(),
            pygame.image.load(os.path.join(SPRITE_DIR, 'bluebird-midflap.png')).convert_alpha(),
            pygame.image.load(os.path.join(SPRITE_DIR, 'bluebird-downflap.png')).convert_alpha()
        ]
        self.speed = SPEED
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = PIPE_IMAGE
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = BASE_IMAGE
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground((GROUND_WIDTH + GROUND_GAP) * i)  # Uses ground_gap to control spacing
    ground_group.add(ground)


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    # Use NumPy to generate a random height for the top pipe
    size = np.random.randint(100, 300)  # Generate a random height between 100 and 300
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted


pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

# Updated render_score function
def render_score(score, x, y):
    score_str = str(score)
    x_offset = x

    for digit in score_str:
        digit_image = score_images[int(digit)]  # Access the image using int(digit) as index
        screen.blit(digit_image, (x_offset, y))
        x_offset += digit_image.get_width()  # Adjust x position for each digit

high_scores_df = pd.read_csv(high_scores_file)
# Extract the high scores
def get_high_score(difficulty):
    if not high_scores_df.empty:
        try:
            high_score = high_scores_df[high_scores_df['Difficulty'] == difficulty]['High Score'].max()
            return int(high_score) if not pd.isnull(high_score) else 0
        except KeyError:
            return 0
    return 0

def draw_high_scores():
    # Get high scores
    easy_score = get_high_score('Easy')
    normal_score = get_high_score('Normal')
    hard_score = get_high_score('Hard')
    
    draw_score_text(easy_score, 185, 50)   # Position for Easy
    draw_score_text(normal_score, 195, 84) # Position for Normal
    draw_score_text(hard_score, 185, 122)  # Position for Hard

def draw_score_text(score, x, y):
    score_text = pixel_font.render(str(score), True, (255, 255, 255))  # White color
    screen.blit(score_text, (x, y))

def add_entry(filename, start_time, end_time, current_score, current_difficulty):
    # Calculate play duration
    play_duration = (end_time - start_time).total_seconds()

    # Update high score only if current score is higher
    high_scores_data = pd.read_csv(high_scores_file)
    high_score_row = high_scores_data[high_scores_data["Difficulty"] == current_difficulty]
    if current_score > high_score_row["High Score"].values[0]:
        high_scores_data.loc[high_scores_data["Difficulty"] == current_difficulty, "High Score"] = int(current_score)
        high_scores_data.to_csv(high_scores_file, index=False)

    # Create a new entry for the game session
    new_data = pd.DataFrame({
        "Date": [start_time.date()],
        "Start Time": [start_time.strftime('%H:%M:%S')],
        "End Time": [end_time.strftime('%H:%M:%S')],
        "Play Duration (seconds)": [play_duration],
        "Current Score": [int(current_score)],
        "Difficulty": [current_difficulty]
    })

    # Append the new data to the main score file
    existing_data = pd.read_csv(filename)
    updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    updated_data.to_csv(filename, index=False)


def display_game_over():
    # Load and display the "Game Over" image at the center of the screen
    game_over_img = GAME_OVER_IMAGE
    game_over_rect = game_over_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(game_over_img, game_over_rect)
    
    # Display the current score centered below the game-over image
    font = pygame.font.Font(None, 36)  # Adjust the font size as needed
    current_score_text = font.render(f"Score: {int(current_score)}", True, (255, 255, 255))
    current_score_rect = current_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(current_score_text, current_score_rect)

        
    pygame.display.update()
    time.sleep(2)  # Display the game over screen for a short period before returning to the main menu or restarting

# Main loop to handle restarting the game
while True:
    # Start screen loop with three boxes for difficulty selection
    begin = True
    current_score = 0  # Reset score each time we return to the start screen
    pipes_passed_count = 0  # Reset pipes passed count

    while begin:
        clock.tick(15)
        screen.blit(BACKGROUND_MAIN, (0, 0))
        screen.blit(BEGIN_IMAGE, (105, 200))

        # Start button image
        screen.blit(START_BUTTON_IMAGE, START_BUTTON_RECT.topleft)

        # Draw Difficulty Button
        screen.blit(DIFFICULTY_BUTTON_IMAGE, DIFFICULTY_BUTTON_RECT.topleft)

        # Draw the Quit Button
        screen.blit(QUIT_BUTTON_IMAGE, QUIT_BUTTON_RECT.topleft)
        
        # Draw the MAPS Button
        screen.blit(MAPS_BUTTON, MAPS_BUTTON_RECT.topleft)

        # Draw the high score Button
        screen.blit(HIGH_SCORE_BUTTON, HIGH_SCORE_BUTTON_RECT)
        
        if more_open:
                screen.blit(HIGHSCORE_BOARD_IMAGE, HIGHSCORE_BOARD_RECT)    
                draw_high_scores()
        # Draw difficulty option images if dropdown is open
        if dropdown_open:
            screen.blit(EASY_IMAGE, EASY_RECT.topleft)
            screen.blit(NORMAL_IMAGE, NORMAL_RECT.topleft)
            screen.blit(HARD_IMAGE, HARD_RECT.topleft)

            # Highlight the selected option
            if current_difficulty == 'Easy':
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, EASY_RECT, 3)
            elif current_difficulty == 'Normal':
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, NORMAL_RECT, 3)
            elif current_difficulty == 'Hard':
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, HARD_RECT, 3)

        # Event handling for the start screen
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if MAPS_BUTTON_RECT.collidepoint(event.pos):
                    run_map_selection()
                if QUIT_BUTTON_RECT.collidepoint(event.pos):
                    pygame.quit()
                    exit()
                if HIGH_SCORE_BUTTON_RECT.collidepoint(event.pos):
                    more_open = not more_open
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if START_BUTTON_RECT.collidepoint(event.pos):
                    with open("selected_map.json", "r") as file:
                        data = json.load(file)

                    # Extract paths and scaling data
                    selected_background_path = data['assets']['background']
                    selected_pipe_path = data['assets']['pipe']
                    selected_base_path = data['assets']['base']
                    scaling = data['scaling']

                    # Load and scale images
                    # global BACKGROUND, PIPE_IMAGE, BASE_IMAG E
                    BACKGROUND = pygame.image.load(os.path.join(SPRITE_DIR,selected_background_path)).convert()
                    PIPE_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, selected_pipe_path)).convert()
                    BASE_IMAGE = pygame.image.load(os.path.join(SPRITE_DIR, selected_base_path)).convert()
                    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

                    start_time = datetime.now()  # Track start time for session data

                    # Apply difficulty settings and start game
                    PIPE_GAP = difficulty_settings[current_difficulty]["pipe_gap"]
                    PIPE_SPACING = difficulty_settings[current_difficulty]["pipe_spacing"]
                    GAME_SPEED = difficulty_settings[current_difficulty]["bird_speed"]
                    begin = False  # Exit start screen loop to start game

                # Toggle dropdown visibility if Difficulty button is pressed
                elif DIFFICULTY_BUTTON_RECT.collidepoint(event.pos):
                    dropdown_open = not dropdown_open

                # Handle difficulty option selection
                if dropdown_open:
                    if EASY_RECT.collidepoint(event.pos):
                        current_difficulty = 'Easy'
                        dropdown_open = False
                    elif NORMAL_RECT.collidepoint(event.pos):
                        current_difficulty = 'Normal'
                        dropdown_open = False
                    elif HARD_RECT.collidepoint(event.pos):
                        current_difficulty = 'Hard'
                        dropdown_open = False

        pygame.display.flip()

    game_over = False  # Track if the game is over

    # Reset bird and pipes for a new game
    bird.rect[1] = SCREEN_HEIGHT / 2  # Reset bird's vertical position
    bird.speed = 0  # Reset bird's speed

    # Clear and recreate pipes
    pipe_group.empty()  # Clear existing pipes
    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])


    BACKGROUND_SPEED = 2  # Speed for the background

    # Initialize variables for background position
    background_x = 0  # Starting position of the background image
    BACKGROUND_WIDTH = BACKGROUND.get_width()  # Width of the background image

    # In your main game loop
    while not game_over:
        clock.tick(15)

        # Event handling for player input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    bird.bump()
                    pygame.mixer.music.load(wing)
                    pygame.mixer.music.play()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()

        # Redraw the background and update game elements
        # Draw the background image twice for looping effect
        screen.blit(BACKGROUND, (background_x, 0))  # First background
        screen.blit(BACKGROUND, (background_x + BACKGROUND_WIDTH, 0))  # Second background

        # Update the background position to create the illusion of movement
        background_x -= BACKGROUND_SPEED  # Move background to the left at BACKGROUND_SPEED

        # Reset background position when it goes off-screen
        if background_x <= -BACKGROUND_WIDTH:
            background_x = 0  # Reset to the original position

        # Ground and pipe update logic
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 20 if current_difficulty != "Hard" else GROUND_WIDTH - 40)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])
            pipes = get_random_pipes(SCREEN_WIDTH * 2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        # Increment score when the bird passes pipes
        for pipe in pipe_group:
            if bird.rect.left > pipe.rect.right and not getattr(pipe, "passed", False):
                pipe.passed = True  # Mark this pipe as passed
                current_score += 0.5  # Increment score by 0.5 per pipe; 1 point for two pipes
                pygame.mixer.music.load(point)
                pygame.mixer.music.play()

        # Render the score at the top of the screen
        render_score(int(current_score), SCREEN_WIDTH // 2, 50)

        # Update and draw sprite groups
        bird_group.update()
        ground_group.update()
        pipe_group.update()
        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)
        pygame.display.update()

        # Collision detection or game over handling
        if pygame.sprite.spritecollide(bird, pipe_group, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(bird, ground_group, False, pygame.sprite.collide_mask):
            # Play death sound and display game over
            pygame.mixer.music.load(hit)
            pygame.mixer.music.play()
            time.sleep(1)
            pygame.mixer.Sound(die).play()
            display_game_over()

            # Record end time for the session
            end_time = datetime.now()
            add_entry(score_data_file, start_time, end_time, current_score, current_difficulty)

            # Exit the game loop to restart or return to the home screen
            game_over = True
            break
