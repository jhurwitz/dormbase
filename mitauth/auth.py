"""
Based very heavily on http://web.mit.edu/snippets/django/mit/__init__.py
"""

from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth.models import User
from django.contrib.auth.views import login as login_view
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.http import HttpResponseRedirect
from django.conf import settings

import ldap
import ldap.filter

class CertificateRemoteUserMiddleware(RemoteUserMiddleware):
    header = 'SSL_CLIENT_S_DN_Email'

class CertificateRemoteUserBackend(RemoteUserBackend):
    def clean_username(self, username, ):
        if '@' in username:
            name, domain = username.split('@')
            assert domain.upper() == 'MIT.EDU'
            return name
        else:
            return username

    def configure_user(self, user, ):
        username = user.username
        user.set_unusable_password()
        con = ldap.open('ldap-too.mit.edu')
        con.simple_bind_s("", "")
        dn = "dc=mit,dc=edu"
        fields = ['cn', 'sn', 'givenName', 'mail', ]
        userfilter = ldap.filter.filter_format('uid=%s', [username])
        result = con.search_s('dc=mit,dc=edu', ldap.SCOPE_SUBTREE, userfilter, fields)
        if len(result) == 1:
            user.first_name = result[0][1]['givenName'][0]
            user.last_name = result[0][1]['sn'][0]
            try:
                user.email = result[0][1]['mail'][0]
            except KeyError:
                user.email = username + '@mit.edu'
        else:
            raise ValueError, ("Could not find user with username '%s' (filter '%s')"%(username, userfilter))
        user.save()
        return user

class CertificateFreeTestingBackend(object):
    def authenticate(self, username=None):
        if not settings.DEBUG:
            return None
        try:
            user = CertificateRemoteUserBackend().authenticate(username)
        except ValueError:
            # no User and no LDAP match
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def scripts_login(request, **kwargs):
    host = request.META['HTTP_HOST'].split(':')[0]

    # this part based on django.contrib.auth.views.login
    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
        request.GET.get(REDIRECT_FIELD_NAME, ''))
    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

    if host in ('localhost', '127.0.0.1'):
        """
        On localhost we can't use certificates, so we'll show a login form
        (username field only, no password). Any username is accepted, as long
        as it either (a) exists already in User, or (b) matches an LDAP user.
        This isn't secure (we can impersonate anyone!) but works great for
        testing.
        """
        assert settings.DEBUG
        if request.method == "POST":
            username = request.POST.get('username', '')
            user = authenticate(username=username)
            if user is not None and user.is_active:
                # login succeeded!
                login(request, user)
                return HttpResponseRedirect(redirect_to)
        # show the login page
        return login_view(request, **kwargs)

    elif request.META['SERVER_PORT'] != '444':
        """
        We're (presumably) on a server that can accept certificates, so let's
        switch to port 444 so the certificate is sent.
        """
        redirect_to = "https://%s:444%s" % (host, request.META['PATH_INFO'], )
        return HttpResponseRedirect(redirect_to)

    else:
        """
        Thanks to RemoteUserMiddleware magic, the certificate has already been
        read, and a User objected (created on-the-spot, if necessary) is now
        in request.user.
        """
        if request.user.is_authenticated():
            # middleware logged us in
            return HttpResponseRedirect(redirect_to)
        else:
            # didn't work, show the login page again
            return login_view(request, **kwargs)
