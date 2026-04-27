#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination module."""

import csv
from typing import Dict, List, Optional


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self) -> None:
        """Initialize server with no cached datasets."""
        self.__dataset = None
        self.__indexed_dataset = None

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

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Return dataset indexed by original insertion order (starting at 0).

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
                "next_index": int (next starting index for next page)
            }

        Raises:
            AssertionError: if index is out of range or not an integer.
        """
        if index is None:
            index = 0

        indexed_data = self.indexed_dataset()
        max_index = max(indexed_data.keys())

        assert isinstance(index, int) and 0 <= index <= max_index

        data = []
        next_index = index

        while len(data) < page_size and next_index <= max_index:
            if next_index in indexed_data:
                data.append(indexed_data[next_index])
            next_index += 1

        return {
            "index": index,
            "data": data,
            "page_size": len(data),
            "next_index": next_index,
        }
