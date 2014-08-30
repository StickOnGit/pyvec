import math
from math import pi as PI, cos, sin, sqrt

from zpt import Zpt
from wireframe import Wireframe

def twod_zpts(x, y, z, sides, rad):
	"""Returns a list of Zpts that create a regular polygon of 'sides' sides.
	These points exist on a circle with radius 'rad'."""
	allpoints = []
	for i in xrange(0, sides):
		allpoints.append(Zpt(x+(rad * cos(2*PI*i/sides)), y+(rad * sin(2*PI*i/sides)), z))
	return allpoints
	
def rightside(wfobj, sides):
	"""Use to rotate the shape after creating, before returning.
	Tries to make it look normal after plotting the points."""
	if sides % 2 == 0:
		wfobj.good_rotate(PI/sides, 'z')
	else:
		wfobj.good_rotate(PI/sides/2, 'z')

def reg_poly(x, y, z, sides, rad=50, color=(140, 140, 140), width=2):
	"""Returns a Wireframe regular polygon with 'sides' number of sides."""
	new_wf = Wireframe(zpts=twod_zpts(x, y, z, sides, rad), color=color, width=width)
	ties = tuple(i for i in range(0, sides))
	new_wf.set_lines(ties)
	rightside(new_wf, sides)
	return new_wf

###############
###3d shapes###

def cube(x, y, z, lng=50, color=(140, 140, 140), width=2):
	h = (sqrt(2)*lng)/2
	_cube = twod_zpts(x, y, z-h, 4, rad=lng) + twod_zpts(x, y, z+h, 4, rad=lng)
	
	new_wf = Wireframe(zpts=_cube, color=color, width=width)
	new_wf.set_lines((0, 1, 2, 3))
	new_wf.set_lines((4, 5, 6, 7))
	for i in xrange(0, 4):
		new_wf.set_line(i, i+4)
	rightside(new_wf, 4)
	return new_wf

def octah(x, y, z, lng=50, color=(140, 140, 140), width=2):
	h = lng/2.0
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

def prism(x, y, z, sides=3, lng=30, dep=50, color=(140, 140, 140), width=2):
	"""Returns two regular polygons joined at each point which is only different
	in its z value."""
	h = lng/2.0
	h_d = dep/2.0
	_prism = twod_zpts(x, y, z-h_d, sides, h) + twod_zpts(x, y, z+h_d, sides, h)
			
	new_wf = Wireframe(zpts=_prism, color=color, width=width)
	first_set = tuple(i for i in range(0, sides))
	second_set = tuple(j for j in range(sides, 2*sides))
	new_wf.set_lines(first_set)
	new_wf.set_lines(second_set)
	for s in range(0, sides):
		new_wf.set_line(first_set[s], second_set[s])
	rightside(new_wf, sides)
	return new_wf

def disc(x, y, z, rad=60, dep=15, color=(140, 140, 140), width=2):
	"""Returns a 12-sided object similar to a disc."""
	_disc = prism(x, y, z, sides=12, lng=rad, dep=dep, color=color, width=width)
	_disc.good_rotate(PI/2, 'x')
	return _disc
	
def nested_disc(x, y, z, rad=60, dep=15, nests=2, color=(140, 140, 140), width=2):
	_ndisc = prism(x, y, z, sides=12, lng=rad, dep=dep, color=color, width=width)
	for ring in range(1, nests):
		alt_h = h * float(ring/nests)
		next = twod_zpts(x, y, z-h_d, sides, alt_h) + twod_zpts(x, y, z+h_d, sides, alt_h)
		_ndisc.zpts += next
		##maybe i don't fucken know whatever
	_ndisc.good_rotate(PI/2, 'x')
	return _ndisc
