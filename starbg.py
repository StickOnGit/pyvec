from multiframe import Multiframe
from wireframe import Wireframe
from zpt import Zpt
from vecview import PAD, PAD_H, PAD_W, PAD_D, PAD_C
import random
import pygame

starx2 = range((0 - PAD), 5) + range((PAD_W - PAD + 5), PAD_W)
stary2 = range((0 - PAD), 5) + range((PAD_H - PAD + 5), PAD_H)
starx = range(0, PAD_W)
stary = range(0, PAD_H)
starz = range(int(PAD_C), int(PAD_D * 2))

rnd = random.randrange

def smallx():
	return (random.choice(starx2), random.choice(stary))

def smally():
	return (random.choice(starx), random.choice(stary2))
	
def x_or_y():
	if random.choice((True, False)):
		newx, newy = smallx()
	else:
		newx, newy = smally()
	return newx, newy

def star_update(obj, func):
	def inner(*args, **kwargs):
		if obj.ctr.z < PAD_C:
			newx, newy = x_or_y()
			newz = PAD_D
			obj.frames[0].zpts[0].x = newx
			obj.frames[0].zpts[0].y = newy
			obj.frames[0].zpts[0].z = newz
			
			obj.frames[0].zpts[1].x = newx
			obj.frames[0].zpts[1].y = newy
			obj.frames[0].zpts[1].z = newz + 30
			obj.frames[0].own_ctr()
			obj.set_ctr()
		return func(*args, **kwargs)
	return inner
	
def star_line_update(obj, func):
	def inner(*args, **kwargs):
		obj.delta_move(0, 0, obj.ztrans)
		if obj.center.z < PAD_C:
			newz = PAD_D * 2
			newx, newy = x_or_y()
			obj.zpts[0].x = newx
			obj.zpts[0].y = newy
			obj.zpts[0].z = newz
			
			obj.zpts[1].x = newx
			obj.zpts[1].y = newy
			obj.zpts[1].z = newz + (obj.ztrans * 1.5)
		obj.own_ctr()
		return func(*args, **kwargs)
	return inner


def star_bg(speed=30):
	starlist = []
	for i in range(0, 40):
		newx, newy = x_or_y()
		newz = random.choice(starz)
		star_wf = Wireframe(zpts=(Zpt(newx, newy, newz), Zpt(newx, newy, newz + (speed*1.5))), width=1)
		star_wf.set_line(0, 1)
		star_wf.ztrans = -speed
		star_wf.update = star_line_update(star_wf, star_wf.update)
		starlist.append(star_wf)
	return starlist
	
