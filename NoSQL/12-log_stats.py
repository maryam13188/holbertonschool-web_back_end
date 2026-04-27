#!/usr/bin/env python3
"""
Module to provide statistics about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def get_nginx_stats():
    """
    Connect to MongoDB, query the logs.nginx collection,
    and print statistics about the logs.
    """
    # Connect to MongoDB (default localhost:27017)
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Total number of logs
    total_logs = collection.count_documents({})

    # Count methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts[method] = collection.count_documents({"method": method})

    # Count GET with path=/status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})

    # Print results (exactly as in the example)
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    get_nginx_stats()
