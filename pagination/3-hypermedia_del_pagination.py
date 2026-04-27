#!/usr/bin/env python3
"""Deletion‑resilient hypermedia pagination module."""

import csv
from typing import List, Dict, Optional


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self) -> None:
        """Initialize the server with no cached datasets."""
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Load and cache the dataset from CSV.

        Returns:
            List[List]: dataset rows excluding header.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]  # skip header
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Return dataset indexed by original insertion order.

        Returns:
            Dict[int, List]: mapping index -> row.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i] for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: Optional[int] = None, page_size: int = 10) -> Dict:
        """
        Return a deletion‑resilient page starting from a given index.

        Args:
            index (Optional[int]): starting index (0‑based). Defaults to 0.
            page_size (int): desired number of items per page.

        Returns:
            Dict: {
                "index": int (the provided index),
                "data": List[List] (collected rows),
                "page_size": int (actual number of rows returned),
                "next_index": int|None (next index to use for next page)
            }

        Raises:
            AssertionError: if index is out of range.
        """
        if index is None:
            index = 0

        indexed = self.indexed_dataset()
        max_idx = max(indexed.keys()) if indexed else -1
        assert isinstance(index, int) and 0 <= index <= max_idx, "Index out of range"

        data = []
        current = index
        while len(data) < page_size and current <= max_idx:
            if current in indexed:
                data.append(indexed[current])
            current += 1

        next_index = current if current <= max_idx else None

        return {
            "index": index,
            "data": data,
            "page_size": len(data),
            "next_index": next_index,
        }
