class LoggingEnable:
    def __init__(self) -> None:
        pass

    def __enter__(self):
        import logging
 
        try:
            # For Python 3
            import http.client as http_client
        except ImportError:
            # For Python 2 users
            import httplib as http_client
        
        # Turn verbosity on with debugging
        http_client.HTTPConnection.debuglevel = 1
        
        # You must initialize logging, otherwise you'll not see debug output.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        return self

    # ...

    def __exit__(self, exc_type, exc_value, traceback):
        