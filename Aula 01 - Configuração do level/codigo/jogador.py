# --- Importar o Pygame --- #
import pygame
from pygame.math import Vector2 as vetor

# --- Importar as configurações --- #
from configuracoes import *


# --- Classe do jogador --- #
class Jogador(pygame.sprite.Sprite):
    """Classe do jogador."""
    def __init__(self, posicao, grupos):
        """Função responsável por inicializar a classe."""
        # --- Herdar a classe Sprites() --- #
        super().__init__(grupos)

        # --- Imagem do sprite do jogador --- #
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')

        # --- Retângulo do sprite do jogador --- #
        self.rect = self.image.get_frect(topleft=posicao)

        # --- Movimento do jogador --- #
        self.direcao = vetor(0, 0)
        self.velocidade = 200

    def entrada(self) -> None:
        """Função repsonsável por receber a entrada do usuário."""
        # --- Obter as teclas pressionadas --- #
        teclas = pygame.key.get_pressed()

        # --- Vetor de entrada ((0, 0) quando iniciar a fase, o jogador não deve se mover sozinho) --- #
        vetor_entrada = vetor(0, 0)

        # --- Verificar qual tecla foi pressionada --- #
        if teclas[pygame.K_RIGHT]:
            vetor_entrada.x += 1
        if teclas[pygame.K_LEFT]:
            vetor_entrada.x -= 1

        # --- A direção do jogador é o vetor de entrada --- #
        self.direcao = vetor_entrada.normalize() if vetor_entrada else vetor_entrada

    def mover(self, dt) -> None:
        """
        Função responsável por movimentar o jogador.
        :param dt: Tempo entre cada frame.
        """
        # --- Movimentar o jogador --- #
        self.rect.topleft += self.direcao * self.velocidade * dt

    def update(self, dt) -> None:
        """
        Função responsável por atualizar o sprite cada vez que o jogador se mover.
        :param dt: Tempo entre cada frame.
        """
        # --- Atualizar as entradas --- #
        self.entrada()

        # --- Atualizar os movimentos --- #
        self.mover(dt)