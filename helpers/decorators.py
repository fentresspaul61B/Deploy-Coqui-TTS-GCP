import time
from datetime import datetime
from functools import wraps
from typing import Callable, List, Any
import inspect
from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionCallSummary:
    function_name: str
    source_file: str
    call_time: str
    input_args: tuple
    input_kwargs: dict
    input_types: List[str]
    output_type: str
    duration: float


def print_summary(summary: FunctionCallSummary) -> None:
    print("--------------------------------------------------------------")
    print(f"Function Name: {summary.function_name}")
    print(f"Source File: {summary.source_file}")
    print(f"Call Time: {summary.call_time}")
    print("Input Arguments:", summary.input_args)
    print("Input Keyword Arguments:", summary.input_kwargs)
    print("Input Data Types:", summary.input_types)
    print("Output Data Type:", summary.output_type)
    print(f"Execution Time: {summary.duration}")
    print("--------------------------------------------------------------")


def get_source_file():
    """Returns the filepath where a specific function was called from."""
    frame = inspect.currentframe()
    outer_frames = inspect.getouterframes(frame)
    file_path = outer_frames[1].filename
    return file_path


def get_input_types(args, kwargs) -> list:
    """Returns a list of the python data types of the input arguments."""
    input_types = [type(arg).__name__ for arg in args] + \
        [f"{key}: {type(value).__name__}" for key, value in kwargs.items()]
    return input_types


def call_and_time_func(func: Callable, args, kwargs) -> tuple[Any, time.time]:
    """Calls a function and returns the output and duration to execute."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    duration = end_time - start_time
    return result, duration


def log_data(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        result, duration = call_and_time_func(func, args, kwargs)

        # ic the collected information
        summary = FunctionCallSummary(
            function_name=func.__name__,
            source_file=get_source_file(),
            call_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            input_args=args,
            input_kwargs=kwargs,
            input_types=get_input_types(args, kwargs),
            output_type=type(result).__name__,
            duration=duration
        )
        print_summary(summary)
        return result

    return wrapper
