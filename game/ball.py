import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        # Initialize sound system (only once)
        pygame.mixer.init()

        # Load sound effects (ensure these .wav files exist in your project’s sounds/ folder)
        self.hit_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.wall_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.score_sound = pygame.mixer.Sound("sounds/score.wav")

        # Ball properties
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.wall_sound.play()  # 🔊 play wall bounce sound

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        # Collision with player paddle
        if ball_rect.colliderect(player_rect):
            self.x = player_rect.right
            self.velocity_x = abs(self.velocity_x)
            offset = (self.y + self.height / 2) - (player_rect.y + player_rect.height / 2)
            self.velocity_y += offset * 0.05
            self.hit_sound.play()  # 🔊 play paddle hit sound

        # Collision with AI paddle
        elif ball_rect.colliderect(ai_rect):
            self.x = ai_rect.left - self.width
            self.velocity_x = -abs(self.velocity_x)
            offset = (self.y + self.height / 2) - (ai_rect.y + ai_rect.height / 2)
            self.velocity_y += offset * 0.05
            self.hit_sound.play()  # 🔊 play paddle hit sound

    def reset(self):
        """Reset ball position after a point and play score sound."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        self.score_sound.play()  # 🔊 play score sound

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
