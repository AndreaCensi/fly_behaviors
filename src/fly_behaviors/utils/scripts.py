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
        logger.debug('Graceful exit with return code %d.' % ret)
        if ret is None:
            ret = 0
        sys.exit(ret)
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
        sys.exit(-2) 
