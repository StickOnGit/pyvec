import math

from zpt import Zpt
from wireframe import Wireframe



###3d shapes###

def cube(x, y, z, lng=50, color=(140, 140, 140), width=2):
	h = lng/2
	
	_cube = [Zpt(x-h, y-h, z-h),
			Zpt(x+h, y-h, z-h),
			Zpt(x+h, y+h, z-h), 
			Zpt(x-h, y+h, z-h), 
			Zpt(x-h, y-h, z+h),
			Zpt(x+h, y-h, z+h),
			Zpt(x+h, y+h, z+h), 
			Zpt(x-h, y+h, z+h)]
		
	new_wf = Wireframe(zpts=_cube, color=color, width=width)
	new_wf.set_lines((0, 1, 2, 3))
	new_wf.set_lines((4, 5, 6, 7))
	new_wf.set_line(0, 4)
	new_wf.set_line(1, 5)
	new_wf.set_line(2, 6)
	new_wf.set_line(3, 7)
	return new_wf

def octah(x, y, z, lng=50, color=(140, 140, 140), width=2):
	h = lng/2
	_octah = [Zpt(x+h, y, z), 
			Zpt(x, y+h, z), 
			Zpt(x, y, z+h), 
			Zpt(x-h, y, z), 
			Zpt(x, y-h, z), 
			Zpt(x, y, z-h)]
			
	new_wf = Wireframe(zpts=_octah, color=color, width=width)
	new_wf.set_lines((1, 2, 4, 5))
	new_wf.set_lines((0, 2, 3, 5))
	new_wf.set_lines((0, 1, 3, 4))
	return new_wf

def prism(x, y, z, lng=50, color=(140, 140, 140), width=2):
	h = lng/2
	return [Zpt(x, y, z), Zpt(x+15, y+15, z), Zpt(x-15, y+15, z), 
		Zpt(x, y, z+30), Zpt(x+15, y+15, z+30), Zpt(x-15, y+15, z+30)]
