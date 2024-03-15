"""
Executé par le serveur web pour lancer l'application.
"""

from __future__ import absolute_import
from mobility import create_app
import time

time.sleep(5)

application = create_app()
