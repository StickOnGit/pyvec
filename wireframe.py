import pygame
import math
from zpt import Zpt

class Wireframe(pygame.sprite.Sprite):
	def __init__(self, zpts, color=(26, 80, 100), width=2):
		pygame.sprite.Sprite.__init__(self)
		self.zpts = [pt for pt in zpts]
		self.shapes = []
		self.lines = []
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
		self.lines.append((self.zpts[ptindex1], self.zpts[ptindex2]))
		
	def set_lines(self, pts, connect=True):
		"""Set a series of lines by their index in obj.zpts.
		First arg should be tuple of ints; second optional arg is for
		whether or not the last point should connect to the first. Defaults True."""
		firstpoint = pts[0]
		for index in range(0, len(pts)-1):
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
			
	def translate(self, newX=0, newY=0, newZ=0):
		"""Somehow this used to not be exactly like delta_move, but now it is.
		I don't know why."""
		for zpt in self.zpts + [self.center]:
			zpt.x += newX
			zpt.y += newY
			zpt.z += newZ
			
	def good_rotate(self, radians, ignore, ctr=None):
		if ctr is None:
			ctr = self.center
		for zpt in self.zpts:
			##x = zpt.x - ctr.x
			##y = zpt.y - ctr.y
			##z = zpt.z - ctr.z
			if ignore == 'x':
				##vals = (y, z)
				vals = (zpt.y - ctr.y, zpt.z - ctr.z)
			elif ignore == 'y':
				##vals = (x, z)
				vals = (zpt.x - ctr.x, zpt.z - ctr.z)
			elif ignore == 'z':
				##vals = (y, x)
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
		self.own_ctr()
		
	def is_pt_tied(self, pt1, pt2):
		"""Checks to see if pt1 is in a shape with pt2. Does NOT mean
		they share a line (wireframe objects don't track lines right now."""
		answer = False
		for shape in self.shapes:
			if pt1 in shape and pt2 in shape:
				answer = True
			else: pass
		return answer
		
	def find_minmax(self):
		allvals = [[zpt.x for zpt in self.zpts],
		[zpt.y for zpt in self.zpts],
		[zpt.z for zpt in self.zpts]]
		returnvals = []
		for ptvals in allvals:
			returnvals.append([min(ptvals), max(ptvals)])
		return returnvals
		

