import pygame
import time, sys

class WindowView(object):
	
	def __init__(self, caption):
		
		self.caption = caption;
		
		pygame.init()
		
		
		self.window = pygame.display.set_mode((640, 480))
		pygame.display.set_caption(caption)
		
		''' pygame variables '''
		self.BLACK = (0, 0, 0)
		self.WHITE = (255, 255, 255)
		self.basicFont = pygame.font.SysFont(None, 228)
		
		background = pygame.Surface(self.window.get_size())
		background = background.convert()
		self.window.fill(self.WHITE)
		
		count = 5
		last_count_time = 0

		#pygame config
		self.count = 4
		

		self.infoObject = pygame.display.Info()

		print ("------------------opening window")
		self.loop(self.window, self.count)
		#window = pygame.display.set_mode((1024, 600),pygame.FULLSCREEN)

	def loop(self, window, count):
		
		last_count_time = 0
		running = True
		while running:

			window.fill(self.WHITE)
			if count == 0:
				pass
			elif time.time() - last_count_time >= 1:
				count = count - 1
				last_count_time = time.time()
			#draw text
			text = self.basicFont.render(str(count), True, self.BLACK)
			textRect = text.get_rect()
			textRect.left = (window.get_rect().centerx - 200)
			textRect.centery = window.get_rect().centery
			
			window.blit(text, textRect)

			#draw it to the screen
			pygame.display.flip() 
			
			''' Handle events '''
			for event in pygame.event.get(): 
					
				if (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT :
					self.my_quit()
					
				if (event.type is pygame.KEYDOWN and event.key == pygame.K_f):
					if window.get_flags() & pygame.FULLSCREEN:
						pygame.display.set_mode((640, 480))
						#loop()
					else:
						pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h), pygame.FULLSCREEN) 
						#loop()

	def my_quit(self):
		pygame.quit
		sys.exit(0)
	




			
			

