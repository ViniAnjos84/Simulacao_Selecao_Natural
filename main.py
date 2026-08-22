import random

import pygame

from funcoes import ALTURA_MUNDO, LARGURA_MUNDO, cor_grama, exibe_mensagem


WIDTH = 900
HEIGHT = 600


def limitar_camera(camera_x, camera_y, zoom):
    largura_visivel = WIDTH / zoom
    altura_visivel = HEIGHT / zoom

    max_camera_x = max(0, LARGURA_MUNDO - largura_visivel)
    max_camera_y = max(0, ALTURA_MUNDO - altura_visivel)

    camera_x = max(0, min(camera_x, max_camera_x))
    camera_y = max(0, min(camera_y, max_camera_y))

    return camera_x, camera_y


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulação de Seleção Natural")

    temperatura = 15
    zoom = 0.25

    camera_x = 0.0
    camera_y = 0.0

    arrastando = False
    mouse_anterior = (0, 0)

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Posição do mundo que estava sob o mouse antes do zoom.
                mundo_x = camera_x + mouse_x / zoom
                mundo_y = camera_y + mouse_y / zoom

                zoom_anterior = zoom
                zoom += event.y * 0.1
                zoom = max(0.25, min(zoom, 2.0))

                # Mantém o mesmo ponto do mundo sob o mouse após o zoom.
                camera_x = mundo_x - mouse_x / zoom
                camera_y = mundo_y - mouse_y / zoom

                camera_x, camera_y = limitar_camera(camera_x, camera_y, zoom)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                arrastando = True
                mouse_anterior = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                arrastando = False

            if event.type == pygame.MOUSEMOTION and arrastando:
                mouse_x, mouse_y = event.pos
                anterior_x, anterior_y = mouse_anterior

                deslocamento_x = mouse_x - anterior_x
                deslocamento_y = mouse_y - anterior_y

                # O movimento da câmera é inverso ao movimento do mouse.
                camera_x -= deslocamento_x / zoom
                camera_y -= deslocamento_y / zoom

                camera_x, camera_y = limitar_camera(camera_x, camera_y, zoom)
                mouse_anterior = event.pos

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_PLUS] or teclas[pygame.K_KP_PLUS]:
            temperatura = min(temperatura + 0.1, 40)

        if teclas[pygame.K_MINUS] or teclas[pygame.K_KP_MINUS]:
            temperatura = max(temperatura - 0.1, -15)

        cor_cenario = cor_grama(temperatura)
        screen.fill(cor_cenario)

        for q in quadrados:
            rect = q["rect"]
            rect_visual = pygame.Rect(
                int((rect.x - camera_x) * zoom),
                int((rect.y - camera_y) * zoom),
                max(1, int(rect.width * zoom)),
                max(1, int(rect.height * zoom))
            )
            pygame.draw.rect(screen, q["cor"], rect_visual)

        texto_temperatura = exibe_mensagem(
            f"Temperatura: {temperatura:.1f}°C",
            24,
            (255, 255, 255)
        )
        screen.blit(
            texto_temperatura,
            (10, HEIGHT - texto_temperatura.get_height() - 10)
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
