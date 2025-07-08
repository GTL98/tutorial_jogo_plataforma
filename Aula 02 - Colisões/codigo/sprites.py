# --- Importar o Pygame --- #
import pygame

# --- Importar as configurações --- #
from configuracoes import *


# --- Classe dos sprites --- #
class Sprites(pygame.sprite.Sprite):
    """Classe para a criação dos sprites."""
    def __init__(self, posicao, superficie, grupos):
        """Função responsável por inicializar a classe."""
        # --- Herdar a classe Sprite() --- #
        super().__init__(grupos)

        # --- Imagem do sprite --- #
        self.image = pygame.Surface((TAMANHO_TILE, TAMANHO_TILE))
        self.image.fill('white')

        # --- Retângulo do sprite --- #
        self.rect = self.image.get_frect(topleft=posicao)
        self.rect_anterior = self.rect.copy()
