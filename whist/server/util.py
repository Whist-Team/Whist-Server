"""Multi Thread adapter.."""
import asyncio

# pylint: disable=too-few-public-methods
class ThreadManager:
    """
    Handles multi threads calls.
    """

    @staticmethod
    def run(func, args) -> None:
        """
        Runs an async function in a new thread.
        :param func: to be called
        :param args: to be parsed to the call.
        :return: None
        """
        loop = asyncio.new_event_loop()
        loop.run_until_complete(func(args))
