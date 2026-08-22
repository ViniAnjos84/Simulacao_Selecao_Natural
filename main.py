import random

import pygame

from funcoes import ALTURA_MUNDO, LARGURA_MUNDO, cor_grama, exibe_mensagem


WIDTH = 900
HEIGHT = 600


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulação de Seleção Natural")

    temperatura = 15
    zoom = 1.0

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
                zoom += event.y * 0.1
                zoom = max(0.25, min(zoom, 2.0))

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
                int(rect.x * zoom),
                int(rect.y * zoom),
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
