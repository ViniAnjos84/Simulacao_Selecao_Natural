import pygame

from funcoes import cor_grama, exibe_mensagem


WIDTH = 900
HEIGHT = 600


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulação de Seleção Natural")

    temperatura = 15

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_PLUS] or teclas[pygame.K_KP_PLUS]:
            temperatura = min(temperatura + 0.5, 40)

        if teclas[pygame.K_MINUS] or teclas[pygame.K_KP_MINUS]:
            temperatura = max(temperatura - 0.5, -15)

        cor_cenario = cor_grama(temperatura)
        screen.fill(cor_cenario)

        texto_temperatura = exibe_mensagem(f"Temperatura: {temperatura:.1f}°C", 24, (255, 255, 255))
        screen.blit(texto_temperatura, (10, HEIGHT - texto_temperatura.get_height() - 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
