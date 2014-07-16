import pygame
import pygame.gfxdraw
import time, sys, math
import config

class WindowView(object):
	
	def __init__(self, caption):
		
		self.caption = caption;	
		pygame.init()

		self.window = pygame.display.set_mode((640, 480))
		pygame.display.set_caption(caption)
		
		''' pygame variables '''
		#self.TXT = (0, 0, 0)
		self.BG = (0, 0, 0)
		
		self.FPS = 30
		self.clock = pygame.time.Clock()
		
		background = pygame.Surface(self.window.get_size())
		background = background.convert()
		background.fill(self.BG)
		
		
		self.infoObject = pygame.display.Info()

		print ("------------------opening window")
		self.main(self.window)
		#window = pygame.display.set_mode((1024, 600),pygame.FULLSCREEN)
		
	class ScreenText:
		
		def __init__(self, window, pos_x, pos_y, text, delay_between_lines=6, loop=False, delay_before_restart=12):
			lines = config.text
			lines = [x.strip for x in lines.split('|')]
			print "---> text init: ", lines
			
			self.font = pygame.font.SysFont(None, 28)
			self.pos_x = pos_x
			self.pos_y = pos_y
			
			
		def update(self):
			return
			
		def draw(self):
			
			textpos = text.get_rect()
			textpos.left = x_pos
			textpos.centery = y_pos
			text = self.font.render(str(count), True, (250,250,250))
			
			window.blit(text, textpos)
			

			
		
	class CountDown:
		
		def __init__(self, window, duration):
			
			self.window = window
			self.constduration = duration
			self.count = duration
			self.x_pos = (window.get_rect().centerx - 300)
			self.y_pos = window.get_rect().centery
			self.last_count_time = 0
			self.font = pygame.font.SysFont(None, 228)
			self.arcstart = 0
			self.arcend = 0

			
			
		def reset(self):
			self.count = self.constduration
				
		def update(self):
			
			count = self.count
			last_count_time = self.last_count_time
			
			if count == 0:
				# fire count finished event?
				pass
				
			elif time.time() - last_count_time >= 1:
				print last_count_time
				self.count = count - 1
				self.last_count_time = time.time()

		def draw(self):
			
			window = self.window
			x_pos=self.x_pos
			y_pos=self.y_pos
			
			arcstart = self.arcstart
			arcend = self.arcend
			
			count = self.count
			text = self.font.render(str(count), True, (250,250,250))
			
			textpos = text.get_rect()
			textpos.left = x_pos
			textpos.centery = y_pos
			
			window.blit(text, textpos)
			
			
	def main(self, window):
		''' The main loop '''
		countdown = self.CountDown(window, 5)
		
		last_count_time = 0
		running = True
		
		while running:
			pygame.time.delay(2)
			''' if no events are happening then
			display the idle Welcome screen. '''
			
			''' Handle events '''
			for event in pygame.event.get(): 
				
				#print("pygame got event-----> ", event)
				if (event.type is pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT :
					self.my_quit()
					
				if (event.type is pygame.KEYDOWN and event.key == pygame.K_f):
					if window.get_flags() & pygame.FULLSCREEN:
						pygame.display.set_mode((640, 480))

					else:
						pygame.display.set_mode((self.infoObject.current_w, self.infoObject.current_h), pygame.FULLSCREEN) 

			self.clock.tick(self.FPS)
			
			window.fill(self.BG)
			
			countdown.update()
			countdown.draw()

			'''
			if do_countdown is True:
				countdown.update()
				countdown.draw()
			
			if do_welcome is True:
				welcome.update()
				welcome.draw()
			'''
				
			#draw text
			
			


			#draw it to the screen
			pygame.display.flip() 


	def my_quit(self):
		pygame.quit
		sys.exit(0)
	
if __name__ == '__main__':
	window = WindowView('Testing')
	main()
