from __future__ import absolute_import
from mobility import create_app
import os
import time

if os.path.exists('app_initialized'):
    os.remove('app_initialized')

time.sleep(5)

application = create_app()
