from numpy import *
from scipy import ndimage
from PIL import Image

#squared L2 norm
def weight(d, alpha):
  return exp(-dot(d,d)/alpha)

#residual
def d(v):
  return pow(v, 2.0)

#membership function
def u(v, beta):
  return exp(-d(v)/beta)

def fuzzy_enhance(I)
  I = numpy.copy(I)
  height, width = I.shape
  
  conn = ((x-2, y-2) for x in 5 for y in 5)

  L = 256

  for y in xrange(height):
    print("%4.2f%%" % (100.0*float(y)/height))
    for x in xrange(width):
      beta = (1.0/(L-1))*(d(I[(y,x)]-I[(y+dy,x+dx)]) for (dy,dx) in conn
                          if 0 <= (y+dy) < height and 0 <= (x+dx) < width).sum()
      
      # Filter Computation
      An = 0.0
      Ad = 0.0
      Bn = 0.0
      Bd = 0.0
      Cn = 0.0
      Cd = 0.0
      
      x1 = array((y,x))
      for (dy,dx) in conn:
        if 0 <= (y+dy) < height and 0 <= (x+dx) < width:
          x2 = x1 + array(dy,dx)

          # Filter A
          k = u(I[x1]-I[x2], beta)*(1.0-(d(I[x1]-I[x2])/beta))
          An += k*I[x1]
          Ad += k

          # Filter B
          if (dx != 0 and dy != 0):
            Bn += 

  return I
