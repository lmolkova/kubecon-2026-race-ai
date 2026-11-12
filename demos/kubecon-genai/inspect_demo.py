"""Fetch a trace from Aspire and execute the talk queries locally."""

import argparse
import json

from aspire_capture import DASHBOARD, capture, ground_truth, open_database, query


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default=":memory:", help="Optional local SQLite output file")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--run-id")
    selection.add_argument("--trace-id")
    args = parser.parse_args()
    db = open_database(args.db)
    try:
        trace_id = capture(db, run_id=args.run_id, trace_id=args.trace_id)
        print(f"Trace: {DASHBOARD}/traces/detail/{trace_id}")
        if args.run_id:
            print("Model-router request totals:")
            print(json.dumps(ground_truth(args.run_id), indent=2))
        for name in ("01-semconv.sql", "02-normalized.sql"):
            print(name)
            print(json.dumps(query(db, name, trace_id), indent=2))
    finally:
        db.close()


if __name__ == "__main__":
    main()
