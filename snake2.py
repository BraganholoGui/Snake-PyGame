import pygame as pg
from random import randint

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZA = (128, 128, 128)
AMARELO = (255, 255, 0)

def main():
	def morte(loop):
		return False

	pg.init()
	clock = pg.time.Clock()
	#pg.display.set_caption("Snake")
	pg.mouse.set_visible(False)
	scrinfo = pg.display.Info()
	rh, rv = scrinfo.current_w, scrinfo.current_h
	screen = pg.display.set_mode((rh, rv), flags=pg.FULLSCREEN)
    
    #carregar recursos
	pg.mixer.music.load("music.mp3")
	pg.mixer.music.set_volume(0.0)
	pg.mixer.music.play(loops=-1)
	som_alimento = pg.mixer.Sound("alimento.wav")
    
	snake = [[rh / 2, rv / 2]]  # corpo da snake
	sx, sy = 0, 0  # sentido horizontal e vertical
	tam = 1  # tamanho da snake
	aum = 0  # aumento de partes da snake
	ali = (randint(32, rh - 32), randint(32, rv - 32))
	loop = True
	while loop:
		screen.fill(CINZA)
		for ev in pg.event.get():
			if ev.type == pg.QUIT:
				loop = False
				
		# captura das teclas
		tecla = pg.key.get_pressed()
		if tecla[pg.K_ESCAPE]:  # sair do jogo
			loop = False
		# controle da direção da snake
		if tecla[pg.K_LEFT]:
			sx, sy = -1, 0
		if tecla[pg.K_RIGHT]:
			sx, sy = 1, 0
		if tecla[pg.K_UP]:
			sx, sy = 0, -1
		if tecla[pg.K_DOWN]:
			sx, sy = 0, 1
		
		# colisão com o alimento
		if snake[0][0] >= ali[0] - 10 and snake[0][0] <= ali[0] + 10 and \
		   	snake[0][1] >= ali[1] - 10 and snake[0][1] <= ali[1] + 10:
				som_alimento.play()	
				aum += 10
				ali = (randint(32, rh - 32), randint(32, rv - 32))
		if aum > 0:
			aum -= 1
			tam += 1
			snake.append(0)
			
		# movimentar snake
		for i in range(tam - 1, 0, -1):
			snake[i] = snake[i - 1].copy()
		snake[0][0] += sx * 4  # movimento horizontal (x)
		snake[0][1] += sy * 4  # movimento vertical (y)

		# passagens laterais
		if snake[0][1] > rv / 2 - 18 and snake[0][1] < rv / 2 + 18:
			if snake[0][0] > rh + 22:
				snake[0][0] = -22
			elif snake[0][0] < -22:
				snake[0][0] = rh + 22
		else: 	#Colisao nas bordas
			if snake[0][0] < 32 or snake[0][0] > rh -32 or \
				snake[0][1] < 32 or snake[0][1] >rv -32:
					loop = morte()



		# desenhar bordas
		pg.draw.rect(screen, PRETO, (20, 20, rh-20, 5))#sombra
		pg.draw.rect(screen, PRETO, (rh -16, rv/2-24, 20, 5))#sombra
		pg.draw.rect(screen, AZUL, (0, 0, rh, 20))
		pg.draw.rect(screen, AZUL, (0, rv - 20, rh, 20))
		pg.draw.rect(screen, PRETO, (3, 20, 23, rv / 2 - 38)) #sombra
		pg.draw.rect(screen, PRETO, (3, rv /2+31, 23, rv / 2 - 50)) #sombra
		pg.draw.rect(screen, AZUL, (0, 0, 20, rv / 2 - 24))
		pg.draw.rect(screen, AZUL, (0, rv / 2 + 24, 20, rv))
		pg.draw.rect(screen, AZUL, (rh - 20, 0, 20, rv / 2 - 24))
		pg.draw.rect(screen, AZUL, (rh - 20, rv / 2 + 24, 20, rv))

		# desenhar alimento
		sombra = (ali[0] + 3, ali[1] + 4)
		pg.draw.circle(screen, PRETO, sombra, 8)
		pg.draw.circle(screen, VERDE, ali, 8)

		# desenhar snake
		for i in range(tam):
			sombra = (snake[i][0] + 3, snake[i][1] + 4)
			pg.draw.circle(screen, PRETO, sombra, 12)
		for i in range(tam):
			pg.draw.circle(screen, AMARELO, snake[i], 12)
		if sx == 0 and sy == 0:  # parado
			pg.draw.circle(screen, PRETO, (snake[0][0] - 5, snake[0][1] - 3), 5)
			pg.draw.circle(screen, PRETO, (snake[0][0] + 5, snake[0][1] - 3), 5)
		elif sy == 0:  # movimento horizontal
			pg.draw.circle(screen, PRETO, (snake[0][0] + sx * 3, snake[0][1] - 2), 5)
		else:  # movimento vertical
			pg.draw.circle(screen, PRETO, (snake[0][0] - 5, snake[0][1] + sy * 3), 5)
			pg.draw.circle(screen, PRETO, (snake[0][0] + 5, snake[0][1] + sy * 3), 5)
		
		pg.display.flip()
		clock.tick(60)
	pg.quit()

main()
