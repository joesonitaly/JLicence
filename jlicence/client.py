import datetime
import json

from os.path import exists, isfile

from django.core.signing import BadSignature, Signer
from django.utils.dateparse import parse_datetime

from . import setting, licenceFile, timestampFile, client, provider


class IncorrectSystemClock(Exception):
   pass


def licenceExists():
   """
   Checks if the licence file exists and is a regular file.

   Returns:
      - Boolean
   """

   updateTimestamp()
   return exists(licenceFile) and isfile(licenceFile)


def licenceIsValid():
   """
   Checks if the licence validity period has not been exceeded.

   Returns:
      - Boolean
   """

   updateTimestamp()

   if not licenceExists():
      return False

   licence = getLicense()

   with open(timestampFile, "r") as f:
      savedTimestamp = parse_datetime(f.read().strip())

   return (savedTimestamp >= parse_datetime(licence["CREATED"])) and (savedTimestamp < parse_datetime(licence["EXPIRES"])) and (provider == licence["PROVIDER"]) and (client == licence["CLIENT"])


def updateTimestamp():
   """
   Must be called after every login or logout attempt and/or periodically.
   Ensures that the system clock continues to tick forward in time, using a saved timestamp.

   Returns:
      - None

   Exceptions:
      - IncorrectSystemClock(), if the current system time is less than the saved timestamp.
   """

   now = datetime.datetime.now()

   try:
      with open(timestampFile, "r+") as f:
         savedTimestamp = parse_datetime(f.read().strip())

         if savedTimestamp:
            if now >= savedTimestamp:
               f.seek(0, 0)
               f.truncate()
               f.write(str(now)[:-7])
            else:
               raise IncorrectSystemClock("Please set your system clock to at least %s." % str(savedTimestamp)[:-7])
         else:
            raise IOError
   except IOError:
      with open(timestampFile, "w") as f:
         licence = getLicense()

         if now >= parse_datetime(licence["CREATED"]):
            f.write(str(now)[:-7])
         else:
            f.write(str(parse_datetime(licence["CREATED"]))[:-7])


def getLicense():
   with open(licenceFile, "r") as f:
      return json.loads(Signer().unsign(f.read().strip()))
