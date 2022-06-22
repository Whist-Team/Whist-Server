"""Multi Thread adapter.."""
from anyio import run


# pylint: disable=too-few-public-methods
class ThreadManager:
    """
    Handles multi threads calls.
    """

    @staticmethod
    def run(func, *args, **kwargs) -> None:
        """
        Runs an async function in a new thread.
        :param func: to be called
        :param args: to be parsed to the call.
        :param kwargs: to be parsed to the call.
        :return: None
        """
        run(func(args, kwargs))
