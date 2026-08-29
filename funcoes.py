import os
import pygame


LARGURA_MUNDO = 900 * 4
ALTURA_MUNDO = 600 * 4


CAMINHO_CARACTERISTICAS = "images/objects/criaturas/caracteristicas"


def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('Arial', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
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


def criar_spritesheet_criatura(criatura, spritesheet):
    """Sobrepoe spritesheets de caracteristicas frame a frame na base."""
    # A spritesheet base ja e uma Surface carregada pela Criatura.
    base = spritesheet.copy().convert_alpha()
    resultado = pygame.Surface(base.get_size(), pygame.SRCALPHA)
    resultado.blit(base, (0, 0))

    caracteristicas = [
        ("nvl_ataque", "ataque"),
        ("nvl_defesa", "defesa"),
        ("nvl_visao", "visao"),
        ("nvl_espinhos", "espinhos"),
    ]

    for nivel_attr, nome_sprite in caracteristicas:
        nivel = getattr(criatura, nivel_attr, 0)

        if nivel is None or nivel <= 0:
            continue

        caminho = os.path.join(CAMINHO_CARACTERISTICAS, f"{nome_sprite}_{nivel}.png")

        if not os.path.exists(caminho):
            continue

        caracteristica = pygame.image.load(caminho).convert_alpha()

        # A caracteristica tambem e uma spritesheet 4x32x32.
        # Ela deve ser colocada inteira sobre a base, sem redimensionar cada frame.
        if caracteristica.get_size() != base.get_size():
            continue

        resultado.blit(caracteristica, (0, 0))

    return resultado
