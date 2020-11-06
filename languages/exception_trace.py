import sys
import traceback

class Error(Exception):
    """Base class for other exceptions"""
    pass

def divideby0():
    print(1 / 0)

def useNone():
    value = None
    value[0] = 1

# https://docs.python.org/ko/3/library/exceptions.html
def raiseError():
    # raise BaseException('BaseException')
    raise Exception('Exception')

def raiseCustomError():
    # raise BaseException('BaseException')
    raise Error('custom exception')

def catch(handler):
    print('catch:********')
    try:
        handler()
    except ZeroDivisionError as err:
        print(err)
    except Exception as err:
        print(err)
    except:
        for i in range(len(sys.exc_info())):
            print(i, ':')
            print(sys.exc_info()[i])
        print("trace:")
        traceback.print_exc()


catch(divideby0)
catch(useNone)
catch(raiseError)
catch(raiseCustomError)