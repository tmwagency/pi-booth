import pygame
import time, sys

class WindowView(object):
	
	def __init__(self, caption):
		
		self.caption = caption;	
		pygame.init()

		self.window = pygame.display.set_mode((640, 480))
		pygame.display.set_caption(caption)
		
		''' pygame variables '''
		self.TXT = (0, 0, 0)
		self.BG = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 228)
		
		background = pygame.Surface(self.window.get_size())
		background = background.convert()
		background.fill(self.BG)
		
		last_count_time = 0
		
		self.count = 4
		
		self.infoObject = pygame.display.Info()

		print ("------------------opening window")
		self.main(self.window, self.count)
		#window = pygame.display.set_mode((1024, 600),pygame.FULLSCREEN)
		
		
	class CountDown:
		
		def __init__(self, duration, x_pos, y_pos):
			self.duration = duration
			self.x_pos = x_pos
			self.y_pos = y_pos
			
		def start(self):
			return
				
		def update(self):
			return
			
		def draw(self, surface):
			return
			
			
	def main(self, window, count):
		
		last_count_time = 0
		running = True
		
		while running:
			delay(0.1)
			''' if no events are happening then
			display the idle Welcome screen. '''
			
			''' Handle events '''
			for event in pygame.event.get(): 
				
				print("pygame got event-----> ", event)
				if (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT :
					self.my_quit()
					
				if (event.type is pygame.KEYDOWN and event.key == pygame.K_f):
					if window.get_flags() & pygame.FULLSCREEN:
						pygame.display.set_mode((640, 480))

					else:
						pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h), pygame.FULLSCREEN) 


			window.fill(self.BG)
			
			if count == 0:
				pass
			elif time.time() - last_count_time >= 1:
				count = count - 1
				last_count_time = time.time()
				
			#draw text
			text = self.font.render(str(count), True, self.TXT)
			textpos = text.get_rect()
			textpos.left = (window.get_rect().centerx - 200)
			textpos.centery = window.get_rect().centery
			
			window.blit(text, textpos)

			#draw it to the screen
			pygame.display.flip() 


	def my_quit(self):
		pygame.quit
		sys.exit(0)
	




			
			

