import pygame

from funcoes import cor_grama


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

        cor_cenario = cor_grama(temperatura)
        screen.fill(cor_cenario)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
