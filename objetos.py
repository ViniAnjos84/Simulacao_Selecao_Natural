import random

import pygame

from funcoes import altera_cor_branco


class Arbusto:
    def __init__(self, largura_mundo, altura_mundo):
        self.tamanho_arbusto = random.randint(100, 200)
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
    def __init__(self, spritesheet, pais=None):
        self.Nome = None
        self.Dieta = None
        self.Vida = None
        self.Fome = None
        self.Velocidade = None
        self.Tamanho = None
        self.Ataque = None
        self.Defesa = None
        self.Visão = None
        self.Espinhos = None

        self.pais = pais
        self.spritesheet = spritesheet
        self.image = self.spritesheet
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def gerar_criatura(self):
        """Gera os atributos da criatura a partir dos pais ou aleatoriamente."""
        if self.pais is None:
            self.Nome = None
            self.Dieta = random.choice(["Herbívoro", "Carnívoro"])
            self.Vida = random.randint(50, 100)
            self.Fome = random.randint(0, 100)
            self.Velocidade = random.uniform(1.0, 5.0)
            self.Tamanho = random.randint(10, 30)
            self.Ataque = random.randint(1, 10)
            self.Defesa = random.randint(1, 10)
            self.Visão = random.randint(50, 300)
            self.Espinhos = random.choice([True, False])
        else:
            pai, mae = self.pais
            atributos = [
                "Dieta", "Vida", "Fome", "Velocidade", "Tamanho",
                "Ataque", "Defesa", "Visão", "Espinhos"
            ]

            for atributo in atributos:
                setattr(self, atributo, random.choice([
                    getattr(pai, atributo),
                    getattr(mae, atributo)
                ]))

        self.image = self.spritesheet
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
