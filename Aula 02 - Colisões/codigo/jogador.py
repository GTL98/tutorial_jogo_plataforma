# --- Importar o Pygame --- #
import pygame
from pygame.math import Vector2 as vetor


# --- Classe do jogador --- #
class Jogador(pygame.sprite.Sprite):
    """Classe do jogador."""
    def __init__(self, posicao, grupos, colisao_sprites):
        """Função responsável por inicializar a classe."""
        # --- Herdar a classe Sprites() --- #
        super().__init__(grupos)

        # --- Imagem do sprite do jogador --- #
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')

        # --- Retângulo do sprite do jogador --- #
        self.rect = self.image.get_frect(topleft=posicao)
        self.rect_anterior = self.rect.copy()  # o Pygame sabe de qual lado o jogador veio

        # --- Movimento do jogador --- #
        self.direcao = vetor(0, 0)
        self.velocidade = 200
        self.gravidade = 1300

        # --- Colisão do jogador --- #
        self.colisao_sprites = colisao_sprites

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
        self.direcao.x = vetor_entrada.normalize().x if vetor_entrada else vetor_entrada.x

    def mover(self, dt) -> None:
        """
        Função responsável por movimentar o jogador.
        :param dt: Tempo entre cada frame.
        """
        # --- Movimento horizontal --- #
        self.rect.x += self.direcao.x * self.velocidade * dt
        self.colisao('horizontal')

        # --- Movimento vertical --- #
        self.direcao.y += self.gravidade / 2 * dt
        self.rect.y += self.direcao.y * dt
        self.direcao.y += self.gravidade / 2 * dt
        self.colisao('vertical')

    def colisao(self, eixo) -> None:
        """
        Função responsável por detectar a colisão do jogador.
        :param eixo: Eixo da colisão ('horizontal' ou 'vertical')
        """
        # --- Obter cada sprite da lista de colisão --- #
        for sprite in self.colisao_sprites:
            # --- Verificar se o rect dos sprites colidiram com o jogador --- #
            if sprite.rect.colliderect(self.rect):
                # --- Se a colisão foi horizonatal --- #
                if eixo == 'horizontal':
                    # --- Colisão do lado esquerdo --- #
                    if self.rect.left <= sprite.rect.right and self.rect_anterior.left >= sprite.rect_anterior.right:
                        self.rect.left = sprite.rect.right

                    # --- Colisão do lado direito --- #
                    if self.rect.right >= sprite.rect.left and self.rect_anterior.right <= sprite.rect_anterior.left:
                        self.rect.right = sprite.rect.left
                # --- Se a colisão for vertical --- #
                else:
                    # --- Colisão com o solo --- #
                    if self.rect.bottom >= sprite.rect.top and self.rect_anterior.bottom <= sprite.rect_anterior.top:
                        self.rect.bottom = sprite.rect.top

                    # --- Colisão com o teto --- #
                    if self.rect.top <= sprite.rect.bottom and self.rect_anterior.top >= sprite.rect_anterior.bottom:
                        self.rect.top = sprite.rect.bottom

                    # --- Evitar que a velocidade vertical aumente para sempre --- #
                    self.direcao.y = 0

    def update(self, dt) -> None:
        """
        Função responsável por atualizar o sprite cada vez que o jogador se mover.
        :param dt: Tempo entre cada frame.
        """
        # --- Obter o rect do frame anterior --- #
        self.rect_anterior = self.rect.copy()

        # --- Atualizar as entradas --- #
        self.entrada()

        # --- Atualizar os movimentos --- #
        self.mover(dt)