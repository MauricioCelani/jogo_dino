#Tutorial https://www.youtube.com/watch?v=Zugjmqelux4
# Ainda não finalizei por completo o código, apresenta alguns bugs que tentarei resolver
import pygame
from pygame.locals import *
from random import randint,randrange,choice
from time import sleep
import os
from sys import exit

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,'imagens')
diretorio_sons = os.path.join(diretorio_principal,'sons')

contador_pause = 0
pygame.init()
pygame.mixer.init()
largura = 1360
altura = 700
gameloop = True

clock = pygame.time.Clock()
display = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Minha versão do Dino Game')
obstaculo_aleat = choice([0,1])

#Cores do jogo
vermelho = [255,0,0]
verde = [0,255,0]
azul = [0,0,255]
preto = [0,0,0]
branco = [255,255,255]
cinza = [128,128,128]
amarelo = [255,255,0]

tam_player = 64
qtd_nuvens = 7
intensidade_do_pulo = 12
intensidade_da_queda = 20
altura_pulo = 300
pontuação = 0

velocidade_geral = 5
velocidade_nuvens = 8
velocidade_piso = 5
#velocidade_cacto = velocidade_geral
velocidade_vilao = 10
max_vel = 20

moeda_img = pygame.image.load(os.path.join(diretorio_imagens,'moeda_2.png'))
moeda_img = pygame.transform.scale(moeda_img,(32*2,32*2))
moedas = 0
vidas = 10

'''def perdeu_vida(vidas):
    vidas -= 1
    if vidas == 0:
        gameloop = False'''
def mensagem(texto,size,cor):
    fonte_pontuação = pygame.font.SysFont('comicsanssms',size,False,False)
    mensagem = f'{texto}'
    mensagem_exibida = fonte_pontuação.render(mensagem,True,cor)
    return mensagem_exibida
def restart():
    global pontuação,colidiu_cacto,velocidade_vilao,velocidade_geral
    player.rect.y = altura - tam_player - 96//2
    player.is_jumping = False
    pontuação = 0
    colidiu_cacto = False
    velocidade_geral = 5
    velocidade_vilao = 10
    vilao_dino.rect.x = largura
    cacto.rect.x = largura

pausado = False
def jogo_pausado():
    global velocidade_piso,velocidade_geral,velocidade_vilao,pausado
    pausado = True
    velocidade_geral = 0
    velocidade_vilao = 0
    velocidade_piso = 0
    pontos_pause = pontuação
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens,'dinoSpritesheet.png')).convert_alpha()
colidiu_cacto = False

som_pontos = pygame.mixer.Sound(os.path.join(diretorio_sons,'score_sound.wav'))
som_pontos.set_volume(1)
som_colisão = pygame.mixer.Sound(os.path.join(diretorio_sons,'death_sound.wav'))
som_colisão.set_volume(1)
som_moeda = pygame.mixer.Sound(os.path.join(diretorio_sons,'smw_coin.wav'))
som_moeda.set_volume(1)

class Moeda(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = moeda_img
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.y = randrange(player.pos_y_inicial, altura - tam_player, 50)
        self.rect.x = randint(largura, largura * 2)

    def update(self):
        if self.rect.topright[0] < 0:
            self.reset()
        self.rect.x -= velocidade_geral
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagem_dino = []
        self.dino_soundjump = pygame.mixer.Sound(os.path.join(diretorio_sons,'jump_sound.wav'))
        self.dino_soundjump.set_volume(1)
        #verificar cada sprite contido na pasta. i * 32 pois cada um tem 32 por 32 de tamanho
        for i in range(3):
            img = sprite_sheet.subsurface((i*32, 0), (32, 32))
            img = pygame.transform.scale(img,(32*3,32*3))
            self.imagem_dino.append(img)
        self.posição_lista_dino = 0
        self.image = self.imagem_dino[self.posição_lista_dino]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.pos_y_inicial = altura-tam_player - 96//2
        self.rect.center = (100,altura-tam_player)
        self.is_jumping = False

    #Parte responsável pelo pulo do dinossauro. o pulo só é executado caso ele esteja no chão
    def jump(self):
        if not self.is_jumping and self.rect.y == self.pos_y_inicial:
            self.is_jumping = True
            self.dino_soundjump.play()
    def update(self):
        if self.is_jumping:
            if self.rect.y <= self.pos_y_inicial - altura_pulo:
                self.is_jumping = False
            self.rect.y -= intensidade_do_pulo
        else:
            if self.rect.y >= self.pos_y_inicial:
                self.rect.y = self.pos_y_inicial
            else:
                self.rect.y += intensidade_da_queda

        if self.posição_lista_dino > 2:
            self.posição_lista_dino = 0
        self.posição_lista_dino += 0.25
        self.image = self.imagem_dino[int(self.posição_lista_dino)]
class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32,0),(32,32))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50,200,50)
        self.rect.x = randrange(1360,2680,50)
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = randint(largura, largura*2)
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= velocidade_nuvens

class Piso(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.y = altura - tam_player
        self.rect.x = pos_x * tam_player

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= velocidade_piso
class Vilão_dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagem_dino = []
        for i in range(3, 5):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.imagem_dino.append(img)
        self.posição_lista_dino = 0
        self.image = self.imagem_dino[self.posição_lista_dino]
        self.mask = pygame.mask.from_surface(self.image)
        self.aleat = obstaculo_aleat
        self.rect = self.image.get_rect()
        self.rect.center = (largura, randint(min(player.pos_y_inicial, 587), max(player.pos_y_inicial, 430)))
        self.rect.x = largura

    def update(self):
        if self.aleat == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
                self.rect.y = randint((player.pos_y_inicial - altura_pulo), player.pos_y_inicial)
            else:
                self.rect.x -= velocidade_vilao

                if self.posição_lista_dino > 1:
                    self.posição_lista_dino = 0
                self.posição_lista_dino += 0.25
                self.image = self.imagem_dino[int(self.posição_lista_dino)]

class Cactos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5 * 32, 0), (32, 32))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.aleat = obstaculo_aleat
        self.rect.center = (largura,altura-tam_player)
        self.rect.x = largura
    def update(self):
        if self.aleat == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            self.rect.x -= velocidade_geral

todas_as_sprites = pygame.sprite.Group()
player = Player()
todas_as_sprites.add(player)

for j in range(qtd_nuvens):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

for k in range(largura*2//64):
    piso = Piso(k)
    todas_as_sprites.add(piso)

moeda = Moeda()
todas_as_sprites.add(moeda)
cacto = Cactos()
todas_as_sprites.add(cacto)
vilao_dino = Vilão_dino()
todas_as_sprites.add(vilao_dino)

obstaculos = pygame.sprite.Group()
obstaculos.add(vilao_dino)
obstaculos.add(cacto)

while gameloop:
    clock.tick(60)
    display.fill(cinza)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_w or event.key == K_UP:
                if player.rect.y != player.pos_y_inicial:
                    pass
                player.jump()

            if event.key == K_r and colidiu_cacto == False:
                pass
            if event.key == K_p:
                pausado = True
                while pausado:
                    jogo_pausado()
                    pontuação += 0
                    contador_pause += 1
                    if event.key == K_p and contador_pause % 2 != 0:
                        pausado = False
                restart()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if player.rect.y != player.pos_y_inicial:
                pass
            player.jump()

    todas_as_sprites.draw(display)
    colisão = pygame.sprite.spritecollide(player,obstaculos,False,pygame.sprite.collide_mask)
    colisao_moeda = pygame.sprite.spritecollide(player, [moeda], False)

    if vilao_dino.rect.topright[0] <= 0 or cacto.rect.topright[0] <= 0:
        obstaculo_aleat = choice([0,1])
        vilao_dino.rect.x = largura
        cacto.rect.x = largura
        vilao_dino.aleat = obstaculo_aleat
        cacto.aleat = obstaculo_aleat

    if colisão and colidiu_cacto == False:
        som_colisão.play()
        #linha provisória while o bug não for reparado ;)
        vidas -= 1
        if vidas < 1:
            mangover = mensagem(f'Você perdeu. fez {pontuação} pontos',40,vermelho)
            display.blit(mangover, (largura // 2, altura // 2))
            pygame.display.update()
            sleep(5)
            gameloop = False
        #era pra quando o jogo acabar ir pra uma tela de gameover
        colidiu_cacto == True

    if colidiu_cacto == True:
        mengover = mensagem(f'Você perdeu. fez {pontuação} pontos',40,vermelho)
        display.blit(mengover,(largura//2,altura//2))
        mensrestart = mensagem('Pressione R para reiniciar',20,preto)
        display.blit(mensrestart,(largura//2,altura//2+120))
    else:
        if pausado == False:
            pontuação += 1
        retorno_função_pontuação = mensagem(pontuação,40,preto)
        msg_moeda = mensagem(f'coins {moedas}',40,amarelo)
        todas_as_sprites.update()
        msg_vidas = mensagem(f'Life {vidas}',40,vermelho)
        if velocidade_geral == max_vel:
            velocidade_geral += 0
            velocidade_vilao += 0
        else:
            if pontuação % 250 == 0:
                velocidade_geral += 1
                velocidade_vilao += 1
                som_pontos.play()
            if colisao_moeda:
                som_moeda.play()
                moedas += 1
                if moedas > 10:
                    vidas += moedas
                    moedas = 0
                moeda.rect.x = randint(largura, largura * 2)
                moeda.rect.y = randrange(player.pos_y_inicial, altura - tam_player, 50)

    display.blit(retorno_função_pontuação,(largura - 80,30))
    display.blit(msg_moeda,(largura-240,30))
    display.blit(msg_vidas, (largura - 400, 30))
    pygame.display.flip()
