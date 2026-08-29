import random
import math
import string

import pygame

from funcoes import altera_cor_branco, criar_spritesheet_criatura


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
        criaturas_comendo = sum(
            0.025 for criatura in (criaturas or [])
            if getattr(criatura, "alimentando", False)
            and getattr(criatura, "alvo", None) is self
            and getattr(criatura, "esta_vivo", lambda: False)()
        )
        if criaturas_comendo > 0:
            self.qtd_frutas = max(0, self.qtd_frutas - (2 * criaturas_comendo))
            self.tempo_regeneracao = 0
        else:
            self.tempo_regeneracao += dt
            while self.tempo_regeneracao >= 1.0:
                self.qtd_frutas = min(100, self.qtd_frutas + 1)
                self.tempo_regeneracao -= 1.0
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
        self.especie = None
        self.idade = 0
        self._tempo_idade = 0.0
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
        self.reproduzindo = False
        self._carregar_frames()
        self.image = self.frames_criatura[self.indice_frame_atual]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def _carregar_frames(self):
        self.frames_criatura.clear()
        largura_frame = self.spritesheet.get_width() // 4
        altura_frame = self.spritesheet.get_height()
        for i in range(4):
            frame = self.spritesheet.subsurface(pygame.Rect(i * largura_frame, 0, largura_frame, altura_frame)).copy()
            self.frames_criatura.append(frame)

    def _gerar_especie(self):
        return "".join(random.choices(string.ascii_uppercase, k=5))

    def _especies_compativeis(self, outra_criatura):
        if not isinstance(self.especie, str) or not isinstance(outra_criatura.especie, str):
            return False
        if len(self.especie) != 5 or len(outra_criatura.especie) != 5:
            return False
        letras_iguais = sum(
            letra_a == letra_b
            for letra_a, letra_b in zip(self.especie, outra_criatura.especie)
        )
        return letras_iguais >= 3

    def gerar_criatura(self):
        if self.pais is None:
            self.nome = None
            self.especie = "INICIO"
            self.idade = 0
            self._tempo_idade = 0.0
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
            self.nvl_visao = 0
            self.visao = None
            self.nvl_espinhos = 0
            self.espinhos = None
        else:
            pai, mae = self.pais
            self.especie = pai.especie
            self.idade = 0
            self._tempo_idade = 0.0
            atributos = ["nvl_velocidade", "velocidade", "tamanho", "nvl_ataque", "ataque", "nvl_defesa", "defesa", "nvl_visao", "visao", "nvl_espinhos", "espinhos"]
            for atributo in atributos:
                setattr(self, atributo, random.choice([getattr(pai, atributo), getattr(mae, atributo)]))
            self.nome = None
            self.dieta = random.choice([pai.dieta, mae.dieta])
            self.vida = random.choice([pai.vida, mae.vida])
            self.fome = random.choice([pai.fome, mae.fome])
        self.spritesheet = criar_spritesheet_criatura(self, self.spritesheet)
        self._carregar_frames()

    def _obter_raio_visao(self):
        return {0: 60, 1: 120, 2: 250, 3: 450}.get(self.nvl_visao, 60)

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

    def _esta_pronto_para_alimentar(self, arbusto):
        intersecao = self.rect.clip(arbusto.rect)
        return intersecao.width >= 10 and intersecao.height >= 10

    def _procurar_arbusto(self, arbustos):
        raio = self._obter_raio_visao()
        centro = pygame.Vector2(self.rect.center)
        alvo = None
        menor_distancia = float("inf")
        for arbusto in arbustos:
            if arbusto.qtd_frutas <= 25:
                continue
            ponto_mais_proximo = pygame.Vector2(
                max(arbusto.rect.left, min(centro.x, arbusto.rect.right)),
                max(arbusto.rect.top, min(centro.y, arbusto.rect.bottom))
            )
            distancia = centro.distance_to(ponto_mais_proximo)
            if distancia <= raio and distancia < menor_distancia:
                menor_distancia = distancia
                alvo = arbusto
        return alvo

    def _procurar_par(self, criaturas):
        raio = self._obter_raio_visao()
        centro = pygame.Vector2(self.rect.center)
        alvo = None
        menor_distancia = float("inf")
        for criatura in criaturas:
            if criatura is self or not criatura.esta_vivo():
                continue
            if not self._especies_compativeis(criatura):
                continue
            if criatura.fome <= 80 or criatura.idade <= 5:
                continue
            if getattr(criatura, "reproduzindo", False):
                continue
            distancia = centro.distance_to(criatura.rect.center)
            if distancia <= raio and distancia < menor_distancia:
                menor_distancia = distancia
                alvo = criatura
        return alvo

    def alimentar(self):
        self.direcao_x = 0
        self.direcao_y = 0
        self.movendo = False
        self.alimentando = True
        if self.fome is None:
            self.fome = 0
        self.fome = min(100, self.fome + 0.1)
        if self.fome >= 100:
            self.alvo = None
            self.alimentando = False
            self.tempo_sem_alvo = 0
            self.tempo_movimento = 0

    def movimentar(self, arbustos, criaturas, largura_mundo, altura_mundo, dt=1 / 60):
        fome = self.fome if self.fome is not None else 100
        if fome > 80 and self.idade > 5 and not self.alimentando:
            if self.alvo is None or not isinstance(self.alvo, Criatura) or not self._especies_compativeis(self.alvo) or self.alvo.fome <= 80 or self.alvo.idade <= 5:
                self.alvo = self._procurar_par(criaturas)
        if self.alimentando:
            if self.alvo is not None and self.alvo.qtd_frutas > 0 and fome < 100 and self._esta_pronto_para_alimentar(self.alvo):
                self.alimentar()
                return
            self.alimentando = False
            self.alvo = None
            self._iniciar_pausa()
            return
        if self.alvo is not None and isinstance(self.alvo, Criatura):
            if not self.alvo.esta_vivo() or not self._especies_compativeis(self.alvo) or self.alvo.fome <= 80 or self.alvo.idade <= 5:
                self.alvo = None
            else:
                destino = pygame.Vector2(self.alvo.rect.center)
                atual = pygame.Vector2(self.rect.center)
                direcao = destino - atual
                if direcao.length() > 2:
                    direcao.normalize_ip()
                    self.direcao_x = direcao.x
                    self.direcao_y = direcao.y
                    self.movendo = True
                else:
                    self.reproduzindo = True
                    self.direcao_x = 0
                    self.direcao_y = 0
                    self.movendo = False
                    return
        if fome < 60 and self.alvo is None:
            self.alvo = self._procurar_arbusto(arbustos)
        if self.alvo is not None and isinstance(self.alvo, Arbusto):
            if self.alvo.qtd_frutas <= 25:
                self.alvo = None
            elif self._esta_pronto_para_alimentar(self.alvo):
                self.alimentando = True
                self.alimentar()
                return
            else:
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
        if self.alvo is None:
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
            self.rect.y += int(self.direcao_y * self.direcao_y * velocidade * dt * 60)
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

    def update(self, dt=1 / 60):
        if self.fome is not None and not self.alimentando:
            self.fome = max(0, self.fome - 0.05)
        self._tempo_idade += dt
        while self._tempo_idade >= 2.0:
            self.idade += 1
            self._tempo_idade -= 2.0
        self.indice_frame_atual += 0.07
        if self.indice_frame_atual >= len(self.frames_criatura):
            self.indice_frame_atual = 0
        self.image = self.frames_criatura[int(self.indice_frame_atual)]
        self.image = altera_cor_branco(self.image, (50, 180, 50))
        self.image = pygame.transform.scale(self.image, (self.tamanho, self.tamanho))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.size = (self.tamanho, self.tamanho)

    def esta_vivo(self):
        return self.fome is not None and self.fome > 0

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
