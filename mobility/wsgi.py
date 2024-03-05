from __future__ import absolute_import
from mobility import create_app
import os
import time

if os.path.exists('app_initialized'):
    try:
        os.remove('app_initialized')
    except:
        pass

time.sleep(5)

application = create_app()
