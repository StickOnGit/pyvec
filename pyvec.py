import pygame
import sys
import random
import vecview as vview
import math
import time
import shapef

from zpt import Zpt
from wireframe import Wireframe
from multiframe import Multiframe
from starbg import star_bg


pygame.init()

FPS = 60
FPSCLOCK = pygame.time.Clock()

TRANSUNIT = vview.DEPTH / (FPS * 2)
SPINUNIT = (2 * 3.14159) / (FPS * 2)

		
vview.set_hzpt((vview.WIDTH/2, vview.HEIGHT/2))

def prism(x, y, z):
	return [Zpt(x, y, z), Zpt(x+15, y+15, z), Zpt(x-15, y+15, z), 
		Zpt(x, y, z+30), Zpt(x+15, y+15, z+30), Zpt(x-15, y+15, z+30)]

def shot_shape(x, y, z):
	return [Zpt(x, y, z), Zpt(x-10, y, z+35), Zpt(x, y, z+45), Zpt(x+10, y, z+35), Zpt(x, y-10, z+35)]
	
def wing(x, y, z, scale=1):
	return [Zpt(x, y, z),
			Zpt((x+80)*scale, (y+40)*scale, (z+100)*scale),
			Zpt(x, (y+40)*scale, (z+100)*scale),
			Zpt((x+80)*scale, (y+40)*scale, (z+150)*scale)]
	
def mf_shot(x, y, z):
	shotshape = Wireframe(zpts=shot_shape(x, y, z), color=(130, 50, 130))
	shotshape.set_lines((0, 1, 2, 3), True)
	shotshape.set_lines((0, 4, 2), False)
	shotshape.set_lines((1, 4, 3), False)
	new_shot = Multiframe(wfs=(shotshape))
	return new_shot
	
def objs_might_hit(obj1, obj2):
	"""Uses distance-squared to see if two objects are at least as close as
	the radius of their furthest-from-center points. Returns True or False."""
	p1, p2 = obj1.ctr, obj2.ctr
	dist = abs(p1.x - p2.x)**2 + abs(p1.y - p2.y)**2 + abs(p1.z - p2.z)**2
	if dist > obj1.zradius + obj2.zradius:
		return False
	else:
		return True
		
	
		
zpyr = [Zpt(300, 300, 300), Zpt(320, 320, 280), Zpt(280, 320, 230), Zpt(300, 320, 320)]

def pymd(x, y, z, lng=30):
	unit = lng / 1.4142135623730951		#sqrt(2). 
	return [Zpt(x+unit, y+unit, z+unit), 
			Zpt(x-unit, y-unit, z+unit), 
			Zpt(x-unit, y+unit, z-unit), 
			Zpt(x+unit, y-unit, z-unit)]
			
def pymd2(x, y, z, lng=30):
	unit = lng / 1.4142135623730951		#sqrt(2). 
	return [Zpt(x+unit, y+unit, z+unit), 
			Zpt(x-unit, y-unit, z+unit), 
			Zpt(x-unit, y+unit, z-unit), 
			Zpt(x+unit, y-unit, z-unit)]
	
def fancy(x, y, z, lng=30):
	tri = math.sqrt(3)
	return [Zpt(x,			y,					z - math.sqrt(lng**2/tri**2) ), 
			Zpt(x,			y+tri-((lng/2)/tri),	z), 
			Zpt(x-(lng/2),	y+((lng/2)/tri),	z), 
			Zpt(x+(lng/2),	y+((lng/2)/tri),	z)]

zarena = [Zpt(0, 0, 0), Zpt(vview.WIDTH, 0, 0), Zpt(vview.WIDTH, vview.HEIGHT, 0), Zpt(0, vview.HEIGHT, 0),
		Zpt(0, 0, vview.DEPTH), Zpt(vview.WIDTH, 0, vview.DEPTH), Zpt(vview.WIDTH, vview.HEIGHT, vview.DEPTH), Zpt(0, vview.HEIGHT, vview.DEPTH)]


GUY = shapef.cube(500, 0, 300)
GUYTWO = shapef.cube(650, 0, 300)

GUYTHR = Wireframe(zpts=wing(60, 60, 60, 1.5), color=(50, 80, 50))
GUYTHR.set_lines((0, 1, 2))
GUYTHR.set_lines((1, 2, 3))
GUYTHR.set_line(0, 3)

playerObj = Multiframe(wfs=(GUY, GUYTWO))

def engine_flare(obj, func):
	def inner(*args, **kwargs):
		obj.color = (random.randrange(150, 220),random.randrange(30, 180),random.randrange(50, 60))
		return func(*args, **kwargs)
	return inner
	
def shot_behavior(shotobj, func):
	def inner(*args, **kwargs):
		for frame in shotobj.frames:
			frame.color = (random.randrange(30, 200),random.randrange(30, 200),random.randrange(30, 200))
		if shotobj.ctr.z > vview.DEPTH * 2 or shotobj.ctr.z < vview.CAM_PT.z:
			shotobj.kill()
		return func(*args, **kwargs)
	return inner
	
def bounce(badobj, func):
	def inner(*args, **kwargs):
		if (not 0 < badobj.ctr.x < vview.WIDTH):
			badobj.xtrans *= -1
		if (not 0 < badobj.ctr.y < vview.HEIGHT):
			badobj.ytrans *= -1
		if (not 0 < badobj.ctr.z < vview.DEPTH):
			badobj.ztrans *= -1
		return func(*args, **kwargs)
	return inner
	
def insta_kill(obj, func):
	def inner(*args, **kwargs):
		obj.kill()
		return func(*args, **kwargs)
	return inner
	
def quick_kill(obj, func):
	def inner(*args, **kwargs):
		obj.color = (255-quick_kill.counter, 0, 0)
		quick_kill.counter += 4
		if quick_kill.counter > 250:
			obj.kill()
		return func(*args, **kwargs)
	obj.color = (255, 0, 0)
	quick_kill.counter = 0
	return inner
	
def rotor(obj, func, radians=0, ignore='x'):
	def inner(*args, **kwargs):
		obj.good_rotate(radians, ignore)
		return func(*args, **kwargs)
	return inner
	

playerObj.frames[1].update = rotor(playerObj.frames[1], playerObj.frames[1].update, .2, 'y')
for frame in playerObj.frames:
	frame.update = engine_flare(frame, frame.update)

BAD_GUY = Wireframe(zpts=pymd(500, 250, 200, 30), color=(40, 40, 140))
BAD_GUY.set_lines((0, 1, 2))
BAD_GUY.set_lines((2, 3, 1), False)
BAD_GUY.set_line(0, 3)
badObj = Multiframe(wfs=BAD_GUY)

badObj.yspin = 2 * SPINUNIT

BAD_TWO = Wireframe(zpts=prism(400, 100, 10), color=(150, 150, 20))
BAD_TWO.set_lines((0, 1, 2))
BAD_TWO.set_lines((3, 4, 5))
BAD_TWO.set_line(0, 3)
BAD_TWO.set_line(1, 4)
BAD_TWO.set_line(2, 5)
badObjTwo = Multiframe(wfs=BAD_TWO)

#badObjTwo.xtrans = 5
#badObjTwo.ytrans = 10
badObjTwo.ztrans = 7

badObjTwo.update = bounce(badObjTwo, badObjTwo.update)

#ARENA = Wireframe(zpts=zarena, color=(128, 128, 128), width=1)
#ARENA.set_shape(0, 1, 2, 3)
#ARENA.set_shape(4, 5, 6, 7)
#ARENA.set_shape(0, 4, 5, 1)
#ARENA.set_shape(3, 7, 6, 2)
#ARENA.set_shape(0, 4, 7, 3)
#ARENA.set_shape(1, 5, 6, 2)

ALLQ = pygame.sprite.Group()
GOODQ = pygame.sprite.Group()
BADQ = pygame.sprite.Group()
BGQ = pygame.sprite.Group()
DRAWQ = pygame.sprite.Group()

def good_visible(*objs):
	"""Adds object to 'good queue' and 'everything queue' for the purposes
	of collisions and updating."""
	GOODQ.add(objs)
	ALLQ.add(objs)
	for obj in objs:
		to_draw_q(obj)

def bad_visible(*objs):
	"""Adds object to 'bad queue' and 'everything queue' for the purposes
	of collisions and updating."""
	BADQ.add(objs)
	ALLQ.add(objs)
	for obj in objs:
		to_draw_q(obj)

def only_visible(*objs):
	"""Adds an object to the 'everything queue' so it will be updated,
	then adds it to the 'drawing queue' for drawing. Neither of these
	are used for collisions so this should just cause them to appear."""
	ALLQ.add(objs)
	for obj in objs:
		to_draw_q(obj)
	
def to_draw_q(obj):
	"""hasattr() is used to see if it has 'frames' attribute; if not, 
	it assumes it is a Wireframe object. 
	Wireframe objects are the only things drawn in DRAWQ."""
	if hasattr(obj, 'frames'):
		DRAWQ.add(obj.frames)
	else:
		DRAWQ.add(obj)

good_visible(playerObj)
bad_visible(badObj, badObjTwo)
only_visible(star_bg())

def main():
	last_fps = FPS
	time_till_fps = 0
	looping = True
	pygame.mouse.set_pos(vview.WIDTH/2, vview.HEIGHT/2)
	while looping:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				looping = False
			elif event.type == pygame.MOUSEMOTION:
				nX, nY = pygame.mouse.get_pos()
				playerObj.d_move((nX - playerObj.ctr.x), (nY - playerObj.ctr.y))
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					playerObj.ztrans += TRANSUNIT
				elif event.key == pygame.K_s:
					playerObj.ztrans -= TRANSUNIT
				elif event.key == pygame.K_d:
					playerObj.yspin += SPINUNIT
				elif event.key == pygame.K_a:
					playerObj.yspin -= SPINUNIT
				elif event.key == pygame.K_e:
					playerObj.xspin += SPINUNIT
				elif event.key == pygame.K_q:
					playerObj.xspin -= SPINUNIT
				elif event.key == pygame.K_c:
					playerObj.zspin += SPINUNIT
				elif event.key == pygame.K_z:
					playerObj.zspin -= SPINUNIT
			elif event.type == pygame.MOUSEBUTTONDOWN:
				newShot = mf_shot(playerObj.ctr.x, playerObj.ctr.y, playerObj.ctr.z)
				newShot.ztrans = 30
				newShot.update = shot_behavior(newShot, newShot.update)
				good_visible(newShot)

		ALLQ.update()
		for obj in GOODQ:
			###check to see if any zpt.zs are in the same range
			###if so, create hit-boxes from minmax pt range and check again
			#good_hit_list = obj.find_minmax()
			try:
				obj.checked -= 1
			except AttributeError:
				obj.checked = 0
			if obj.checked > 0:
				continue
			for badobj in BADQ:
				if objs_might_hit(obj, badobj):
					hit_o = shapef.octah(badobj.ctr.x, badobj.ctr.y, badobj.ctr.z)
					hit_o.update = quick_kill(hit_o, hit_o.update)
					hit_p = shapef.octah(obj.ctr.x, obj.ctr.y, obj.ctr.z)
					hit_p.update = quick_kill(hit_p, hit_p.update)
					only_visible(hit_o, hit_p)
					pass
				else:
					obj.checked = 3
				#	zmin, zmax = good_hit_list[2][0], good_hit_list[2][1]
				#	if zmin <= badzpt.z <= zmax:
				#		xpts, ypts = good_hit_list[0], good_hit_list[1]
				#		goodXYRect = pygame.Rect(xpts[0], ypts[0], xpts[1] - xpts[0], ypts[1] - ypts[0])
				#		badXYpt = badzpt.x, badzpt.y
				#		if goodXYRect.collidepoint(badXYpt):
				#			badobj.color = (random.randrange(30, 200),
				#							random.randrange(30, 200),
				#							random.randrange(30, 200))
				#			print "boom at (%d, %d, %d)" % badzpt.as_t()
		
		vview.wipe()
		vview.drawq_draw(DRAWQ)
		vview.flip()
		
		if time_till_fps < 0:
			new_fps = FPSCLOCK.get_fps()
			if new_fps != last_fps:
				last_fps = (new_fps + last_fps) / 2
				pygame.display.set_caption("%d" % last_fps)
				
			time_till_fps = FPS * 2
		time_till_fps -= 1
		FPSCLOCK.tick(FPS)

if __name__ == "__main__":
	main()
	print "--Exit--"
	pygame.quit()
	sys.exit()
