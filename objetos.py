import random

import pygame


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
