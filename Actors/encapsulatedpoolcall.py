from threadlocal import thread_local
import itertools

class EncapsulatedPoolCall(object):
  
  def __init__(self, sources, method, ref_to_ref):
    self.__sources = sources
    self.__method = method
    self.__ref_to_ref = ref_to_ref
  
  def __call__(self, *args, **kwds):
    # Pre: all lists in args are the same length
    # this constrasts to python whoose map inserts None if
    # lacking in length.
    # I think the behaviour to auto-repeat a non-list
    # would be nice, ala partial functions in Haskell.
    num_of_args = len(args)
    length_of_args = len(args[0])
    results = list()
    # Try producing a cyclic iterator in one line in Java :-)
    sources_iter = itertools.cycle(self.__sources)
    actor = thread_local.actor
    for i in range(0, length_of_args):   
      arg_group = list()
      for j in range(0, num_of_args):
        arg_group.append(args[j][i])
      actorid = sources_iter.next()
      print 'sent msg: ' + str(i) + ' to ' + actorid
      (val, actor_id) = actor.sendmessage(actorid, self.__method, arg_group, kwds)
      results.append(val)
      if actor_id:
        self.__ref_to_ref.actor_ids[i] = actor_id
    return results

class EncapsulatedRepeatedPoolCall(object):
	
  def __init__(self, sources, method):
    self.__sources = sources
    self.__method = method
  
  def __call__(self, *args, **kwds):
	results = list()
	actor = thread_local.actor
	for source in self.__sources:
		(val, actor_id) = actor.sendmessage(source, self.__method, args, kwds)
		results.append(val)
	return results