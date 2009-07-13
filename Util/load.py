import os
try:
  import multiprocessing as mp
  num_cores = mp.cpu_count()
except:
  num_cores = 1

def load_avg():
  return os.getloadavg()[0]

def is_underloaded():
  # TODO: currently for the node rather than core
  max = num_cores * 0.75
  return (load_avg() < max)