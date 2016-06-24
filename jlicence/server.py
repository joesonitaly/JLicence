import datetime
import json

from django.conf import settings
from django.core.signing import Signer

from . import licenceFile, client, provider


def generateLicence(expires, file=licenceFile, key=settings.SECRET_KEY, client=client, provider=provider, created=datetime.datetime.now()):
   """
   Creates a licence file.

   Parameters:
      - expires (datetime): the licence expiration date.
      - file (string): the path to the licence file.
      - key (string): the cryptographic signing key (the same key is used for signing and unsigning).
      - client (string): the licence client.
      - provider (string): the licence provider.
      - created (datetime): the licence creation date.

   Returns:
      - None
   """

   licence = {
                "CLIENT": str(client),
                "PROVIDER": str(provider),
                "CREATED": str(created)[:-7],
                "EXPIRES": str(expires)[:-7],
             }

   with open(file, "w") as f:
      f.write(Signer().sign(json.dumps(licence, indent=3) + "\n"))
