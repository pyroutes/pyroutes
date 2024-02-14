#!/usr/bin/env python
# encoding: utf-8

"""
Contains all the examples from the «Let’s do it! (aka Quickstart)» section of
the pyroutes documentation. Handy if you find it a waste of time copying and
pasting the code ;)
"""

import os

from pyroutes import application, route
from pyroutes.http.response import Response, Http403, Http404


@route('/')
def index(_):
    return 'Hello world!'


@route('/sayhello')
def sayhello(_, name='world'):
    return 'Hello %s!' % name


@route('/archive')
def archive(_, year, month=None, day=None):
    return 'Year: %s  Month: %s  Day: %s' % (year, month, day)


@route('/pathprint')
def pathprint(_, *args):
    return 'User requested /%s under /pathprint' % '/'.join(args)


@route('/newpost')
def new_post(request):
    if 'image' in request.FILES:
        # Do stuff with image
        filename, data = request.FILES['image']
        data = data.read()
    category = request.GET.get('category', 'default')
    title = request.POST.get('title', None)
    if not title:
        return 'No title!'
    return 'OK'


@route('/pdf')
def pdf(_):
    with open('mypdf.pdf') as fh:
        return Response(fh, [('Content-Type', 'application/pdf')])


@route('/decrypt_file')
def decrypt_file(request, filename, key):
    full_filename = os.path.join('secrets_folder', filename)
    if not os.path.exists(full_filename):
        raise Http404({'#details': 'No such file "%s"' % filename})
    try:
        return decrypt(full_filename, key)
    except KeyError:
        raise Http403({'#details': 'Key did not match file'})


@route('/cookie-set')
def set_cookies(request, message='Hi!'):
    response = Response('Cookies set!')
    response.cookies.add_cookie('logged_in', 'true')
    # Insecure cookie setting
    response.cookies.add_unsigned_cookie('message', message)
    return response


@route('/cookie-get')
def get_cookies(request):
    logged_in = request.COOKIES.get_cookie('logged_in')
    message = request.COOKIES.get_unsigned_cookie('message')
    if logged_in:
        return message
    raise Http403({'#details': 'Go away!'})


@route('/cookie-del')
def del_cookies(_):
    response = Response('Cookies deleted!')
    response.cookies.del_cookie('logged_in')
    response.cookies.del_cookie('message')
    return response


if __name__ == '__main__':
    from pyroutes import utils
    route('/media')(utils.fileserver)
    utils.devserver(application)
