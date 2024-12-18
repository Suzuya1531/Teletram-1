import pygame
from pygame import mixer
from time import sleep
from random import randint

pygame.init()
mixer.init()

janela = pygame.display.set_mode([1056, 716])
pygame.display.set_caption("Teletram - 1")

imagem_fundo = pygame.image.load("C:/Users/samue/OneDrive/Imagens/1140964.png")
player = pygame.image.load("C:/Users/samue/OneDrive/Imagens/b6e67a48a0d410e.png")
inimigo = pygame.image.load("C:/Users/samue/OneDrive/Imagens/08215f87b54c173.png")
tiro = pygame.image.load("C:/Users/samue/OneDrive/Imagens/tiro.png")
tiro_som = mixer.Sound("C:/Users/samue/Downloads/decepticon-null-ray-1-shot-made-with-Voicemod.wav")

# Posição da nave/jogador
jogador = [
    {"imagem1": player, "pos_y_player": randint(300,300), "pos_x_player":randint(475,475), "vel_nave_player": randint(10,10)},]

inimigos = [
    {"imagem": inimigo, "x": randint(0, 1000), "y": randint(-50, 0), "vel_y": randint(1, 5), "mov_x": -1, "mov_y":1}]


tiro_alvo = False
vel_x_missel = 300
pos_y_missel = 300
pos_x_missel = 475
   
pontos = 0
fonte = pygame.font.SysFont("arial", 40, True, True)

# Criação dos retângulos para colisão
player_rect = player.get_rect()
tiro_rect = tiro.get_rect()
inimigo_rect = inimigo.get_rect()

def colisoes():
    global pontuacao
    for player in jogador:
        player_rect= pygame.Rect(player["pos_x_player"], player["pos_y_player"], player["imagem1"].get_width(), player["imagem1"].get_height())
        player_rect.x = player["pos_x_player"]
        player_rect.y = player["pos_y_player"]
        tiro_rect.x = pos_x_missel
        tiro_rect.y = pos_y_missel
        
    # Verificando colisões
    for inimigo in inimigos:
        inimigo_rect = pygame.Rect(inimigo["x"], inimigo["y"], inimigo["imagem"].get_width(), inimigo["imagem"].get_height())
    for player in jogador:
        player_rect = pygame.Rect(player["pos_x_player"], player["pos_y_player"], player["imagem1"].get_width(), player["imagem1"].get_height())

        # Colisão entre o player e os inimigos
        if player_rect.colliderect(inimigo_rect):
            inimigo ["x"] = randint(0,1000) #reseta a posição do inimigo ao colidir com o player
            inimigo ["y"] = randint(-50,10)
            player ["pos_x_player"] = 475
            player ["pos_y_player"] = 300
        # Colisão entre o tiro e os inimigos
        if tiro_rect.colliderect(inimigo_rect):
            # Respawn do inimigo atingido
            inimigo["x"] = randint(0, 1000)
            inimigo["y"] = randint(-50, -50)
            inimigo["vel_y"] = randint(1, 5)
            global pontos
            pontos = pontos +  1

loop = True

while loop:

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            loop = False
           
    # MOVIMENTAÇÃO      
    teclas = pygame.key.get_pressed()
    for player in jogador:
        if teclas[pygame.K_w]:
            
            player ["pos_y_player"] -= player["vel_nave_player"]
        elif teclas[pygame.K_s]:
            player ["pos_y_player"] += player["vel_nave_player"]
        elif teclas[pygame.K_a]:
            player ["pos_x_player"] -= player["vel_nave_player"]
        elif teclas[pygame.K_d]:
            player ["pos_x_player"] += player["vel_nave_player"]
        
    # TIRO
    if teclas[pygame.K_SPACE] and not tiro_alvo:
        tiro_alvo = True
        pos_y_missel = player["pos_y_player"]
        pos_x_missel = player["pos_x_player"]
        tiro_som.play()
        
    if tiro_alvo:
        pos_y_missel -= vel_x_missel 
        if pos_y_missel < 0:
            tiro_alvo = False
            
    for inimigo in inimigos:
        inimigo["x"] += inimigo["mov_x"]
        inimigo["y"] += inimigo["mov_y"]
        
        # Respawn do inimigo se sair da tela
        if inimigo["y"] > 716:
            inimigo["y"] = -50
            inimigo["x"] = randint(-1000, 1000)
            inimigo["vel_y"] = randint(1, 5)
    
    colisoes()
    
    mensagem = f"Pontos: {pontos}"
    texto_formatado = fonte.render(mensagem, False, (255,255,255))
    
    # Limites da nave/jogador
    for player in jogador:
        
        if player ["pos_y_player"] <= 10:
            player["pos_y_player"] += player["vel_nave_player"]
        elif player["pos_y_player"] >= 630:
         player["pos_y_player"] -= player["vel_nave_player"]
        
         if player["pos_x_player"] <= -1000:
            player["pos_x_player"] += player["vel_nave_player"]
        elif player["pos_x_player"] >= 1000:
            player["pos_x_player"] -= player["vel_nave_player"]
        
    janela.blit(imagem_fundo, (0, 0))
    for player in jogador:
         janela.blit(player["imagem1"], (player["pos_x_player"], player["pos_y_player"]))
    
    for inimigo in inimigos:
        janela.blit(inimigo["imagem"], (inimigo["x"], inimigo["y"]))
    
    if tiro_alvo:
        janela.blit(tiro, (pos_x_missel, pos_y_missel))    
    janela.blit(texto_formatado, (850,40))
    
    pygame.display.update()
    print(inimigos)