# --- Importar o Pygame --- #
import pygame
from pygame.math import Vector2 as vetor

# --- Importar as configurações --- #
from configuracoes import *


# --- Classe dos sprites --- #
class Sprites(pygame.sprite.Sprite):
    """Classe para a criação dos sprites."""
    def __init__(self, posicao, superficie=pygame.Surface((TAMANHO_TILE, TAMANHO_TILE)), grupos=None):
        """Função responsável por inicializar a classe."""
        # --- Herdar a classe Sprite() --- #
        super().__init__(grupos)

        # --- Imagem do sprite --- #
        self.image = superficie
        self.image.fill('white')

        # --- Retângulo do sprite --- #
        self.rect = self.image.get_frect(topleft=posicao)
        self.rect_anterior = self.rect.copy()


# --- Classe dos sprites móveis --- #
class SpritesMoveis(Sprites):
    """Classe dos sprites móveis."""
    def __init__(self, grupos, pos_inicial, pos_final, direcao_movimento, velocidade):
        """Função responsável por inicializar a classe."""
        # --- Criar a superfície --- #
        superficie = pygame.Surface((200, 50))

        # --- Herdar a classe pai (Sprites) --- #
        super().__init__(pos_inicial, superficie, grupos)

        # --- Centralizar o sprite no centro do movimento --- #
        if direcao_movimento == 'x':
            self.rect.midleft = pos_inicial
        else:
            self.rect.midtop = pos_inicial

        # --- Posição --- #
        self.pos_inicial = pos_inicial
        self.pos_final = pos_final

        # --- Movimento --- #
        self.movimento = True
        self.velocidade = velocidade
        self.direcao = vetor(1, 0) if direcao_movimento == 'x' else vetor(0, 1)
        self.direcao_movimento = direcao_movimento

    def verificar_limite(self) -> None:
        """Função responsável por limitar o caminho dos sprites móveis."""
        # --- Limitar o movimento no eixo X --- #
        if self.direcao_movimento == 'x':
            if self.rect.right >= self.pos_final[0] and self.direcao.x == 1:
                self.direcao.x = -1
                self.rect.right = self.pos_final[0]
            if self.rect.left <= self.pos_inicial[0] and self.direcao.x == -1:
                self.direcao.x = 1
                self.rect.left = self.pos_inicial[0]
        else:
            if self.rect.bottom >= self.pos_final[1] and self.direcao.y == 1:
                self.direcao.y = -1
                self.rect.bottom = self.pos_final[1]
            if self.rect.top <= self.pos_inicial[1] and self.direcao.y == -1:
                self.direcao.y = 1
                self.rect.top = self.pos_inicial[1]

    def update(self, dt) -> None:
        """
        Função responsável por atualizar os sprites móveis.
        :param dt: Tempo entre cada frame.
        """
        # --- Copiar o rect para verificar o rect anterior --- #
        self.rect_anterior = self.rect.copy()

        # --- Movimentação do sprite móvel --- #
        self.rect.topleft += self.direcao * self.velocidade * dt

        # --- Limitar o caminho dos sprites móveis --- #
        self.verificar_limite()
