import pkg_resources
import io
 
 
class RessourceError(EnvironmentError):
 
    def __init__(self, msg, error):
        super().__init__(msg)

def binary_resource_stream(resource, location):
    """ Return a resource from this path or package """
        # Assume location is a module and try to load it using pkg_resource
    try:
        return pkg_resources.resource_stream(location, resource)
    except (ImportError, EnvironmentError) as e:
        msg = ('Unable to find resource "%s" in "%s". ')
        raise RessourceError(msg % (resource, location), e)

def filename_resource(resource, location):
    # Assume location is a module and try to load it using pkg_resource
    try:
        return pkg_resources.resource_filename(location, resource)
    except (ImportError, EnvironmentError) as e:
        msg = ('Unable to find resource "%s" in "%s". ')
        raise RessourceError(msg % (resource, location), e)
 
def text_resource_stream(path, location, encoding="utf8", errors=None,
                    newline=None, line_buffering=False):
    """ Return a resource from this path or package. Transparently decode the stream. """
    stream = binary_resource_stream(path, location)
    return io.TextIOWrapper(stream, encoding, errors, newline, line_buffering)
