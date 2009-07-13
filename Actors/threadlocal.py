import threading

# Since the actor model perscribes one thread
# per actor the current actor can be derived
# from this thread local variable
thread_local = threading.local()