import sys


def error_handle(e):
    try:
        cnx
    except NameError:
        pass
    else:
        cnx.close()
        print("Mysql Connection Closed due to error")

    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(exc_type, exc_obj, " - on line:", exc_tb.tb_lineno)
    print(repr(e))
