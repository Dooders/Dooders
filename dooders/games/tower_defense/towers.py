import pygame

tower_image = pygame.image.load('assets/tower.png')

# Smoothly scale the image to the desired size
desired_size = (100, 100)  # Adjust the size as needed
tower_image = pygame.transform.smoothscale(tower_image, desired_size)

class Tower:
    """
    Tower class

    Attributes
    ----------
    x : int
        x position of the tower
    y : int
        y position of the tower
    range : int
        range of the tower
    damage : int
        damage of the tower
    attack_speed : int
        attack speed of the tower
    last_attack_time : int
        last time the tower attacked
    image : pygame.Surface
        image of the tower

    Methods
    -------
    draw(screen: pygame.Surface) -> None:
        Draws the tower on the screen
    attack(enemies: list) -> None:
        Attacks the enemies
    is_enemy_in_range(enemy: object) -> bool:
        Checks if an enemy is in range
    """

    def __init__(
        self, x: int, y: int, range: int, damage: int, attack_speed: int
    ) -> None:
        """
        Parameters
        ----------
        x : int
            x position of the tower
        y : int
            y position of the tower
        range : int
            range of the tower
        damage : int
            damage of the tower
        attack_speed : int
            attack speed of the tower
        """
        self.x = x
        self.y = y
        self.range = range
        self.damage = damage
        self.attack_speed = attack_speed
        self.last_attack_time = pygame.time.get_ticks()

        # Placeholder image for the tower, replace with your actual tower image
        self.image = tower_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen: pygame.Surface) -> None:
        """
        Parameters
        ----------
        screen : pygame.Surface
            screen to draw the tower on
        """
        screen.blit(self.image, self.rect)

    def attack(self, enemies: list) -> None:
        """
        Parameters
        ----------
        enemies : list
            list of enemies to attack
        """
        # Current time
        current_time = pygame.time.get_ticks()

        # Check if it's time to attack
        if current_time - self.last_attack_time > self.attack_speed:
            for enemy in enemies:
                # Check if enemy is in range and attack
                if self.is_enemy_in_range(enemy):
                    enemy.take_damage(self.damage)
                    self.last_attack_time = current_time
                    break

    def is_enemy_in_range(self, enemy: object) -> bool:
        """
        Parameters
        ----------
        enemy : object
            enemy to check if in range

        Returns
        -------
        bool
            True if enemy is in range, False otherwise
        """
        # Calculate distance to the enemy and check if within range
        enemy_x, enemy_y = enemy.get_position()
        distance = ((enemy_x - self.x) ** 2 + (enemy_y - self.y) ** 2) ** 0.5
        return distance <= self.range
