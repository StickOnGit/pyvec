import pygame
from zpt import Zpt
from wireframe import Wireframe
import random
import math
from multiprocessing import Pool

ViewPool = Pool(processes=4)

GOLD = 1.618033

WIDTH = 1000
HEIGHT = 600
DEPTH = (WIDTH+HEIGHT)/GOLD

PAD = 150
PAD_W, PAD_H, PAD_D = WIDTH + PAD, HEIGHT + PAD, (DEPTH + PAD) * 2
N_PAD = -1 * PAD

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)

H_ZPT = Zpt(WIDTH/2, HEIGHT/2, DEPTH)
CAM_PT = Zpt(WIDTH/2, HEIGHT/2, DEPTH * -1.0)

PAD_C = CAM_PT.z - PAD

ALLCAM = Wireframe(zpts=(H_ZPT, CAM_PT), color=BLACK)

##global for new_mf_draw testing##
camToDepth = abs(CAM_PT.z) + DEPTH


def set_horizon(xytuple):
	HORIZON = xytuple
	HOR_X = HORIZON[0] / float(WIDTH)
	HOR_Y = HORIZON[1] / float(HEIGHT)
	return HORIZON, HOR_X, HOR_Y
	
def set_hzpt(xytuple):
	H_ZPT.x, H_ZPT.y = xytuple
	HOR_X = H_ZPT.x / float(WIDTH)
	HOR_Y = H_ZPT.y / float(HEIGHT)
	return HOR_X, HOR_Y

HOR_X, HOR_Y = set_hzpt((H_ZPT.x, H_ZPT.y))
	
def wipe():
	SCREEN.fill(BLACK)

flip = pygame.display.update

def draw_obj_img(obj):
	SCREEN.blit(obj.image, obj.rect.center)
	
def zoom_zpt_pos(zpt):
	z = 1.0 - (zpt.z / DEPTH)
	screenX = zpt.x - HOR_X / z 
	screenY = zpt.y - HOR_Y / z
	
	
	return screenX, screenY
	
	
	
def new_zpt_pos(zpt):
	"""Changes a zpt to an (x, y) tuple after adjusting for depth."""
	fret = camToDepth - (camToDepth / (2 ** (zpt.z/(camToDepth/2))))
	horzoff = 1.0 - (fret / camToDepth)
	invhorz = 1.0 - horzoff
	newX = (zpt.x * horzoff) + (WIDTH * invhorz * HOR_X)
	newY = (zpt.y * horzoff) + (HEIGHT * invhorz * HOR_Y)
	return (newX, newY)
	
def rc_zpt_pos(zpt):
	#cartX = zpt.x - HOR_X
	#cartY = -zpt.y + HOR_Y
	xdist = abs(CAM_PT.x - zpt.x)**2
	ydist = abs(CAM_PT.y - zpt.y)**2
	zdist = abs(CAM_PT.z - zpt.z)**2
	camdist = abs(CAM_PT.z - DEPTH)**2
	#zoff = 1.0 - (zdist / (camToDepth*camToDepth))
	zoff = camToDepth / (zdist/(camToDepth/2))
	zinv = 1.0 - zoff
	#newX = (zpt.x * zoffset) + (WIDTH * zinset * HOR_X)
	#newY = (zpt.y * zoffset) + (HEIGHT * zinset * HOR_Y)
	###xoff = 1.0 - (xdist / (camToDepth*camToDepth))
	#xoff = 1.0 - (abs(HOR_X*HOR_X - xdist) / (WIDTH))
	xoff = 1.0 - (xdist / camdist)
	#print xoff
	xinv = 1.0 - xoff
	yoff = 1.0 - (ydist / camdist)
	yinv = 1.0 - yoff
	newX = (zpt.x * xoff * zoff) + (WIDTH * HOR_X * zinv)
	newY = (zpt.y * yoff * zoff) + (HEIGHT * HOR_Y * zinv)
	
	return (newX, newY)
	
def cart_zpt_pos(zpt):
	"""If can't remember how to fix, the Y coordinate calculations mimic the X."""
	#cartX = zpt.x - H_ZPT.x
	cartY = -zpt.y + HOR_Y
	#cartCamX = CAM_PT.x - H_ZPT.x
	cartCamY = -CAM_PT.y + HOR_Y
	##print "screen: (%d, %d) cart: (%d, %d)" % (zpt.x, zpt.y, cartX, cartY)
	##print "zpt.x: %d, HOR_X: %d" % (zpt.x, H_ZPT.x)
	#xdist = abs(cartCamX - cartX)**2
	ydist = abs(cartCamY - cartY)**2
	zdist = abs(CAM_PT.z - zpt.z)**2
	camdist = abs(CAM_PT.z - DEPTH)**2
	zoff = camToDepth / (zdist/(camToDepth/GOLD))
	zinv = 1.0 - zoff
	#xoff = xdist / camdist
	xoff = 1.0 - (abs(zpt.x - H_ZPT.x)) / WIDTH
	##print xoff
	yoff = ydist / camdist
	#newX = ((cartX) - (HOR_X * xoff)) * zoff + (WIDTH * HOR_X * zinv)
	newX = ((zpt.x) - (HOR_X * xoff)) * zoff + (WIDTH * HOR_X * zinv)
	newY = ((HOR_Y * yoff) - (cartY)) * zoff + (HEIGHT * HOR_Y * zinv)
	return (newX, newY)

F_O_V = 5

def use_hzpt_pos(zpt):
	"""Definitely the best as of 03/10/14."""
	##cartX = zpt.x - H_ZPT.x
	##cartY = -zpt.y + H_ZPT.y
	##zdist = abs(CAM_PT.z - zpt.z)**2
	##zoff = camToDepth / (zdist/(camToDepth/GOLD))
	zoff = camToDepth / ((abs(CAM_PT.z - zpt.z)**2)/(camToDepth/GOLD))
	zinv = 1.0 - zoff
	xoff = 1.0 - ((abs(zpt.x - H_ZPT.x)) / WIDTH)/ F_O_V
	yoff = 1.0 - ((abs(zpt.y - H_ZPT.y)) / HEIGHT)/ F_O_V
	##newX = ((cartX * xoff) + H_ZPT.x) * zoff + (WIDTH * HOR_X * zinv)
	##newY = ((H_ZPT.y) - (cartY * yoff)) * zoff + (HEIGHT * HOR_Y * zinv)
	newX = (((zpt.x - H_ZPT.x) * xoff) + H_ZPT.x) * zoff + (WIDTH * HOR_X * zinv)
	newY = ((H_ZPT.y) - ((-zpt.y + H_ZPT.y) * yoff)) * zoff + (HEIGHT * HOR_Y * zinv)
	return (newX, newY)
	
def unpack_use_hzpt_pos(zpt, horizon=H_ZPT, hor_x=HOR_X, hor_y=HOR_Y, total_d=camToDepth, gold=GOLD):
	lx, ly, lz = zpt.x, zpt.y, zpt.z
	#zoff = camToDepth / (abs(CAM_PT.z - lz)**2/(camToDepth/GOLD))
	zoff = total_d / (abs(CAM_PT.z - lz)**2/(total_d/gold))
	zinv = 1.0 - zoff
	xoff = 1.0 - ((abs(lx - horizon.x)) / WIDTH)/ F_O_V
	yoff = 1.0 - ((abs(ly - horizon.y)) / HEIGHT)/ F_O_V
	newX = (((lx - horizon.x) * xoff) + horizon.x) * zoff + (WIDTH * hor_x * zinv)
	newY = ((horizon.y) - ((-ly + horizon.y) * yoff)) * zoff + (HEIGHT * hor_y * zinv)
	return (newX, newY)
	
def new_shape(shape):
	"""Returns a tuple of adjusted shape points."""
	shape_pts = ()
	for zpt in shape:
		shape_pts = (unpack_use_hzpt_pos(zpt), ) + shape_pts
		#shape_pts = (zoom_zpt_pos(zpt), ) + shape_pts
	return shape_pts
	
def new_wireframe(wfobj):
	new_shapes = ()
	for shape in sorted(wfobj.shapes, key=lambda shape: max([zpt.z for zpt in shape]), reverse=True):
		new_shapes += new_shape(shape)
	return new_shapes

def multiframe_draw(obj):
	"""Quite good as long as horizon is the center of the screen"""
	camToDepth = abs(CAM_PT.z) + DEPTH
	for wf in obj.frames:
		objCtrX, objCtrY, objCtrZ = wf.center.as_t()
		if (not PAD_C < objCtrZ < PAD_D) or (not N_PAD < objCtrX < PAD_W) or (not N_PAD < objCtrY < PAD_H):
			pass
		else:
			for shape in sorted(wf.shapes, key=lambda shape: max([zpt.z for zpt in shape]), reverse=True):
				shapeZ = sum(zpt.z for zpt in shape) / len(shape)
				drawnpoints = []
				for zpt in shape:
					##ctrZ = zpt.z
					##fret = camToDepth - (camToDepth / (2 ** (ctrZ/(camToDepth/2))))
					fret = camToDepth - (camToDepth / (2 ** (zpt.z/(camToDepth/2))))
					horzoff = 1.0 - (fret / camToDepth)
					invhorz = 1.0 - horzoff
					newX = (zpt.x * horzoff) + (WIDTH * invhorz * HOR_X)
					newY = (zpt.y * horzoff) + (HEIGHT * invhorz * HOR_Y)
					drawnpoints.append((newX, newY))
				colormod = 1.0 - (shapeZ / camToDepth)
				if colormod > 1:
					colormod = 1
				if colormod < 0:
					colormod = 0
				widthmod = int(wf.width * horzoff * 2)
				if 1 > widthmod > 0:
					widthmod = 1
				if widthmod <= 0 and wf.width == 0:
					widthmod = 0
				elif widthmod <= 0 and wf.width > 0:
					widthmod = 1
				newcolor = [int(x * colormod) for x in wf.color]
				pygame.draw.polygon(SCREEN, newcolor, drawnpoints, widthmod)



def new_mf_draw(obj):
	"""Composite from multiframe_draw, separating functions out."""
	drawqueue = []
	for wf in obj.frames:
		if (not PAD_C < obj.ctr.z < PAD_D) or (not N_PAD < obj.ctr.x < PAD_W) or (not N_PAD < obj.ctr.y < PAD_H):
			pass
		else:
			#drawnpoints = []
			for shape in sorted(wf.shapes, key=lambda shape: max([zpt.z for zpt in shape]), reverse=True):
				shapeZ = sum(zpt.z for zpt in shape) / len(shape)
				drawnpoints = new_shape(shape)
				colormod = 1.0 - (shapeZ / camToDepth)
				if colormod > 1:
					colormod = 1
				if colormod < 0:
					colormod = 0
				widthmod = int(wf.width * (1.0 - (shapeZ / camToDepth)) * 2)
				if 1 > widthmod > 0:
					widthmod = 1
				if widthmod <= 0 and wf.width == 0:
					widthmod = 0
				elif widthmod <= 0 and wf.width > 0:
					widthmod = 1
				#newcolor = [int(x * colormod) for x in wf.color]
				newcolor = map(lambda x: x * colormod, wf.color)
				#pygame.draw.polygon(SCREEN, newcolor, drawnpoints, widthmod)
				drawqueue.append((newcolor, drawnpoints, widthmod))
	for drawobj in drawqueue:
		pygame.draw.polygon(SCREEN, drawobj[0], drawobj[1], drawobj[2])
		
def get_colormod(shape, gold=GOLD):
	colormod = 1.0 - ((sum(zpt.z for zpt in shape) / len(shape)) / (camToDepth * gold))
	if colormod > 1:
		colormod = 1
	if colormod < 0:
		colormod = 0
	return colormod
	
def get_widthmod(wfobj):
	widthmod = int(wfobj.width * (1.0 - (wfobj.center.z / len(wfobj.zpts)) / camToDepth)) * 2
	if widthmod <= 0 and wfobj.width == 0:
		widthmod = 0
	elif widthmod <= 0 and wfobj.width > 0:
		widthmod = 1
	return widthmod
		
def bg_draw_lines(wfobj):
	widthmod = get_widthmod(wfobj)
	for line in sorted(wfobj.lines, key=lambda line: (line[0].z + line[1].z)/2):
		colormod = get_colormod(line)
		twopts = new_shape(line)
		pygame.draw.line(SCREEN, [int(x * colormod) for x in wfobj.color], twopts[0], twopts[1], widthmod)
		#pygame.draw.line(SCREEN, map(lambda x: x * colormod, wfobj.color), twopts[0], twopts[1], widthmod)
		
def drawq_draw(groupobj, draw_it=pygame.draw.line, wmod=get_widthmod, cmod=get_colormod, news=new_shape):
	to_draw = []
	for wfobj in groupobj:
		#widthmod = get_widthmod(wfobj)
		widthmod = wmod(wfobj)
		for line in wfobj.lines:
			#colormod = get_colormod(line)
			colormod = cmod(line)
			#to_draw.append((new_shape(line),
			to_draw.append((news(line), 
							[x * colormod for x in wfobj.color], 
							widthmod, 
							(line[0].z + line[1].z) / -2))
	for drawline in sorted(to_draw, key=lambda x: x[3]):
		#pygame.draw.line(SCREEN, drawline[1], drawline[0][0], drawline[0][1], drawline[2])
		draw_it(SCREEN, drawline[1], drawline[0][0], drawline[0][1], drawline[2])
		
def proc_draw(groupobj):
	maybe = ViewPool.apply_async(drawq_draw, [groupobj])
	maybe.get(timeout=1)
	
current_draw = drawq_draw		##makes testing new methods simpler :/
