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
        self.pulo = False
        self.altura_pulo = 900

        # --- Colisão do jogador --- #
        self.colisao_sprites = colisao_sprites
        self.na_superficie = {'chao': False, 'esquerda': False, 'direita': False}
        self.plataforma = None

    def entrada(self) -> None:
        """Função repsonsável por receber a entrada do usuário."""
        # --- Obter as teclas pressionadas --- #
        teclas = pygame.key.get_pressed()

        # --- Vetor de entrada ((0, 0) quando iniciar a fase, o jogador não deve se mover sozinho) --- #
        vetor_entrada = vetor(0, 0)

        # --- Se o jogador não estiver na parede, ou seja, andando pelo chão --- #
        if teclas[pygame.K_RIGHT]:
            vetor_entrada.x += 1
        if teclas[pygame.K_LEFT]:
            vetor_entrada.x -= 1

        # --- A direção do jogador é o vetor de entrada --- #
        self.direcao.x = vetor_entrada.normalize().x if vetor_entrada else vetor_entrada.x

        # --- Entrada do pulo --- #
        if teclas[pygame.K_SPACE]:
            self.pulo = True

    def mover(self, dt) -> None:
        """
        Função responsável por movimentar o jogador.
        :param dt: Tempo entre cada frame.
        """
        # --- Movimento horizontal --- #
        self.rect.x += self.direcao.x * self.velocidade * dt
        self.colisao('horizontal')

        # --- Movimento vertical --- #
        if not self.na_superficie['chao'] and any((self.na_superficie['esquerda'], self.na_superficie['direita'])):  # gravidade na parede
            self.direcao.y = 0
            self.rect.y += self.gravidade / 10 * dt
        else:  # gravidade normal
            self.direcao.y += self.gravidade / 2 * dt
            self.rect.y += self.direcao.y * dt
            self.direcao.y += self.gravidade / 2 * dt

        if self.pulo:
            if self.na_superficie['chao']:  # verificar se o jogador está no chão
                self.direcao.y = -self.altura_pulo  # pula
                self.rect.bottom -= 1
            elif any((self.na_superficie['esquerda'], self.na_superficie['direita'])):
                self.direcao.y = -self.altura_pulo
                self.direcao.x = 1 if self.na_superficie['esquerda'] else -1
            self.pulo = False  # evita que fique voando

        self.colisao('vertical')

    def movimento_plataforma(self, dt) -> None:
        """
        Função responsável por movimentar o jogador junto com a plataforma.
        :param dt: Tempo entre cada frame.
        """
        if self.plataforma:
            self.rect.topleft += self.plataforma.direcao * self.plataforma.velocidade * dt

    def verificar_contato(self) -> None:
        """Função responsável por verificar o contato do jogador com a
        superfície dos sprites estruturais do mapa."""
        # --- Criar os retângulos de colisão do sprite do jogador --- #
        chao_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, 2))
        direita_rect = pygame.Rect(self.rect.topright + vetor(0, self.rect.height / 4), (2, self.rect.height / 2))
        esquerda_rect = pygame.Rect(self.rect.topleft + vetor(-2, self.rect.height / 4), (2, self.rect.height / 2))

        # --- Lista com os rects para a colisão --- #
        colisao_rects = [sprite.rect for sprite in self.colisao_sprites]

        # --- Verificar as colisões --- #
        self.na_superficie['chao'] = True if chao_rect.collidelist(colisao_rects) >= 0 else False
        self.na_superficie['direita'] = True if direita_rect.collidelist(colisao_rects) >= 0 else False
        self.na_superficie['esquerda'] = True if esquerda_rect.collidelist(colisao_rects) >= 0 else False

        # --- Se o jogador estiver na plataforma --- #
        self.plataforma = None
        for sprite in [sprite for sprite in self.colisao_sprites.sprites() if hasattr(sprite, 'movimento')]:
            if sprite.rect.colliderect(chao_rect):
                self.plataforma = sprite

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

        # --- Atualizar a posição do jogador quando na plataforma --- #
        self.movimento_plataforma(dt)

        # --- Verificar se houve colisão entre o jogador e o mapa --- #
        self.verificar_contato()
