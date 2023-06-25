"""
Program for automatic A giver in terms of Q
"""

from __future__ import annotations
import time
import pyperclip
from typing import Any, NoReturn, Final
import json


class ClipboardMonitor:

    """
    A class to monitor and interact with clipboard.
    """

    def __init__(self, dict_qa: dict[str, str]) -> None:

        """
        Initializes ClipboardMonitor with a dictionary of questions and answers.
        """

        self.__dict_qa: Final[dict[str, str]] = dict_qa
        self.__answers: Final[set[str]] = set(dict_qa.values())
        self.__prev_data: str = str()
        pyperclip.copy(str())  # Clearing the clipboard

    @property
    def dict_qa(self) -> dict[str, str]:

        """
        Getter for the self.__dict_qa attribute.

        Returns:
            self.__dict_qa (dict[str, str]): The dictionary of questions and answers.
        """

        return self.__dict_qa

    @property
    def prev_data(self) -> str:

        """
        Getter for the self.__prev_data attribute.

        Returns:
            self.__prev_data (str): The lately saved clipboard contents as a string.

        """

        return self.__prev_data

    @prev_data.setter
    def prev_data(self, value: str) -> None:

        """
        Setter for the self.__prev_data attribute.

        Raises:
            TypeError: An exception is thrown if the new value type is not str.
        """

        if isinstance(value, str):
            self.__prev_data = value
        else:
            raise TypeError(f"value type should match {str}. {type(value)} given instead.")

    @property
    def answers(self) -> set[str]:

        """
        Getter for the self.__answers attribute
        """

        return self.__answers

    def check_clipboard(self) -> None:

        """
        Checks clipboard for any new data, if found matches with dict_qa and replaces with appropriate answer.
        """

        # Checks if clipboard contents have changed
        if (new_data := pyperclip.paste()) != self.prev_data:
            self.prev_data: str = new_data
            if self.prev_data in self.answers:
                return
            pyperclip.copy(self.dict_qa.get(new_data, 'NA'))

    def start_monitoring(self) -> None:

        """
        Starts monitoring the clipboard.
        """

        while True:
            try:
                self.check_clipboard()
                time.sleep(0.5)  # Reduces CPU usage by waiting for 0.5 seconds before checking clipboard again
            except KeyboardInterrupt:
                break


class _Main(type):

    """
    A metaclass for initialization of the Q and A.
    It'd be nice if the data were initialized during compile-time for the performance issues.
    """

    def __new__(mcs, name: Any, bases: Any, attrs: dict) -> _Main:
        attrs['dict_qa']: dict[str, str] = mcs.__dict_init()
        return super().__new__(mcs, name, bases, attrs)

    @staticmethod
    def __dict_init() -> dict[str, str]:

        """
        Method for initialization of QA dictionary

        Returns: the dictionary of QA

        """

        try:
            with open('dict_qa.txt', 'r') as file:
                return dict(json.loads(file.read().replace("'", '"')))
        except (FileNotFoundError, TypeError):
            return dict()


class Main(metaclass=_Main):

    """
    The main class for executing the program. The program is run within this class.

    Attributes:
        dict_qa (dict[str, str]): A dictionary mapping questions to their respective answers
    """

    dict_qa: Final[dict[str, str]] = ...

    @classmethod
    def main(cls) -> NoReturn:

        """
        The main method for the whole program execution.
        Initializes ClipboardMonitor object and uses ClipboardMonitor().start_monitoring() method for automation of
        Q and A.
        """

        ClipboardMonitor(cls.dict_qa).start_monitoring()


if __name__ == "__main__":
    Main.main()
