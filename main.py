import random

import pygame

from funcoes import ALTURA_MUNDO, LARGURA_MUNDO
from objetos import Arbusto, Criatura


WIDTH = 900
HEIGHT = 600


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulação de Seleção Natural")

    qtd_arbustos = 50
    zoom = 0.25

    camera_x = 0.0
    camera_y = 0.0
    arrastando_camera = False
    posicao_anterior_mouse = None

    arbustos = [
        Arbusto(LARGURA_MUNDO, ALTURA_MUNDO)
        for _ in range(qtd_arbustos)
    ]

    spritesheet_criatura = pygame.image.load(
        "images/objects/criaturas/criatura_base.png"
    ).convert_alpha()

    criaturas = [
        Criatura(spritesheet_criatura),
        Criatura(spritesheet_criatura)
    ]

    for criatura in criaturas:
        criatura.gerar_criatura()
        criatura.update()
        criatura.rect.topleft = (
            random.randint(0, LARGURA_MUNDO - criatura.rect.width),
            random.randint(0, ALTURA_MUNDO - criatura.rect.height)
        )

    quadrados = []

    TAMANHO = 10

    for _ in range(1000):
        x = random.randint(0, LARGURA_MUNDO - TAMANHO)
        y = random.randint(0, ALTURA_MUNDO - TAMANHO)

        cor1 = (77, 170, 73)
        cor2 = (120, 170, 73)
        cor3 = (120, 125, 73)

        quadrados.append({
            "rect": pygame.Rect(x, y, TAMANHO, TAMANHO),
            "cor": random.choice([cor1, cor2, cor3])
        })

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                mundo_x_antes = camera_x + mouse_x / zoom
                mundo_y_antes = camera_y + mouse_y / zoom

                zoom += event.y * 0.1
                zoom = max(0.25, min(zoom, 2.0))

                camera_x = mundo_x_antes - mouse_x / zoom
                camera_y = mundo_y_antes - mouse_y / zoom

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    arrastando_camera = True
                    posicao_anterior_mouse = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    arrastando_camera = False
                    posicao_anterior_mouse = None

            if event.type == pygame.MOUSEMOTION and arrastando_camera:
                mouse_x, mouse_y = event.pos
                anterior_x, anterior_y = posicao_anterior_mouse

                camera_x -= (mouse_x - anterior_x) / zoom
                camera_y -= (mouse_y - anterior_y) / zoom

                posicao_anterior_mouse = event.pos

        for arbusto in arbustos:
            arbusto.update()

        for criatura in criaturas:
            criatura.movimentar(arbustos, LARGURA_MUNDO, ALTURA_MUNDO, dt)
            criatura.update()

        largura_visivel = WIDTH / zoom
        altura_visivel = HEIGHT / zoom

        camera_x = max(0, min(camera_x, LARGURA_MUNDO - largura_visivel))
        camera_y = max(0, min(camera_y, ALTURA_MUNDO - altura_visivel))

        screen.fill((50, 150, 50))

        for q in quadrados:
            rect = q["rect"]

            rect_visual = pygame.Rect(
                int((rect.x - camera_x) * zoom),
                int((rect.y - camera_y) * zoom),
                max(1, int(rect.width * zoom)),
                max(1, int(rect.height * zoom))
            )

            pygame.draw.rect(screen, q["cor"], rect_visual)

        for arbusto in arbustos:
            rect = arbusto.rect

            rect_visual = pygame.Rect(
                int((rect.x - camera_x) * zoom),
                int((rect.y - camera_y) * zoom),
                max(1, int(rect.width * zoom)),
                max(1, int(rect.height * zoom))
            )

            image = pygame.transform.scale(
                arbusto.image,
                (rect_visual.width, rect_visual.height)
            )
            screen.blit(image, rect_visual)

        for criatura in criaturas:
            rect = criatura.rect

            rect_visual = pygame.Rect(
                int((rect.x - camera_x) * zoom),
                int((rect.y - camera_y) * zoom),
                max(1, int(rect.width * zoom)),
                max(1, int(rect.height * zoom))
            )

            image = pygame.transform.scale(
                criatura.image,
                (rect_visual.width, rect_visual.height)
            )
            screen.blit(image, rect_visual)

            criatura.desenhar_raio_visao(
                screen, camera_x, camera_y, zoom
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
