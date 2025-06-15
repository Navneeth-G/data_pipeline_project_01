import time
from functools import wraps
from typing import Callable, Tuple, Type

class RetryHandler:
    def __init__(self, log_block: LogBlock):
        self.log_block = log_block
    
    def retry(self, max_attempts: int = 3, delay: float = 1.0, 
              exceptions: Tuple[Type[Exception], ...] = (Exception,)):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(1, max_attempts + 1):
                    try:
                        result = func(*args, **kwargs)
                        if attempt > 1:
                            self.log_block.info(
                                key="RETRY_SUCCESS",
                                message=f"{func.__name__} succeeded on attempt {attempt}"
                            )
                        return result
                    except exceptions as e:
                        if attempt == max_attempts:
                            self.log_block.error(
                                key="RETRY_FAILED",
                                message=f"{func.__name__} failed after {max_attempts} attempts: {str(e)}"
                            )
                            raise
                        
                        self.log_block.warning(
                            key="RETRY_ATTEMPT",
                            message=f"{func.__name__} failed attempt {attempt}/{max_attempts}: {str(e)}"
                        )
                        time.sleep(delay)
                        
            return wrapper
        return decorator

# Usage
log_block = LogBlock()
retry_handler = RetryHandler(log_block)

@retry_handler.retry(max_attempts=3, delay=2.0)
def api_call():
    # Your pipeline function
    pass

@retry_handler.retry(max_attempts=5, delay=1.0, exceptions=(ConnectionError, TimeoutError))
def database_operation():
    # Another pipeline function
    pass
