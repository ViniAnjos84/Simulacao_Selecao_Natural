import os
import pygame


LARGURA_MUNDO = 900 * 4
ALTURA_MUNDO = 600 * 4


CAMINHO_CARACTERISTICAS = "images/objects/criaturas/caracteristicas"


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


def criar_spritesheet_criatura(criatura, spritesheet):
    """Monta a spritesheet da criatura adicionando suas caracteristicas visuais.

    As imagens da pasta caracteristicas sao moldes transparentes e sao colocadas
    sobre cada frame da criatura. A coloracao da criatura acontece depois,
    portanto os moldes permanecem sem cor durante esta etapa.
    """
    base = pygame.image.load(spritesheet).convert_alpha()
    resultado = pygame.Surface(base.get_size(), pygame.SRCALPHA)
    resultado.blit(base, (0, 0))

    caracteristicas = [
        ("nvl_ataque", "ataque"),
        ("nvl_defesa", "defesa"),
        ("nvl_visao", "visao"),
        ("nvl_espinhos", "espinhos"),
    ]

    largura_frame = base.get_width() // 4
    altura_frame = base.get_height()

    for nivel_attr, nome_sprite in caracteristicas:
        nivel = getattr(criatura, nivel_attr, 0)

        # Nivel 0 nao possui sprite adicional.
        if nivel is None or nivel <= 0:
            continue

        caminho = os.path.join(
            CAMINHO_CARACTERISTICAS,
            f"{nome_sprite}_{nivel}.png"
        )

        if not os.path.exists(caminho):
            continue

        caracteristica = pygame.image.load(caminho).convert_alpha()

        # Cada caracteristica e aplicada sobre os quatro frames.
        for indice_frame in range(4):
            x = indice_frame * largura_frame
            frame_caracteristica = caracteristica

            # Mantem o tamanho original do molde quando ele ja corresponde ao frame.
            if frame_caracteristica.get_size() != (largura_frame, altura_frame):
                frame_caracteristica = pygame.transform.scale(
                    frame_caracteristica,
                    (largura_frame, altura_frame)
                )

            resultado.blit(frame_caracteristica, (x, 0))

    return resultado
