import pygame
from math import hypot, atan2, sin, cos
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
		self.all_pts = set()
		self.set_all_pts()
		self.set_ctr()
		self.set_zradius()
		
	def set_all_pts(self):
		#for frame in self.frames:
		#	self.add_zpts_in_frame(frame)
		map(self.add_zpts_in_frame, self.frames)
					
	def add_zpts_in_frame(self, frame):
		for zpt in frame.zpts:
			if zpt not in self.all_pts:
				self.all_pts.add(zpt)
			
		
	def set_ctr(self, xyz=None):
		if xyz is not None:
			self.ctr = Zpt(xyz[0], xyz[1], xyz[2])
		else:
			allshapes = len(self.all_pts)
			newX = sum([zpt.x for zpt in self.all_pts]) / allshapes
			newY = sum([zpt.y for zpt in self.all_pts]) / allshapes
			newZ = sum([zpt.z for zpt in self.all_pts]) / allshapes
			self.ctr = Zpt(newX, newY, newZ)
	
	def get_zlen(self, p1, p2):
		lenx = abs(p1.x - p2.x)
		leny = abs(p1.y - p2.y)
		lenz = abs(p1.z - p2.z)
		rootme = lenx**2 + leny**2 + lenz**2
		return rootme
	
	def set_zradius(self):
		possible_zrads = []
		for zpt in self.all_pts:
			possible_zrads.append(self.get_zlen(zpt, self.ctr))
		self.zradius = max(possible_zrads)
		#print math.sqrt(self.zradius)
				
	
	def add_frame(self, frame):
		self.frames.append(frame)
		self.add_zpts_in_frame(frame)
		
	def d_move(self, deltaX=0, deltaY=0, deltaZ=0):
		for frame in self.frames:
			frame.delta_move(deltaX, deltaY, deltaZ)
		self.set_ctr()
		
	def alt_d_move(self, deltaX=0, deltaY=0, deltaZ=0):
		for zpt in self.all_pts:
			zpt.x += deltaX
			zpt.y += deltaY
			zpt.z += deltaZ
		self.ctr.x += deltaX
		self.ctr.y += deltaY
		self.ctr.z += deltaZ
	
	def rotate(self, radians, ignore, ctr=None):
		if ctr is None:
			ctr = self.ctr
		for frame in self.frames:
			frame.good_rotate(radians, ignore, ctr)
		#self.set_ctr()
		
	def alt_rotate(self, radians, ignore, ctr=None):
		#total_pts = set(zpt for zpt in self.all_pts)
		#total_pts.add(self.ctr if ctr is None else ctr)
		#for zpt in self.all_pts.add(self.ctr):
		#for zpt in self.zpts + [self.center]:
		#all_pts = self.all_pts
		if ctr is None:
			ctr = self.ctr
		for zpt in self.all_pts:
			if ignore == 'x':
				vals = (zpt.y - ctr.y, zpt.z - ctr.z)
			elif ignore == 'y':
				vals = (zpt.x - ctr.x, zpt.z - ctr.z)
			elif ignore == 'z':
				vals = (zpt.y - ctr.y, zpt.x - ctr.x)
			v1, v2 = vals
			d = hypot(v1, v2)
			theta = atan2(v1, v2) + radians
			if ignore == 'x':
				zpt.z = ctr.z + d * cos(theta)
				zpt.y = ctr.y + d * sin(theta)
			elif ignore == 'y':
				zpt.z = ctr.z + d * cos(theta)
				zpt.x = ctr.x + d * sin(theta)
			elif ignore == 'z':
				zpt.x = ctr.x + d * cos(theta)
				zpt.y = ctr.y + d * sin(theta)
		if ctr is not self.ctr:
			self.set_ctr()
	
	def update(self):
		#print len(self.all_pts)
		if self.xtrans + self.ytrans + self.ztrans != 0:
			self.alt_d_move(self.xtrans, self.ytrans, self.ztrans)
		if self.xspin != 0:
			self.alt_rotate(self.xspin, 'x')
		if self.yspin != 0:
			self.alt_rotate(self.yspin, 'y')
		if self.zspin != 0:
			self.alt_rotate(self.zspin, 'z')
		#self.set_ctr()
		for frame in self.frames:
			frame.update()
		#map(lambda frame: frame.update(), self.frames)
	
	def kill(self):
		for frame in self.frames:
			frame.kill()
		super(Multiframe, self).kill()
			
