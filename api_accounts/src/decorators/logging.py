from functools import wraps

from api_players.src import app


def log_info(log_time=True, log_return=True):
    """ Save logs about execution of function to set log_file

    Parameters
    ----------
    log_time : bool, default = True
        Optional. Should time of executed function be logged.

    log_return : bool, default = True
        Optional. Should returned result of executed function be logged.
    """

    import logging
    import time
    from datetime import datetime

    def function_decorator(func):

        @wraps(func)
        def function_wrapper(*args, **kwargs):

            start = time.time()
            result = func(*args, **kwargs)
            stop = time.time()

            log = f"{datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S.%f')} | " \
                  f"Executing function named '{func.__name__}' " \
                  f"with args: {args} and kwargs: {kwargs}"

            if log_time:
                log += f" | execution time: {round(stop - start, 5)}s"
            if log_return and hasattr(result, "__str__"):
                log += f" | function returned: {result}"

            if hasattr(app, "config") and app.config.get("ENABLE_LOGGING", False):

                # Create (or get) unique loggers for each module
                logger = logging.getLogger(func.__module__)
                logger.setLevel(logging.INFO)

                if not logger.hasHandlers():
                    formatter = logging.Formatter("%(levelname)s | %(name)s | %(message)s")
                    file_handler = logging.FileHandler(app.config.get("API_Accounts_LOGGING_FILE", "../api_accounts_logs.log"))
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)

                logger.info(log)

            return result
        return function_wrapper
    return function_decorator
