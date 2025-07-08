# --- Importar as bibliotecas --- #
import sys
import pygame
from os.path import join
from pytmx.util_pygame import load_pygame

# --- Importar os módulos criados --- #
from level import Level

# --- Importar as configurações --- #
from configuracoes import *



# --- Criar a classe principal do jogo --- #
class Jogo:
    """Classe do jogo."""
    def __init__(self):
        """Função responsável por inicializar a classe."""
        # --- Inicializar o Pygame --- #
        pygame.init()

        # --- Criar a tela do jogo --- #
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

        # --- Título da tela do jogo --- #
        pygame.display.set_caption('Super Pirate World')

        # --- Configurar o FPS --- #
        self.clock = pygame.time.Clock()

        # --- Dicionários com os mapas carregados --- #
        self.mapas_tmx = {
            0: load_pygame(join('..', 'data', 'levels', 'omni.tmx'))
        }

        # --- Instânciar a classe dos levels --- #
        self.estado_atual = Level(self.mapas_tmx[0])

    def executar(self) -> None:
        """Função responsável por executar o jogo."""
        # --- Game loop: on coração do jogo --- #
        while True:
            # --- Obter o tempo entre cada frame --- #
            dt = self.clock.tick() / 1000

            # --- Obter os eventos da tela do jogo --- #
            for evento in pygame.event.get():
                # --- Fechar a tela do jogo --- #
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # --- Executar o estado atual do jogo --- #
            self.estado_atual.executar(dt)

            # --- Atualizar a tela a cada frame --- #
            pygame.display.update()


if __name__ == '__main__':
    # --- Instânciar a classe do jogo --- #
    jogo = Jogo()

    # --- Executar o jogo --- #
    jogo.executar()
