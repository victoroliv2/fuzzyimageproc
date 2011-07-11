import numpy
from scipy import ndimage
from PIL import Image


conn = [
        ( 0, 0),
        (-1,-1),
        ( 0,-1),
        (+1,-1),
        (-1, 0),
        (+1, 0),
        (-1,+1),
        ( 0,+1),
        (+1,+1)
       ]

def tnorm(a,b):
  return max(a+b-1.0, 0.0)

def impl(a,b):
  return min(1.0, 1.0-a+b)


def fdilation(image, struc):
  result = numpy.zeros_like(image)
  height, width = image.shape

  for y in xrange(height):
    for x in xrange(width):
      
      l = []
      for (dx,dy) in conn:
        vy = y+dy
        vx = x+dx
        if 0 <= vy < height and 0 <= vx < width:
          l += ( tnorm(struc[-dy+1,-dx+1], image[y+dy,x+dx]) ,)
      
      result[y,x] = max(l)
      
  return result

def ferosion(image, struc):
  result = numpy.zeros_like(image)
  height, width = image.shape

  for y in xrange(height):
    for x in xrange(width):
      
      l = []
      for (dx,dy) in conn:
        vy = y+dy
        vx = x+dx
        if 0 <= vy < height and 0 <= vx < width:
          l += ( impl(struc[-dy+1,-dx+1], image[y+dy,x+dx]) ,)
          
      result[y,x] = min(l)
      
  return result

def fopening(image, struc):
  return fdilation( ferosion(image, struc), struc )

def fclosing(image, struc):
  return ferosion( fdilation(image, struc), struc )

def fgrad(image, struc):
  return abs(fdilation(image, struc) - ferosion( image, struc ))
  
### TESTS ###

I = numpy.asarray(Image.open("station.jpg").convert("L")).astype(numpy.float)/255.0

B = numpy.array([
                 [0.85, 0.95, 0.85],
                 [0.95, 1.00, 0.95],
                 [0.85, 0.95, 0.85],
                ])

from multiprocessing import Process

def a():
  D = I
  for i in range(5):
    print i
    D = fdilation(D, B)
    
  J = (255.0*D).astype(numpy.uint8)
  Image.fromarray(J).save("fdilation.png")

def b():
  E = I
  for i in range(5):
    print i
    E = ferosion(E, B)
 
  J = (255.0*E).astype(numpy.uint8)
  Image.fromarray(J).save("ferosion.png")

def c(): 
  K = fgrad(I, B)
  J = (255.0*K).astype(numpy.uint8)
  Image.fromarray(J).save("fgrad.png")

pa = Process(target=a)
pb = Process(target=b)
pc = Process(target=c)
pa.start()
pb.start()
pc.start()
pa.join()
pb.join()
pc.join()
