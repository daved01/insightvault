from typing import TypeVar, Union, List, Callable
from functools import wraps

T = TypeVar('T')

def ensure_list(arg_name: str = 'documents') -> Callable:
    """Decorator to ensure an argument is a list
    
    Args:
        arg_name: The name of the argument to check/convert
        
    Returns:
        Decorator function that ensures the argument is a list
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if the argument exists in kwargs
            if arg_name in kwargs:
                value = kwargs[arg_name]
                if not isinstance(value, list):
                    kwargs[arg_name] = [value]
            # Check if it's a positional argument
            else:
                # Get the function's parameter names
                import inspect
                params = inspect.signature(func).parameters
                param_names = list(params.keys())
                
                # Find position of our target argument
                try:
                    arg_pos = param_names.index(arg_name)
                    # If we have enough positional args and the target isn't a list
                    if len(args) > arg_pos and not isinstance(args[arg_pos], list):
                        args = list(args)  # Convert tuple to list for modification
                        args[arg_pos] = [args[arg_pos]]
                        args = tuple(args)  # Convert back to tuple
                except ValueError:
                    pass  # Argument not found in parameters
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
