"""
Example CLI module

Please DON'T import modules globally, import them in `run`.
Please DON'T initialize resource (e.g., variable) globally.
"""


def parser():
    """
    Initialize sub-parser.
    Parameters: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser
    """
    return {
        'help': 'this is dummy',
        'description': 'this is a basic example'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument(action="store", type=str, metavar="name", dest="name")
    parser.add_argument("-i", "--info", action="store", type=str, dest="info")
    parser.add_argument("-e", "--error", action="store_true", help="raise an error")


def run(name, info, error):
    """
    Arguments here should be defined in `add_arguments` first.
    The return value (integer) will be the return code in shell. It will set to 0 if no value returns.
    Though you can return a non-zero value to indicate error, raise exceptions defined in kgtk.exceptions is preferred
    since this gives user an unified error code and message.
    """
    # import modules locally
    import socket
    from kgtk.exceptions import KGTKException

    if error:
        raise KGTKException

    print('name: {}, info: {}\nhost: {}'.format(name, info, socket.gethostname()))
