import random
import math

import pygame

from funcoes import altera_cor_branco


class Arbusto:
    def __init__(self, largura_mundo, altura_mundo):
        self.tamanho_arbusto = random.randint(80, 150)
        self.PosX = random.randint(0, largura_mundo - self.tamanho_arbusto)
        self.PosY = random.randint(0, altura_mundo - self.tamanho_arbusto)
        self.qtd_frutas = random.randint(30, 100)

        self.spritesheet = pygame.image.load(
            "images/objects/spritesheet_arbusto.png"
        ).convert_alpha()

        self.frames_arbusto = []
        self.indice_frame_atual = 0

        largura_frame = self.spritesheet.get_width() // 4
        altura_frame = self.spritesheet.get_height()

        for i in range(4):
            frame = self.spritesheet.subsurface(
                pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame)
            ).copy()
            frame = pygame.transform.scale(
                frame,
                (self.tamanho_arbusto, self.tamanho_arbusto)
            )
            self.frames_arbusto.append(frame)

        self.image = self.frames_arbusto[self.indice_frame_atual]
        self.rect = self.image.get_rect(topleft=(self.PosX, self.PosY))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.qtd_frutas < 0:
            self.qtd_frutas = 0

        if self.qtd_frutas >= 75:
            self.indice_frame_atual = 0
        elif 75 > self.qtd_frutas >= 50:
            self.indice_frame_atual = 1
        elif 50 > self.qtd_frutas >= 25:
            self.indice_frame_atual = 2
        else:
            self.indice_frame_atual = 3

        self.image = self.frames_arbusto[self.indice_frame_atual]


class Criatura:
    MOSTRAR_RAIO_VISAO = True

    def __init__(self, spritesheet, pais=None):
        # Características gerais
        self.nome = None
        self.dieta = None
        self.vida = None
        self.fome = None

        # Mutáveis
        self.nvl_velocidade = None
        self.velocidade = None
        self.tamanho = None
        self.nvl_ataque = None
        self.ataque = None
        self.nvl_defesa = None
        self.defesa = None
        self.nvl_visao = None
        self.visao = None
        self.nvl_espinhos = None
        self.espinhos = None

        self.pais = pais
        self.spritesheet = spritesheet
        self.frames_criatura = []
        self.indice_frame_atual = 0

        self.direcao_x = 0
        self.direcao_y = 0
        self.tempo_movimento = 0
        self.alvo = None
        self.tempo_sem_alvo = 0

        largura_frame = self.spritesheet.get_width() // 4
        altura_frame = self.spritesheet.get_height()

        for i in range(4):
            frame = self.spritesheet.subsurface(
                pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame)
            ).copy()
            self.frames_criatura.append(frame)

        self.image = self.frames_criatura[self.indice_frame_atual]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def gerar_criatura(self):
        """Gera os atributos da criatura a partir dos pais ou para a primeira geração."""
        if self.pais is None:
            self.nome = None
            self.dieta = "Herbívoro"
            self.vida = None
            self.fome = None
            self.nvl_velocidade = 0
            self.velocidade = 8
            self.tamanho = 100
            self.nvl_ataque = 0
            self.ataque = None
            self.nvl_defesa = 0
            self.defesa = None
            self.nvl_visao = 0
            self.visao = None
            self.nvl_espinhos = 0
            self.espinhos = None
        else:
            pai, mae = self.pais
            atributos = [
                "nvl_velocidade", "velocidade", "tamanho",
                "nvl_ataque", "ataque", "nvl_defesa", "defesa",
                "nvl_visao", "visao", "nvl_espinhos", "espinhos"
            ]
            for atributo in atributos:
                setattr(self, atributo, random.choice([
                    getattr(pai, atributo),
                    getattr(mae, atributo)
                ]))
            self.nome = None
            self.dieta = random.choice([pai.dieta, mae.dieta])
            self.vida = random.choice([pai.vida, mae.vida])
            self.fome = random.choice([pai.fome, mae.fome])

    def _obter_raio_visao(self):
        return {0: 0, 1: 15, 2: 40, 3: 100}.get(self.nvl_visao, 0)

    def _movimento_aleatorio(self):
        if self.tempo_movimento <= 0:
            angulo = random.uniform(0, math.tau)
            self.direcao_x = math.cos(angulo)
            self.direcao_y = math.sin(angulo)
            self.tempo_movimento = random.uniform(1.0, 3.0)
        self.tempo_movimento -= 1 / 60

    def _procurar_arbusto(self, arbustos):
        raio = self._obter_raio_visao()
        if raio <= 0:
            return None

        centro = pygame.Vector2(self.rect.center)
        alvo = None
        menor_distancia = float("inf")

        for arbusto in arbustos:
            distancia = centro.distance_to(arbusto.rect.center)
            if distancia <= raio and distancia < menor_distancia:
                menor_distancia = distancia
                alvo = arbusto

        return alvo

    def movimentar(self, arbustos, largura_mundo, altura_mundo, dt=1 / 60):
        fome = self.fome if self.fome is not None else 100

        if fome < 60 and self.nvl_visao > 0:
            self.alvo = self._procurar_arbusto(arbustos)

        if self.alvo is not None:
            destino = pygame.Vector2(self.alvo.rect.center)
            atual = pygame.Vector2(self.rect.center)
            direcao = destino - atual

            if direcao.length() > 2:
                direcao.normalize_ip()
                self.direcao_x = direcao.x
                self.direcao_y = direcao.y
            else:
                self.alvo = None
        elif self.nvl_visao == 0:
            self._movimento_aleatorio()
        elif fome >= 60:
            if self.tempo_movimento <= 0:
                if random.random() < 0.35:
                    self.direcao_x = 0
                    self.direcao_y = 0
                    self.tempo_movimento = random.uniform(1.0, 3.0)
                else:
                    self._movimento_aleatorio()
        else:
            self.tempo_sem_alvo += dt
            if self.tempo_sem_alvo >= 2.0:
                self._movimento_aleatorio()
                self.tempo_sem_alvo = 0

        velocidade = self.velocidade if self.velocidade is not None else 0
        self.rect.x += int(self.direcao_x * velocidade * dt * 60)
        self.rect.y += int(self.direcao_y * velocidade * dt * 60)
        self.rect.clamp_ip(pygame.Rect(0, 0, largura_mundo, altura_mundo))

    def update(self):
        self.indice_frame_atual += 0.07
        if self.indice_frame_atual >= len(self.frames_criatura):
            self.indice_frame_atual = 0

        self.image = self.frames_criatura[int(self.indice_frame_atual)]
        self.image = altera_cor_branco(self.image, (50, 180, 50))
        self.image = pygame.transform.scale(
            self.image,
            (self.tamanho, self.tamanho)
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.size = (self.tamanho, self.tamanho)

    def desenhar_raio_visao(self, superficie, camera_x=0, camera_y=0, zoom=1):
        if not self.MOSTRAR_RAIO_VISAO:
            return

        raio = self._obter_raio_visao()
        if raio <= 0:
            return

        centro_x = int((self.rect.centerx - camera_x) * zoom)
        centro_y = int((self.rect.centery - camera_y) * zoom)
        raio_visual = max(1, int(raio * zoom))

        pygame.draw.circle(
            superficie,
            (255, 255, 255),
            (centro_x, centro_y),
            raio_visual,
            1
        )
