import pygame
import math
from zpt import Zpt

class Wireframe(pygame.sprite.Sprite):
	def __init__(self, zpts, color=(26, 80, 100), width=2):
		pygame.sprite.Sprite.__init__(self)
		self.zpts = [pt for pt in zpts]
		#self.zpts = set(zpt for zpt in zpts)
		self.shapes = []
		#self.lines = []
		self.lines = set()
		self.color = color
		self.width = width
		self.own_ctr()
		
	def set_shape(self, *zpts):
		newShape = []
		for index in zpts:
			newShape.append(self.zpts[index])
		self.shapes.append(tuple(newShape))
		
	def set_line(self, ptindex1, ptindex2):
		"""Set a line by the index of the point within obj.zpts list."""
		#self.lines.append((self.zpts[ptindex1], self.zpts[ptindex2]))
		self.lines.add((self.zpts[ptindex1], self.zpts[ptindex2]))
		
	def set_lines(self, pts, connect=True):
		"""Set a series of lines by their index in obj.zpts.
		First arg should be tuple of ints; second optional arg is for
		whether or not the last point should connect to the first. Defaults True."""
		firstpoint = pts[0]
		for index in xrange(0, len(pts)-1):
			self.set_line(pts[index], pts[index+1])
			if connect:
				self.set_line(pts[-1], firstpoint)
		
	def find_center(self):
		"""Finds the center of the object, according to the average value of
		all of its Zpts x, y, z values."""
		allpoints = len(self.zpts)
		ctrX = sum([zpt.x for zpt in self.zpts]) / allpoints
		ctrY = sum([zpt.y for zpt in self.zpts]) / allpoints
		ctrZ = sum([zpt.z for zpt in self.zpts]) / allpoints
		return Zpt(ctrX, ctrY, ctrZ)
	
	def own_ctr(self):
		self.center = self.find_center()
	
	def delta_move(self, deltaX=0, deltaY=0, deltaZ=0):
		"""Moves all the points by a certain number."""
		for zpt in self.zpts + [self.center]:
			zpt.x += deltaX
			zpt.y += deltaY
			zpt.z += deltaZ
			
	def move_ctr_to_pt(self, newX=None, newY=None, newZ=None):
		"""Move the wireframe by setting its center to a new point."""
		passX = newX - self.center.x if newX is not None else 0
		passY = newY - self.center.y if newY is not None else 0
		passZ = newZ - self.center.z if newZ is not None else 0
		self.delta_move(passX, passY, passZ)
			
	def good_rotate(self, radians, ignore, ctr=None):
		if ctr is None:
			ctr = self.center
		for zpt in self.zpts + [self.center]:
			if ignore == 'x':
				vals = (zpt.y - ctr.y, zpt.z - ctr.z)
			elif ignore == 'y':
				vals = (zpt.x - ctr.x, zpt.z - ctr.z)
			elif ignore == 'z':
				vals = (zpt.y - ctr.y, zpt.x - ctr.x)
			v1, v2 = vals
			d = math.hypot(v1, v2)
			theta = math.atan2(v1, v2) + radians
			if ignore == 'x':
				zpt.z = ctr.z + d * math.cos(theta)
				zpt.y = ctr.y + d * math.sin(theta)
			elif ignore == 'y':
				zpt.z = ctr.z + d * math.cos(theta)
				zpt.x = ctr.x + d * math.sin(theta)
			elif ignore == 'z':
				zpt.x = ctr.x + d * math.cos(theta)
				zpt.y = ctr.y + d * math.sin(theta)
		
	def pts_are_tied(self, pt1, pt2):
		"""Checks to see if two points are in a line."""
		for line in self.lines:
			if pt1 in line and pt2 in line:
				return True
		return False
		
	def find_minmax(self):
		allvals = [[zpt.x for zpt in self.zpts],
		[zpt.y for zpt in self.zpts],
		[zpt.z for zpt in self.zpts]]
		returnvals = []
		for ptvals in allvals:
			returnvals.append([min(ptvals), max(ptvals)])
		return returnvals
		

