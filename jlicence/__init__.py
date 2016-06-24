from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


try:
   setting = settings.JLICENCE
except AttributeError:
   raise ImproperlyConfigured("Please verify that this project contains a JLICENCE setting.")

try:
   licenceFile = setting["LICENCE"]
except KeyError:
   throwImproperlyConfigured("LICENCE")

try:
   timestampFile = setting["TIMESTAMP"]
except KeyError:
   throwImproperlyConfigured("TIMESTAMP")

try:
   client = setting["CLIENT"]
except KeyError:
   throwImproperlyConfigured("CLIENT")

try:
   provider = setting["PROVIDER"]
except KeyError:
   throwImproperlyConfigured("PROVIDER")


def throwImproperlyConfigured(key):
   raise ImproperlyConfigured("Please verify that the JLICENCE project setting contains a %s key with a valid value." % key)
