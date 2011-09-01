from . import logger
import sys
import traceback

def run_script(f):
    ''' 
        Wrapper for script main function. 
        If an exception occurs, it exits with error and
        shows the exception. Otherwise it exits with 0.
        
    '''
    try:
        ret = f(sys.argv[1:])
        if ret is None:
            ret = 0
        try:
            ret = int(ret)
        except:
            logger.error('Cannot convert returned value %r to number.' % ret)
            ret = -1
        sys.exit(ret)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        sys.exit(-2) 
