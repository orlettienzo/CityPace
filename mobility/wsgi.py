from __future__ import absolute_import
from mobility import create_app
import os
import time
# from mobility.models.appdata_model import get_db_populated

# if not get_db_populated(): # if the database is not populated, allow the app to populate it
if os.path.exists('app_initialized'):
    try:
        os.remove('app_initialized')
    except:
        pass

time.sleep(5)

application = create_app()
