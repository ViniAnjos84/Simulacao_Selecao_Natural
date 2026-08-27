import pygame


LARGURA_MUNDO = 900 * 5
ALTURA_MUNDO = 600 * 5


def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('Arial', tamanho, True, False)

    mensagem = f'{msg}'

    texto_formatado = fonte.render(mensagem, True, cor)

    # Pega apenas a área realmente ocupada pelo texto (sem padding)
    bounding = texto_formatado.get_bounding_rect()
    texto_recortado = texto_formatado.subsurface(bounding).copy()

    return texto_recortado


def altera_cor_branco(imagem, cor):
    imagem = imagem.copy()
    largura, altura = imagem.get_size()

    for x in range(largura):
        for y in range(altura):
            if imagem.get_at((x, y))[:3] == (255, 255, 255):
                alpha = imagem.get_at((x, y))[3]
                imagem.set_at((x, y), (*cor, alpha))

    return imagem
