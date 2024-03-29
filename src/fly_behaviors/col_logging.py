import logging; logging.basicConfig()
import platform

def add_coloring_to_emit_ansi(fn):
    # add methods we need to the class
    def new(*args):
        levelno = args[1].levelno
        if(levelno >= 50):
            color = '\x1b[31m' # red
        elif(levelno >= 40):
            color = '\x1b[31m' # red
        elif(levelno >= 30):
            color = '\x1b[33m' # yellow
        elif(levelno >= 20):
            color = '\x1b[32m' # green 
        elif(levelno >= 10):
            color = '\x1b[35m' # pink
        else:
            color = '\x1b[0m' # normal
        args[1].msg = color + str(args[1].msg) + '\x1b[0m'  # normal
        return fn(*args)
    return new

if platform.system() != 'Windows':
    logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)


logger = logging.getLogger("fly_behaviors")
logger.setLevel(logging.DEBUG)
