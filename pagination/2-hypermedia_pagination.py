#!/usr/bin/env python3
"""Hypermedia pagination module for popular baby names dataset."""

import csv
import math
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate start and end indexes for a given page.

    Args:
        page (int): 1-indexed page number.
        page_size (int): Number of items per page.

    Returns:
        Tuple[int, int]: start index, end index.
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
            List[List]: dataset rows (excluding header).
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # skip header
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Return one page of data.

        Args:
            page (int): page number (1-indexed, > 0).
            page_size (int): number of items per page (> 0).

        Returns:
            List[List]: list of rows for the requested page, or empty list if out of range.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start, end = index_range(page, page_size)
        data = self.dataset()
        if start >= len(data):
            return []
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Return hypermedia dictionary for pagination.

        Args:
            page (int): current page number.
            page_size (int): desired number of items per page.

        Returns:
            Dict: {
                "page_size": int (actual length of data),
                "page": int,
                "data": List[List],
                "next_page": int or None,
                "prev_page": int or None,
                "total_pages": int
            }
        """
        data = self.get_page(page, page_size)
        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages,
        }
