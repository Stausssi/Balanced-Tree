"""
This file contains utility methods, which fall under neither GUI nor Tree.
"""
import os.path


def readCSV(path) -> str:
    """
    This method reads a given CSV file and returns the content as a string.

    Args:
        path (str): The path to the CSV file

    Returns:
        str: The contents of the file

    Raises:
        FileNotFoundError: If the given path doesn't exist
    """

    if os.path.isfile(path) and path.lower().endswith(".csv"):
        with open(path) as file:
            return file.read()
    else:
        raise FileNotFoundError(f"No CSV file found at {path}!")
