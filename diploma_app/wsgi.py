import os
import time
import traceback
import signal
import sys
from django.core.wsgi import get_wsgi_application
# attempt to solve issue with drf_spectacular
try:
    application = get_wsgi_application()
    print('WSGI without exception')
except Exception:
    print('handling WSGI exception')
    traceback.print_exc()
    os.kill(os.getpid(), signal.SIGINT)
    time.sleep(2.5)
