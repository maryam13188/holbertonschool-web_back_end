#!/usr/bin/env python3
"""Simple pagination module that provides pagination for a CSV dataset."""

import csv
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate start and end indices for a given page and page size.

    Args:
        page (int): 1-indexed page number
        page_size (int): number of items per page

    Returns:
        Tuple[int, int]: a tuple (start_index, end_index)
    """
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self) -> None:
        """Initialize the server with no cached dataset."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Load and cache the dataset from CSV file.

        Returns:
            List[List]: the dataset as a list of rows (excluding header)
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as file:
                reader = csv.reader(file)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # skip header row
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieve a specific page of the dataset.

        Args:
            page (int): page number (1-indexed, must be > 0)
            page_size (int): number of items per page (must be > 0)

        Returns:
            List[List]: list of rows for the requested page, or empty list if out of range

        Raises:
            AssertionError: if page or page_size is not a positive integer
        """
        assert isinstance(page, int) and page > 0, "page must be a positive integer"
        assert isinstance(page_size, int) and page_size > 0, "page_size must be a positive integer"

        start, end = index_range(page, page_size)
        data = self.dataset()

        if start >= len(data):
            return []
        return data[start:end]
