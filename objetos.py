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
        self.spritesheet = pygame.image.load("images/objects/spritesheet_arbusto.png").convert_alpha()
        self.frames_arbusto = []
        self.indice_frame_atual = 0
        self.tempo_regeneracao = 0
        largura_frame = self.spritesheet.get_width() // 4
        altura_frame = self.spritesheet.get_height()
        for i in range(4):
            frame = self.spritesheet.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame)).copy()
            frame = pygame.transform.scale(frame, (self.tamanho_arbusto, self.tamanho_arbusto))
            self.frames_arbusto.append(frame)
        self.image = self.frames_arbusto[self.indice_frame_atual]
        self.rect = self.image.get_rect(topleft=(self.PosX, self.PosY))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, criaturas=None, dt=1 / 60):
        self.qtd_frutas = max(0, min(100, self.qtd_frutas))

        # Cada criatura efetivamente se alimentando deste arbusto consome 2 frutas por frame.
        criaturas_comendo = sum(
            1 for criatura in (criaturas or [])
            if getattr(criatura, "alimentando", False)
            and getattr(criatura, "alvo", None) is self
        )

        if criaturas_comendo > 0:
            self.qtd_frutas = max(0, self.qtd_frutas - (2 * criaturas_comendo))
            self.tempo_regeneracao = 0
        else:
            # Recupera 1 fruta por segundo, independentemente do FPS.
            self.tempo_regeneracao += dt
            while self.tempo_regeneracao >= 1.0:
                self.qtd_frutas = min(100, self.qtd_frutas + 1)
                self.tempo_regeneracao -= 1.0

        # 4 frames: cheio, 75%, 50%, vazio.
        if self.qtd_frutas > 75:
            self.indice_frame_atual = 0
        elif self.qtd_frutas > 50:
            self.indice_frame_atual = 1
        elif self.qtd_frutas > 25:
            self.indice_frame_atual = 2
        else:
            self.indice_frame_atual = 3

        self.image = self.frames_arbusto[self.indice_frame_atual]


class Criatura:
    MOSTRAR_RAIO_VISAO = True
    MOSTRAR_BARRA_FOME = True

    def __init__(self, spritesheet, pais=None):
        self.nome = None
        self.dieta = None
        self.vida = None
        self.fome = None
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
        self.movendo = False
        self.alimentando = False
        largura_frame = self.spritesheet.get_width() // 4
        altura_frame = self.spritesheet.get_height()
        for i in range(4):
            frame = self.spritesheet.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame)).copy()
            self.frames_criatura.append(frame)
        self.image = self.frames_criatura[self.indice_frame_atual]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def gerar_criatura(self):
        if self.pais is None:
            self.nome = None
            self.dieta = "Herbívoro"
            self.vida = None
            self.fome = 100
            self.nvl_velocidade = 0
            self.velocidade = 4
            self.tamanho = 50
            self.nvl_ataque = 0
            self.ataque = None
            self.nvl_defesa = 0
            self.defesa = None
            self.nvl_visao = 3
            self.visao = None
            self.nvl_espinhos = 0
            self.espinhos = None
        else:
            pai, mae = self.pais
            atributos = ["nvl_velocidade", "velocidade", "tamanho", "nvl_ataque", "ataque", "nvl_defesa", "defesa", "nvl_visao", "visao", "nvl_espinhos", "espinhos"]
            for atributo in atributos:
                setattr(self, atributo, random.choice([getattr(pai, atributo), getattr(mae, atributo)]))
            self.nome = None
            self.dieta = random.choice([pai.dieta, mae.dieta])
            self.vida = random.choice([pai.vida, mae.vida])
            self.fome = random.choice([pai.fome, mae.fome])

    def _obter_raio_visao(self):
        return {0: 0, 1: 120, 2: 250, 3: 450}.get(self.nvl_visao, 0)

    def _iniciar_movimento_aleatorio(self):
        angulo = random.uniform(0, math.tau)
        self.direcao_x = math.cos(angulo)
        self.direcao_y = math.sin(angulo)
        self.tempo_movimento = random.uniform(1.0, 2.0)
        self.movendo = True

    def _iniciar_pausa(self):
        self.direcao_x = 0
        self.direcao_y = 0
        self.tempo_movimento = random.uniform(1.0, 2.0)
        self.movendo = False

    def _procurar_arbusto(self, arbustos):
        raio = self._obter_raio_visao()
        if raio <= 0:
            return None
        centro = pygame.Vector2(self.rect.center)
        alvo = None
        menor_distancia = float("inf")
        for arbusto in arbustos:
            if arbusto.qtd_frutas <= 25:
                continue
            distancia = centro.distance_to(arbusto.rect.center)
            if distancia <= raio and distancia < menor_distancia:
                menor_distancia = distancia
                alvo = arbusto
        return alvo

    def alimentar(self, arbusto):
        self.direcao_x = 0
        self.direcao_y = 0
        self.movendo = False
        self.alimentando = True
        if self.fome is None:
            self.fome = 0
        self.fome = min(100, self.fome + 0.5)
        if self.fome >= 100:
            self.alvo = None
            self.alimentando = False
            self.tempo_sem_alvo = 0
            self.tempo_movimento = 0

    def movimentar(self, arbustos, largura_mundo, altura_mundo, dt=1 / 60):
        fome = self.fome if self.fome is not None else 100

        if self.alimentando:
            if self.alvo is not None and self.alvo.qtd_frutas > 0 and fome < 100:
                self.alimentar(self.alvo)
                return
            self.alimentando = False
            self.alvo = None
            self._iniciar_pausa()
            return

        if self.alvo is not None and self.rect.colliderect(self.alvo.rect):
            self.alimentando = True
            self.alimentar(self.alvo)
            return

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
                self.movendo = True
            else:
                self.alvo = None
        elif self.nvl_visao == 0 or fome < 60:
            if self.tempo_movimento <= 0:
                if self.movendo:
                    self._iniciar_pausa()
                else:
                    self._iniciar_movimento_aleatorio()
        elif fome >= 60:
            if self.tempo_movimento <= 0:
                if self.movendo:
                    self._iniciar_pausa()
                else:
                    self._iniciar_movimento_aleatorio()

        if self.tempo_movimento > 0:
            self.tempo_movimento -= dt

        velocidade = self.velocidade if self.velocidade is not None else 0
        if self.movendo:
            self.rect.x += int(self.direcao_x * velocidade * dt * 60)
            self.rect.y += int(self.direcao_y * velocidade * dt * 60)

        bateu_horizontal = False
        bateu_vertical = False
        if self.rect.left <= 0:
            self.rect.left = 0
            bateu_horizontal = True
            self.direcao_x = abs(self.direcao_x)
        elif self.rect.right >= largura_mundo:
            self.rect.right = largura_mundo
            bateu_horizontal = True
            self.direcao_x = -abs(self.direcao_x)
        if self.rect.top <= 0:
            self.rect.top = 0
            bateu_vertical = True
            self.direcao_y = abs(self.direcao_y)
        elif self.rect.bottom >= altura_mundo:
            self.rect.bottom = altura_mundo
            bateu_vertical = True
            self.direcao_y = -abs(self.direcao_y)
        if bateu_horizontal or bateu_vertical:
            self.alvo = None
            self._iniciar_pausa()

    def update(self):
        if self.fome is not None and not self.alimentando:
            self.fome = max(0, self.fome - 0.05)
        self.indice_frame_atual += 0.07
        if self.indice_frame_atual >= len(self.frames_criatura):
            self.indice_frame_atual = 0
        self.image = self.frames_criatura[int(self.indice_frame_atual)]
        self.image = altera_cor_branco(self.image, (50, 180, 50))
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))
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
        pygame.draw.circle(superficie, (255, 255, 255), (centro_x, centro_y), raio_visual, 1)

    def desenhar_barra_fome(self, superficie, camera_x=0, camera_y=0, zoom=1):
        if not self.MOSTRAR_BARRA_FOME:
            return
        fome = max(0, min(100, self.fome if self.fome is not None else 0))
        largura = max(20, int(self.tamanho * zoom))
        altura = max(4, int(6 * zoom))
        x = int((self.rect.centerx - camera_x) * zoom - largura / 2)
        y = int((self.rect.top - camera_y) * zoom - altura - 5 * zoom)
        pygame.draw.rect(superficie, (40, 40, 40), pygame.Rect(x, y, largura, altura))
        pygame.draw.rect(superficie, (60, 200, 60), pygame.Rect(x, y, int(largura * fome / 100), altura))
