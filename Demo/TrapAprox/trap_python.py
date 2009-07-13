import time
import math
import sys

def main(trapezoids):
  start = time.time()
  result = approximate(trapezoids, 0, 20)
  end = time.time()
  print "Result: %s Runtime: %s" % (result, end - start)

def approximate(n, lower, upper):
    result = 0.0
    h = (upper - lower) / float(n)
    for i in range(1, n+1):
      result += (f(xi(i, h)) + f(xi(i+1, h))) * (h / 2)
    return result
  
def f(x):
  #return 5*(x**4)
  return (math.sin(x**3.0-1.0)/(x+1))*math.sqrt(1.0+math.exp(math.sqrt(2.0*x)))
    
def xi(i, h):
  return (i-1) * h
    
if __name__ == '__main__':
  main(int(sys.argv[1]))