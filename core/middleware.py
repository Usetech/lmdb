from django import http
from django.conf import settings

__author__ = 'sergio'


class FilterPersistMiddleware(object):
    def process_request(self, request):
        if request.method == 'POST':
            return None

        if 'HTTP_REFERRER' in request.META:
            referrer = request.META['HTTP_REFERRER'].split('?')[0]
            referrer = referrer.lstrip("http://")
            referrer = referrer[referrer.find('/'):len(referrer)]
        else:
            referrer = u''

        popup = 'pop=1' in request.META['QUERY_STRING']
        path = request.path
        query_string = request.META['QUERY_STRING']
        session = request.session

        if session.get('redirected', False):  # so that we don't loop once redirected
            del session['redirected']
            return None

        key = 'key'+path.replace('/', '_')
        if popup:
            key = 'popup'+key

        if path == referrer:
            # We are in the same page as before. We assume that filters were
            # changed and update them.
            if query_string == '':  # Filter is empty, delete it
                if key in session:
                    del session[key]
                return None
            else:
                request.session[key] = query_string
        else:
            # We are are coming from another page. Set querystring to
            # saved or default value.
            query_string = session.get(key)
            if query_string is not None:
                redirect_to = path+'?'+query_string
                request.session['redirected'] = True
                return http.HttpResponseRedirect(redirect_to)
            else:
                return None