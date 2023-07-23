import functools
from asyncio import events
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any, TypeVar

T = TypeVar("T")


async def to_subthread(func: Callable[..., T], /, *args: Any, **kwargs: Any) -> T:
    """I/Oバウンドなブロッキング処理の関数をコルーチンに変換して実行"""
    loop = events.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=1)
    func_call = functools.partial(func, *args, **kwargs)
    return await loop.run_in_executor(executor, func_call)


async def to_subprocess(func: Callable[..., T], /, *args: Any, **kwargs: Any) -> T:
    """CPUバウンドなブロッキング処理の関数をコルーチンに変換して実行

    Pythonのプロセス間通信の仕様上、渡せる値と戻り値は Picklable な値のみです
    lambda式やモジュールトップレベル以外で定義された関数やクラスは渡せません
    https://docs.python.org/ja/3/library/pickle.html#what-can-be-pickled-and-unpickled
    """
    loop = events.get_running_loop()
    executor = ProcessPoolExecutor(max_workers=1)
    func_call = functools.partial(func, *args, **kwargs)
    return await loop.run_in_executor(executor, func_call)
