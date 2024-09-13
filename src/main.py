import pygame
import sys

# Inicializar o PyGame
pygame.init()

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")


# Classes para o jogador, inimigos e balas
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))  # Criar um retângulo verde para o jogador
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        # Não precisa de argumento keys, movemos o jogador aqui
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))  # Criar um retângulo vermelho para os inimigos
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self):
        # Movimento dos inimigos (horizontal e descida quando tocam as bordas)
        self.rect.x += self.speed
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed *= -1
            self.rect.y += 20


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Um retângulo pequeno para as balas
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        # Movimento vertical da bala
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()  # Remove a bala quando ela sai da tela


# Função principal do jogo
def main():
    clock = pygame.time.Clock()

    # Instanciar jogador, grupos de inimigos e balas
    player = Player()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Criar múltiplos inimigos
    for i in range(5):
        for j in range(3):
            enemy = Enemy(100 + i * 100, 50 + j * 60)
            enemies.add(enemy)

    # Agrupar todos os sprites para desenhar e atualizar
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemies)

    running = True
    while running:
        # Processar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Atualizar o jogador (sem precisar de argumento keys)
        all_sprites.update()

        # Atirar bala quando a barra de espaço for pressionada
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

        # Verificar colisões entre balas e inimigos
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            if hits:
                bullet.kill()  # Remove a bala quando atingir um inimigo

        # Desenhar tudo na tela
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

        # Definir a taxa de quadros (FPS)
        clock.tick(30)


if __name__ == "__main__":
    main()
