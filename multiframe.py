import pygame
import math
from zpt import Zpt
from wireframe import Wireframe as Wf

class Multiframe(pygame.sprite.Sprite):
	def __init__(self, wfs, xtrans=0, ytrans=0, ztrans=0, xspin=0, yspin=0, zspin=0):
		pygame.sprite.Sprite.__init__(self)
		self.frames = [f for f in wfs] if isinstance(wfs, tuple) else [wfs]
		self.xtrans = xtrans
		self.ytrans = ytrans
		self.ztrans = ztrans
		self.xspin = xspin
		self.yspin = yspin
		self.zspin = zspin
		self.set_ctr()
		self.set_zradius()
		
	def set_ctr(self, xyz=None):
		if xyz is not None:
			self.ctr = Zpt(xyz[0], xyz[1], xyz[2])
		else:
			allshapes = len(self.frames)
			newX = sum([frame.center.x for frame in self.frames]) / allshapes
			newY = sum([frame.center.y for frame in self.frames]) / allshapes
			newZ = sum([frame.center.z for frame in self.frames]) / allshapes
			self.ctr = Zpt(newX, newY, newZ)
	
	def get_zlen(self, p1, p2):
		lenx = abs(p1.x - p2.x)
		leny = abs(p1.y - p2.y)
		lenz = abs(p1.z - p2.z)
		rootme = lenx**2 + leny**2 + lenz**2
		###return math.sqrt(rootme) ###distance squared
		return rootme
	
	def set_zradius(self):
		possible_zrads = []
		for frame in self.frames:
			for zpt in frame.zpts:
				possible_zrads.append(self.get_zlen(zpt, self.ctr))
		self.zradius = max(possible_zrads)
		#print self.zradius
				
	
	def add_frame(self, frame):
		self.frames.append(frame)
		
	def d_move(self, deltaX=0, deltaY=0, deltaZ=0):
		for frame in self.frames:
			frame.delta_move(deltaX, deltaY, deltaZ)
		self.set_ctr()
	
	def rotate(self, radians, ignore, ctr=None):
		if ctr is None:
			ctr = self.ctr
		for frame in self.frames:
			frame.good_rotate(radians, ignore, ctr)
		#self.set_ctr()
	
	def update(self):
		if self.xtrans + self.ytrans + self.ztrans != 0:
			self.d_move(self.xtrans, self.ytrans, self.ztrans)
		if self.xspin != 0:
			self.rotate(self.xspin, 'x')
		if self.yspin != 0:
			self.rotate(self.yspin, 'y')
		if self.zspin != 0:
			self.rotate(self.zspin, 'z')
		#self.set_ctr()
		for frame in self.frames:
			frame.update()
	
	def kill(self):
		for frame in self.frames:
			frame.kill()
		super(Multiframe, self).kill()
			
