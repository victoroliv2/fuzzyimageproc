import numpy
from scipy import ndimage
from PIL import Image

def laplace(image):
  mask = numpy.array(
               [[ 0, 1, 0],
                [ 1,-4, 1],
                [ 0, 1, 0]]
                )
  return ndimage.filters.convolve(image, mask)

# Edge Extraction by FIRE Operators
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
  result = numpy.zeros_like(image)
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
            (2,4),
            (4,6),
            (6,8),
            (8,2),
          )

  L = 256
  
  #antedecent
  C_ZERO = 0
  W_ZERO = (L-2)/3
  
  #consequent
  C_BL = 0
  C_WH = (L-1)
  W_BL = W_WH = (3*L)/4

  C_T = C_BL
  C_E = C_WH
  W_T = W_BL
  W_E = W_WH

  @memoize  
  def m(u, c, w):
    if u <= c-w:
      return 0.0
    elif c-w < u < c+w:
      return float(w-abs(u-c))/w
    else:
      return 0.0
  
  for y in xrange(height):
    print("%4.2f%%" % (100.0*float(y)/height))
    for x in xrange(width):
      l_lambda = []
      for r in rules:
        l_m = [1.0,] # 1 is min invariant
        
        for i in r:
          (dx,dy) = conn[i]
          vy = y+dy
          vx = x+dx
          if 0 <= vy < height and 0 <= vx < width:
            x_j = int(image[vy,vx])-int(image[y,x])
            l_m += (m(x_j, C_ZERO, W_ZERO),)
        
        l_lambda += (min(l_m),)
        
      lambda_T = max(l_lambda)
      lambda_E = 1.0-lambda_T
      
      v = (C_T*lambda_T*W_T+C_E*lambda_E*W_E)/(lambda_T*W_T+lambda_E*W_E)
      result[y,x] = v
  return result

I = numpy.asarray(Image.open("station.jpg").convert("L")).astype(numpy.uint8)

T = laplace(I)
Image.fromarray(T).save("laplace.png")

T = fuzzy_filter(I)
Image.fromarray(T).save("fuzzy.png")
