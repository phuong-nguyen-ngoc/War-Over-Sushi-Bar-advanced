#Phuong Nguyen Ngoc, Elliot Zhou, Zixuan Wang, Eduardo Sosa, Katie Andre
#CS269
from common_setting import *
from bullet import Bullet
import pygame as pg
import time

class Chef(pg.sprite.Sprite):
	#the official constructor is __init__(self, x, y, color, enemy)
	def __init__(self, x, y, character, left_keyboard, bullet_group, sprite_group, superbullet_group, block_group):
		pg.sprite.Sprite.__init__(self)
		#self.image = pg.Surface((40,40))
		#self.image.fill(YELLOW)
		self.image = pg.image.load(character[0]).convert()
		self.image.set_colorkey(BLACK)
		self.rect = pg.Rect(0, 0, 30, 30)
		self.rect.center = (120+40*x,220+40*y)
		self.character = character
		self.bullet_group = bullet_group
		self.sprite_group = sprite_group
		self.block_group = block_group
		self.superbullet_group = superbullet_group
		self.left_keyboard = left_keyboard
		self.dir = "up"

		self.start = time.time()
		self.end = time.time()

		self.point = 0
		self.walk_count = -1 #this serves the animation, we're gonna store the animation in a list
		self.life = 2
		self.cabbage = 40
		self.sound = None
		self.superbullet = 0
		self.speed = False
		
		self.light = False
		self.stLight = time.time()
		self.endLight = time.time()

		self.releaseSpace = True



	def update(self):
	 #these lines make sure the speed up bonus lasts for limited time
		events = pg.event.get()
		if len(events)>0:
			event = (events[0])
			#print(event.type)
			if event.type == pg.KEYDOWN:
				print("down")

		if self.speed == True:
			self.end = time.time()
			elapsed = self.end - self.start
			if elapsed >= 5.00:
				self.speed = False
		self.image.set_colorkey(BLACK)
		
		# if self.left_keyboard:
		# 	key = pg.key.get_pressed()
		# 	if key[pg.K_LEFT]:
		# 		#time.sleep(0.03)
		# 		self.move_left()
		# 	elif key[pg.K_RIGHT]:
		# 		#time.sleep(0.03)
		# 		self.move_right()
		# 	elif key[pg.K_UP]:
		# 		#time.sleep(0.03)
		# 		self.move_forward()
		# 	elif key[pg.K_DOWN]:
		# 		#time.sleep(0.03)
		# 		self.move_backward()
		# 	elif key[pg.K_SPACE]:
		# 		#time.sleep(0.03)
		# 		if self.releaseSpace:
		# 			self.shoot()
		# 			#time.sleep(0.05)
		# 			self.releaseSpace = False
		# 	else:
		# 		self.releaseSpace = True

	
	def move_left(self):
		old_x = self.get_x()
		old_y = self.get_y()
		#self.walk_count = 0
		if not self.dir == 'left':
			self.dir = "left"
			self.walk_count = -1
		self.walk_count += 1
		if self.walk_count == 3:
			self.walk_count = -1
		self.image =  pg.image.load(self.character[1][self.walk_count]).convert()
		self.image.set_colorkey(BLACK)
		if self.speed:
			self.rect.x -=20
		else:			
			self.rect.x -= 8
		#check boundary
		if self.rect.left < 100:
			self.rect.left = 100
		chef_collide_block = pg.sprite.spritecollide(self, self.block_group, False)
		if chef_collide_block:
			self.set_x(old_x)
			self.set_y(old_y)
		self.sound = pg.mixer.Sound('newwalk.wav')
		#also need to update the image
	
	def move_right(self):
		old_x = self.get_x()
		old_y = self.get_y()
		#self.walk_count = 0
		if not self.dir == 'right':
			self.dir = "right"
			self.walk_count = -1
		self.walk_count += 1
		if self.walk_count == 3:
			self.walk_count = -1
		self.image =  pg.image.load(self.character[2][self.walk_count]).convert()
		self.image.set_colorkey(BLACK)
		if self.speed:
			self.rect.x +=20
		else:	 
			self.rect.x += 8
		if self.rect.right > 900:
			self.rect.right = 900
		chef_collide_block = pg.sprite.spritecollide(self, self.block_group, False)
		if chef_collide_block:
			self.set_x(old_x)
			self.set_y(old_y)
		self.sound = pg.mixer.Sound('newwalk.wav')

	def move_backward(self):
		old_x = self.get_x()
		old_y = self.get_y()
		if not self.dir == 'down':
			self.dir = "down"
			self.walk_count = -1
		self.walk_count += 1
		if self.walk_count == 1:
			self.walk_count = -1
		self.image =  pg.image.load(self.character[4][self.walk_count]).convert()
		self.image.set_colorkey(BLACK)
		if self.speed:
			self.rect.y +=20
		else:		
			self.rect.y += 8
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		chef_collide_block = pg.sprite.spritecollide(self, self.block_group, False)
		if chef_collide_block:
			self.set_x(old_x)
			self.set_y(old_y)
		self.sound = pg.mixer.Sound('newwalk.wav')

	def move_forward(self):
		old_x = self.get_x()
		old_y = self.get_y()
		if not self.dir == 'up':
			self.dir = "up"
			self.walk_count = -1
		self.walk_count += 1
		if self.walk_count == 2:
			self.walk_count = -1
		self.image =  pg.image.load(self.character[3][self.walk_count]).convert()
		self.image.set_colorkey(BLACK)
		self.dir = "up"
		if self.speed:
			self.rect.y -=20
		else:		
			self.rect.y -= 8
		if self.rect.top < 200:
			self.rect.top = 200
		chef_collide_block = pg.sprite.spritecollide(self, self.block_group, False)
		if chef_collide_block:
			self.set_x(old_x)
			self.set_y(old_y)
		self.sound = pg.mixer.Sound('newwalk.wav')
	
	def shoot(self):

		if self.superbullet > 0:
			self.superbullet -=1
			bullet2 = Bullet(self.dir, self.rect.center, True)
			self.superbullet_group.add(bullet2)
			self.sprite_group.add(bullet2)

		if self.cabbage > 0:
			print(self.cabbage)
			self.cabbage -= 1
			bullet1 = Bullet(self.dir, self.rect.center)
			self.bullet_group.add(bullet1)
			self.sprite_group.add(bullet1)	
			
	def get_x(self):
		return self.rect.x

	def get_y(self):
		return self.rect.y

	def get_center(self):
		return self.rect.center

	def set_x(self, x):
		self.rect.x = x

	def set_y(self, y):
		self.rect.y = y

	def get_dir(self):
		return self.dir

	def is_hit(self):
		self.life -= 1
		print(self.life)
	
	def claim_life(self):
		self.life += 1
		print(self.life)

	def claim_point(self):
		self.point += 1
		print(self.point)

	def claim_cabbage(self):
		self.cabbage += 5
	
	def claim_superbullet(self):
		self.superbullet +=1
	
	def get_life(self):
		return self.life

	def set_life(self, life):
		self.life = life

	def get_all_bullets(self):
		return self.all_bullets

	def is_dead(self):
		if self.life <= 0:
			return True
		else:
			return False
	def set_dead(self):
		self.life = 0
	
	def get_point(self):
		return self.point
	
	def set_point(self, point):
		self.point = point


	def get_cabbage(self):
		return self.cabbage
	
	def set_cabbage(self, cab):
		self.cabbage = cab
	
	def gainSpeed(self):
		self.start = time.time()
		self.speed = True
	
	def close_speed(self):
		self.speed = False
	
	def get_superbullet(self):
		return self.superbullet
	
	def get_speed(self):
		return self.speed
	
	def gainLight(self):
		self.stLight =time.time()
		self.light = True
	
	def get_Light(self):
		return self.light
	
	def get_stLight(self):
		return self.stLight
	
	def get_endLight(self):
		return self.endLight
	
	def set_endLight(self):
		self.endLight= time.time()

	def close_Light(self):
		self.light= False
	
	def get_stSpeed(self):
		return self.start
	
	def get_endSpeed(self):
		return self.end

	def set_endSpeed(self):
		self.end= time.time()

	def set_center(self, x, y):
		self.rect.center = (120+40*x,220+40*y)

	def set_block_group(self, block_group):
		self.block_group = block_group

	

