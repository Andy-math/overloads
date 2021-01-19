# -*- coding: utf-8 -*-
import multiprocessing.pool
from typing import (Callable, Dict, List, Optional, Sequence, Text, Tuple, TypeVar, Union)

import psutil  # type: ignore

import tuplize
from capture_exceptions import Captured_Exception, capture_exceptions

param_t = TypeVar('param_t')
return_t = TypeVar('return_t')
pool: Optional[multiprocessing.pool.Pool] = None
output: List[str] = []


def launch_parpool() -> None:
    global pool
    multiprocessing.set_start_method('spawn')
    processes: int = psutil.cpu_count(logical=False)
    pool = multiprocessing.pool.Pool(processes)


def print(*values: object, sep: Text = ' ', end: Text = '\n') -> None:
    output.append(sep.join((str(value) for value in values)) + end)


def helper(
    info_tuple: Tuple[int, Callable[[param_t], return_t], param_t]
) -> Tuple[int, Union[return_t, Captured_Exception[return_t]], str]:
    idx, f, arg = info_tuple
    value = capture_exceptions(f, arg)
    output_str = ''.join(output)
    output.clear()
    return idx, value, output_str


def print_without_line_feed(*values: object) -> None:
    import builtins
    builtins.print(*values, end='')


def parfor(
    f: Callable[[param_t], return_t],
    arg_list: Sequence[param_t],
    *,
    callback: Optional[Callable[[Union[return_t, Captured_Exception[return_t]]], None]] = None,
    print_out: Optional[Callable[[Text], None]] = None,
    print_err: Optional[Callable[[Text], None]] = None  # force line wrap
) -> List[Union[return_t, Captured_Exception[return_t]]]:
    if print_out is None:
        print_out = print_without_line_feed
    if print_err is None:
        print_err = print_out
    if pool is None:
        launch_parpool()
        assert pool is not None
    helper_arg_list = ((idx, f, arg) for idx, arg in enumerate(arg_list))
    result_dict: Dict[int, Union[return_t, Captured_Exception[return_t]]] = {}
    for idx, result, output in pool.imap_unordered(helper, helper_arg_list):
        print_out(output)
        if isinstance(result, Captured_Exception):
            print_err('[{}]: {}\n'.format(idx, result))
        if callback is not None:
            callback(result)
        result_dict[idx] = result
    result_list = [result_dict[idx] for idx in range(len(arg_list))]
    return result_list


Numeric = Union[int, float]


@tuplize.tuplize_1
def show(x: Numeric) -> Numeric:
    import time
    time.sleep(0.1)
    print(multiprocessing.current_process(), x)
    assert x < 5, "x应当小于5"
    return x


if __name__ == '__main__':
    import builtins

    def mycallback(x: Union[Numeric, Captured_Exception[Numeric]]) -> None:
        if isinstance(x, (int, float)):
            builtins.print('[{}]'.format(x))

    builtins.print(parfor(show, [(x, ) for x in range(10)], callback=mycallback))
