#!/usr/bin/env python3
"""Deletion‑resilient hypermedia pagination module."""

import csv
import math
from typing import List, Tuple, Dict, Optional


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Return start and end indexes for a given page and page size."""
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self) -> None:
        """Initialize the server with no cached dataset."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Load and cache the dataset from CSV file."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # skip header
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Return dataset indexed by original position (0..len-1).
        Simulates deletions by allowing entries to be None.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] if i < len(dataset) else None
                for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Return one page of data using simple pagination."""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        start, end = index_range(page, page_size)
        data = self.dataset()
        if start >= len(data):
            return []
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Return hypermedia metadata for simple pagination."""
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

    def get_hyper_index(self, index: Optional[int] = None, page_size: int = 10) -> Dict:
        """
        Return a page resilient to deletions.

        Args:
            index (int, optional): Starting index (0-indexed). Defaults to 0.
            page_size (int): Desired number of items per page.

        Returns:
            Dict: Contains index, next_index, page_size, data.
        """
        indexed_ds = self.indexed_dataset()
        total_length = len(indexed_ds)

        if index is None:
            index = 0
        assert 0 <= index < total_length, "Index out of range"

        data = []
        current = index
        while len(data) < page_size and current < total_length:
            item = indexed_ds.get(current)
            if item is not None:
                data.append(item)
            current += 1

        next_index = current if current < total_length else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data,
        }
