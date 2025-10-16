import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60)
        self.winning_score = 5
        self.game_over = False
        self.winner_text = ""

    def handle_input(self):
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

        # Check for winner
        self.check_winner()

    def check_winner(self):
        if self.player_score >= self.winning_score:
            self.game_over = True
            self.winner_text = "Player Wins!"
            self.show_game_over_screen()
        elif self.ai_score >= self.winning_score:
            self.game_over = True
            self.winner_text = "AI Wins!"
            self.show_game_over_screen()

    def show_game_over_screen(self):
        """Display winner + replay menu."""
        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        # Display winner
        winner_surface = self.large_font.render(self.winner_text, True, WHITE)
        winner_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 2 - 80))
        screen.blit(winner_surface, winner_rect)

        # Display replay options
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        for i, text in enumerate(options):
            text_surface = self.font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        self.wait_for_replay_choice()

    def wait_for_replay_choice(self):
        """Wait for user input to restart or exit."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key in (pygame.K_3, pygame.K_5, pygame.K_7):
                        # Determine new winning score based on input
                        if event.key == pygame.K_3:
                            self.winning_score = 3
                        elif event.key == pygame.K_5:
                            self.winning_score = 5
                        elif event.key == pygame.K_7:
                            self.winning_score = 7

                        # Reset everything
                        self.reset_game()
                        waiting = False

    def reset_game(self):
        """Reset all scores and positions for a new match."""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
        self.game_over = False

    def render(self, screen):
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
