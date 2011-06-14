import numpy
from scipy import ndimage
from PIL import Image
import pymorph

def median(image):
  return ndimage.filters.median_filter(image, size=5)

def areaclose(image):
  return pymorph.areaclose(image, 4, pymorph.secross())

# A Fuzzy Filter for Images Corrupted by Impulse Noise
# Fabrizio Russo, Member, IEEE, and Giovanni Ramponi, Member, IEEE

def memoize(function):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper
  
def fuzzy_filter(image):
  image = numpy.copy(image)
  height, width = image.shape

  conn = {
          0 : ( 0, 0),
          1 : (-1,-1),
          2 : ( 0,-1),
          3 : (+1,-1),
          4 : (-1, 0),
          5 : (+1, 0),
          6 : (-1,+1),
          7 : ( 0,+1),
          8 : (+1,+1)
         }

  # Rule Base
  rules = (
            (2, 5, 7),
            (5, 7, 4),
            (7, 4, 2),
            (4, 2, 5),
            (1,3,8,6),
            (1,2,3,5),
            (2,3,5,8),
            (3,5,8,7),
            (5,8,7,6),
            (8,7,6,4),
            (7,6,4,1),
            (6,4,1,2),
            (4,1,2,3)
          )

  L = 256
  C_PO =  L-1
  C_NE = -L+1
  W = 2*(L-1)

  @memoize  
  def m(u, c, w):
    if u <= c-w:
      return 0.0
    elif c-w < u < c+w:
      return float(w-abs(u-c))/w
    else:
      return 0.0
  
  @memoize
  def m_sm(u, a=40, b=32):
    if u <= a:
      return 1.0
    elif a < u <= a+b:
      return (a+b-u)/b
    else:
      return 0.0

  for y in xrange(height):
    print("%4.2f%%" % (100.0*float(y)/height))
    for x in xrange(width):
      l_1 = []
      l_2 = []
      for r in rules:
        l_po = [1.0,] # 1 is min invariant
        l_ne = [1.0,]
        for i in r:
          (dx,dy) = conn[i]
          vy = y+dy
          vx = x+dx
          if 0 <= vy < height and 0 <= vx < width:
            x_j = int(image[vy,vx])-int(image[y,x])
            l_po += (m(x_j, C_PO, W),)
            l_ne += (m(x_j, C_NE, W),)
        l_1 += (min(l_po),)
        l_2 += (min(l_ne),)
      lambda_1 = max(l_1)
      lambda_2 = max(l_2)
      lambda_0 = max(0.0, 1.0-lambda_1-lambda_2)
      v = (L-1)*((lambda_1-lambda_2)/(lambda_0+lambda_1+lambda_2))
      v_small = v*(1.0-m_sm(abs(v)))
      image[y,x] += v_small
  return image

I = numpy.asarray(Image.open("station.jpg").convert("L")).astype(numpy.uint8)

#impulsive noise
N = 30
#salt
noise = numpy.random.random_integers(0, 100, size=I.shape) > (100-(N/2))
noise = (noise*255).astype(numpy.uint8)
I = I | noise
#pepper
noise = ~(numpy.random.random_integers(0, 100, size=I.shape) > (100-(N/2)))
noise = (noise*255).astype(numpy.uint8)
I = I & noise

Image.fromarray(I).save("noise.png")

T = median(I)
Image.fromarray(T).save("median.png")
#T = areaclose(I)
#Image.fromarray(T).save("areaclose.png")
T = fuzzy_filter(I)
Image.fromarray(T).save("fuzzy.png")
