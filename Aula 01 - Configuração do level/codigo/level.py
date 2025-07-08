# --- Importar o Pygame --- #
import pygame

# --- Importar os módulos criados--- #
from jogador import Jogador
from sprites import Sprites

# --- Importar as configurações --- #
from configuracoes import *



# --- Classe dos levels --- #
class Level:
    """Classe para a criação dos levels."""
    def __init__(self, mapa_tmx):
        """Função responsável por inicializar a classe."""
        # --- Criar a tela do level a partir da tela do jogo --- #
        self.tela = pygame.display.get_surface()

        # --- Grupo dos sprites --- #
        self.todos_sprites = pygame.sprite.Group()

        # --- Configuração do level --- #
        self.configuracao(mapa_tmx)

    def configuracao(self, mapa_tmx) -> None:
        """
        Função responsável pela configuração do design do level.
        :param mapa_tmx: Mapa TMX do level.
        """
        # --- Desenhar os sprites do terreno no mapa --- #
        for x, y, superficie in mapa_tmx.get_layer_by_name('Terrain').tiles():
            Sprites((x * TAMANHO_TILE, y * TAMANHO_TILE), superficie, self.todos_sprites)

        # --- Desenhar o sprite do jogador no mapa --- #
        for objeto in mapa_tmx.get_layer_by_name('Objects'):
            if objeto.name == 'player':
                Jogador((objeto.x, objeto.y), self.todos_sprites)

    def executar(self, dt) -> None:
        """
        Função responsável por executar a tela do level.
        :param dt: Tempo entre cada frame.
        """
        # --- Atualizar os sprites a cada frame --- #
        self.todos_sprites.update(dt)

        # --- Preencher a tela --- #
        self.tela.fill('black')

        # --- Desenhar os sprites no level --- #
        self.todos_sprites.draw(self.tela)
