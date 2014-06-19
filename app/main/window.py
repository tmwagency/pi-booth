import pygame

class WindowView(object):
	
	def __init__(self):
		pygame.init() 

		global count
		global last_count_time

		#pygame config
		BLACK = (0, 0, 0)
		WHITE = (255, 255, 255)
		RED = (255, 0, 0)
		GREEN = (0, 255, 0)
		BLUE = (0, 0, 255)
		basicFont = pygame.font.SysFont(None, 228)

		count = 4
		last_count_time = 0

		infoObject = pygame.display.Info()
	
	def init(self):
		print ("------------------opening window")
		window = pygame.display.set_mode((640, 480))
		pygame.display.set_caption('Hello world!')
		
	'''
	def loop():

		window.fill(WHITE)
		if count == 0:
			pass
		elif time.time() - last_count_time >= 1:
			count = count - 1
			last_count_time = time.time()
		#draw text
		text = basicFont.render(str(count), True, BLACK)
		textRect = text.get_rect()
		textRect.left = (window.get_rect().centerx - 200)
		textRect.centery = window.get_rect().centery
		
		window.blit(text, textRect)

		#draw it to the screen
		pygame.display.flip() 

	def my_quit():
		pygame.quit
		sys.exit(0)

	#input handling (somewhat boilerplate code):
	while True:

		loop()
		
		for event in pygame.event.get(): 
				
			if (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT :
				my_quit()
				
			if (event.type is pygame.KEYDOWN and event.key == pygame.K_f):
				if window.get_flags() & pygame.FULLSCREEN:
					pygame.display.set_mode((640, 480))
					#loop()
				else:
					pygame.display.set_mode((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN) 
					#loop()
	'''