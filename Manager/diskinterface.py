import threading

__lock = threading.Lock()


def save_to_disk(self, module_name, module_src):
    self.__lock.acquire()
    name = '/tmp/actor-%s' % module_name
    file = open(name, 'w')
    file.write(module_src)
    file.flush()  
    file.close()
    __lock.release()
    return name

def get_from_disk(self, file_name):
    self.__lock.acquire()
    file = open(file_name, 'r')
    module_src = file.read()
    file.close()
    __lock.release()
    return module_src

    
def import_from_disk(self, module_name, file_name):
    
    imp.acquire_lock()
    imp.load_source(modulename, name)
    imp.release_lock()