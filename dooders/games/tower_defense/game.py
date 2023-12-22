import pygame

from towers import Tower

# Initialize Pygame
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tower Defense Game")

# Colors
SOFT_YELLOW = (255, 253, 208)
LIGHT_GREEN = (144, 238, 144)
FUZZY_BLUE = (173, 216, 230)

# Fonts
font = pygame.font.Font(None, 36)



# Enemy class
class Enemy:
    def __init__(self, path, health, speed):
        self.path = path
        self.health = health
        self.speed = speed
        self.current_path_index = 0
        self.x, self.y = self.path[0]

        # Placeholder image for the enemy, replace with your actual enemy image
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))

    def get_position(self):
        return self.x, self.y

    def move(self):
        # Move along the path
        if self.current_path_index < len(self.path) - 1:
            next_x, next_y = self.path[self.current_path_index + 1]
            direction_x = next_x - self.x
            direction_y = next_y - self.y

            distance = (direction_x**2 + direction_y**2) ** 0.5
            direction_x /= distance
            direction_y /= distance

            self.x += direction_x * self.speed
            self.y += direction_y * self.speed

            # Check if reached next path point
            if (direction_x >= 0 and self.x >= next_x) or (
                direction_x <= 0 and self.x <= next_x
            ):
                if (direction_y >= 0 and self.y >= next_y) or (
                    direction_y <= 0 and self.y <= next_y
                ):
                    self.current_path_index += 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            return True  # Indicates the enemy is defeated
        return False

    def is_defeated(self):
        return self.health <= 0


# Resource Management
resources = 100


def update_resources(amount):
    global resources
    resources += amount


# UI



class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self, screen, font):
        # Draw the button
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_click(self, position):
        if self.rect.collidepoint(position):
            self.callback()


# Initialize buttons
tower_button = Button(700, 100, 80, 40, "Tower", lambda: print("Tower selected"))
upgrade_button = Button(700, 150, 80, 40, "Upgrade", lambda: print("Upgrade"))
sell_button = Button(700, 200, 80, 40, "Sell", lambda: print("Sell"))

# UI settings (example values)
score = 0
resources = 100
wave_number = 1
font = pygame.font.Font(
    None, 36
)  # Use a system font; you can replace it with a custom font


def draw_ui(screen, font):
    # Draw score
    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surf, (10, 10))

    # Draw resources
    resources_surf = font.render(f"Resources: {resources}", True, (255, 255, 255))
    screen.blit(resources_surf, (10, 50))

    # Draw wave number
    wave_surf = font.render(f"Wave: {wave_number}", True, (255, 255, 255))
    screen.blit(wave_surf, (10, 90))

    # Draw buttons
    tower_button.draw(screen, font)
    upgrade_button.draw(screen, font)
    sell_button.draw(screen, font)

    # Status bar for game messages
    status_message = "Prepare for the next wave!"
    status_surf = font.render(status_message, True, (255, 255, 255))
    screen.blit(status_surf, (10, screen_height - 30))





initial_tower = Tower(300, 300, 150, 30, 1000)




# Game Loop
running = True
towers = []
enemies = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tower_button.check_click(event.pos)
            upgrade_button.check_click(event.pos)
            sell_button.check_click(event.pos)

    # Update game state
    for tower in towers:
        tower.attack(enemies)

    for enemy in enemies:
        enemy.move()
        if enemy.is_defeated():
            enemies.remove(enemy)
            update_resources(enemy.reward)

    # Draw everything
    screen.fill(FUZZY_BLUE)  # Background
    # Draw the tower
    initial_tower.draw(screen)
    for tower in towers:
        tower.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    draw_ui(screen, font)

    # Update the display
    pygame.display.update()

# Cleanup
pygame.quit()
