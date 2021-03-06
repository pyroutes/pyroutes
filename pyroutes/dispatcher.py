"""
The pyroutes Dispatcher class and supporting methods. Core handling code that
is run for all incoming requests.
"""

import pyroutes

from pyroutes.http.request import Request
import pyroutes.settings as settings

class Dispatcher(object):
    """
    The pyroutes Dispatcher object. An instance of this object is kept directly
    on the pyroutes module for all dispatching purposes.
    """

    def dispatch(self, environ, start_response):
        """
        Dispathes a request. The call signature is that of a standard WSGI
        application.
        """
        # Update site root value so pyroutes can make root-relative path
        # redirects
        if not hasattr(settings, 'SITE_ROOT'):
            settings.SITE_ROOT = environ.get('SCRIPT_NAME', '').rstrip('/')

        request = Request(environ)
        route = self.find_route(environ['PATH_INFO'], request)
        response = self.create_middleware_chain(route, request)
        headers = self._combine_headers(response)
        start_response(response.status_code, headers)

        if isinstance(response.content, basestring):
            if isinstance(response.content, unicode):
                response.content = response.content.encode('utf-8')
            return [response.content]
        else:
            return response.content

    def find_route(self, current_path, request=None):
        """
        Locates the route for the specified path. Return None if not found.
        """

        # If we don't have a current path, look for the root route.
        # See issue #2 <http://github.com/pyroutes/pyroutes/issues/2>
        complete_path = '/' + current_path.strip('/')
        current_path = '/%s/' % current_path.strip('/')

        while True:
            current_path = current_path[:current_path.rfind('/')] or '/'
            if current_path in pyroutes.__routes__:
                route = pyroutes.__routes__[current_path]
                argument_count = self._get_argument_count(
                        complete_path, current_path)
                if self._match_with_arguments(route, argument_count):
                    if request is not None:
                        request.matched_path = current_path
                    return route
            if current_path == '/':
                return

    @staticmethod
    def create_middleware_chain(route, request):
        """
        Builds the middleware chain. I.e. wrap the route in all the middlewares
        indicated in settings.MIDDLEWARE.
        """
        chain = route
        for full_path in reversed(settings.MIDDLEWARE):
            module_name, class_name = full_path.rsplit('.', 1)

            module = __import__(module_name, globals(), locals(), [class_name])
            middleware = getattr(module, class_name)

            chain = middleware(chain, route)

        return chain(request)

    @staticmethod
    def _get_argument_count(complete_path, current_path):
        """
        Returns the number of URL elements left over for between
        the current path and the complete path.
        """
        complete_path_comps = complete_path.rstrip('/').split('/')
        current_path_comps = current_path.rstrip('/').split('/')
        return len(complete_path_comps) - len(current_path_comps)

    @staticmethod
    def _match_with_arguments(route, arg_count):
        """
        Returns True if the number of remaining URL elements for the tested
        route matches the number of arguments for the route handler. It takes
        optional arguments and *args into account.
        """

        if route.variable_arguments is not None:
            return True

        defaults = len(route.variable_defaults or '')
        if arg_count <= route.required_argument_length and \
           route.required_argument_length <= (defaults + arg_count):
            return True
        return False

    @staticmethod
    def _combine_headers(response):
        """
        Combine "normal" http headers with the cookie headers into single list
        """
        return response.headers + response.cookies.cookie_headers
