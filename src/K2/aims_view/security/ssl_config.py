"""
SSL configuration bypass for enterprise environments
This must be imported before any HTTP libraries (CrewAI, litellm, etc.)
"""

import os
import ssl
import warnings
import urllib3


def configure_ssl_bypass():
    """
    Configure comprehensive SSL bypass for enterprise environments
    This must be called BEFORE any imports of CrewAI, litellm, or other HTTP libraries
    """
    
    # Disable SSL warnings globally
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    warnings.filterwarnings('ignore', category=UserWarning)
    
    # Set global environment variables for SSL bypass
    os.environ['POSTHOG_DISABLED'] = '1'
    os.environ['OTEL_SDK_DISABLED'] = 'true'
    os.environ["PYTHONHTTPSVERIFY"] = "0"
    os.environ["LITELLM_SSL_VERIFY"] = "false"
    os.environ["REQUESTS_CA_BUNDLE"] = ""
    os.environ["CURL_CA_BUNDLE"] = ""
    os.environ["SSL_VERIFY"] = "false"
    
    # Create unverified SSL context globally
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except AttributeError:
        # Handle case where this attribute doesn't exist
        pass
    
    # Additional SSL bypass for httpx (used by litellm)
    try:
        import httpx
        # Monkey patch httpx to disable SSL verification
        original_build = httpx.HTTPTransport.__init__
        def patched_build(self, *args, **kwargs):
            kwargs['verify'] = False
            return original_build(self, *args, **kwargs)
        httpx.HTTPTransport.__init__ = patched_build
    except ImportError:
        pass
    
    # Additional SSL bypass for requests library
    try:
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        # Create a session with SSL disabled
        class SSLDisabledHTTPAdapter(HTTPAdapter):
            def init_poolmanager(self, *args, **kwargs):
                kwargs['ssl_context'] = ssl.create_default_context()
                kwargs['ssl_context'].check_hostname = False
                kwargs['ssl_context'].verify_mode = ssl.CERT_NONE
                return super().init_poolmanager(*args, **kwargs)
        
        # Monkey patch requests to disable SSL globally
        original_session = requests.Session
        def patched_session(*args, **kwargs):
            session = original_session(*args, **kwargs)
            session.verify = False
            adapter = SSLDisabledHTTPAdapter()
            session.mount('https://', adapter)
            session.mount('http://', adapter)
            return session
        
        requests.Session = patched_session
    except ImportError:
        pass
    
    # Final SSL bypass specifically for litellm
    try:
        import litellm
        # Set litellm specific SSL bypass
        litellm.verify = False
        # Also try to patch litellm's internal client if accessible
        if hasattr(litellm, 'client'):
            litellm.client.verify = False
    except ImportError:
        pass


# Auto-configure SSL bypass when module is imported
configure_ssl_bypass()
