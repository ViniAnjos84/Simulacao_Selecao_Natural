import pygame


def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('Arial', tamanho, True, False)

    mensagem = f'{msg}'

    texto_formatado = fonte.render(mensagem, True, cor)

    # Pega apenas a área realmente ocupada pelo texto (sem padding)
    bounding = texto_formatado.get_bounding_rect()
    texto_recortado = texto_formatado.subsurface(bounding).copy()

    return texto_recortado


def cor_grama(temperatura):
    if temperatura <= 15:
        # -10°C → 15°C
        t = (temperatura + 10) / 25
        cor_fria = (180, 200, 180)
        cor_normal = (50, 150, 50)
    else:
        # 15°C → 40°C
        t = (temperatura - 15) / 25
        cor_normal = (50, 150, 50)
        cor_quente = (190, 150, 40)
        cor_fria = cor_normal
        cor_normal = cor_quente

    r = int(cor_fria[0] + (cor_normal[0] - cor_fria[0]) * t)
    g = int(cor_fria[1] + (cor_normal[1] - cor_fria[1]) * t)
    b = int(cor_fria[2] + (cor_normal[2] - cor_fria[2]) * t)

    return (r, g, b)
