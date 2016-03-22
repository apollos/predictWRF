import inspect
import sys
def line():
    try:
            raise Exception
    except:
            return sys.exc_info()[2].tb_frame.f_back.f_lineno
def file():
    return inspect.currentframe().f_code.co_filename
 
if __name__ == '__main__':
    print "%s: %d" % (file(), line())

