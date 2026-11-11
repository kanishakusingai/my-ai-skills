#!/usr/bin/env python3
"""Merge Helium 10 keyword CSVs, deduplicate exports and rank observed phrases."""
import argparse
import hashlib
from pathlib import Path
import sys

import pandas as pd


def read_export(path):
    frame = pd.read_csv(path, encoding="utf-8-sig")
    frame.columns = [name.strip().casefold() for name in frame.columns]

    def column(*names):
        for name in names:
            if name in frame:
                return frame[name]
        return pd.Series(index=frame.index, dtype=object)

    if not {"keyword phrase", "keyword"}.intersection(frame.columns):
        raise SystemExit(f"No keyword column found in {path}. Columns: {list(frame.columns)}")

    def numeric(name):
        cleaned = column(name).astype(str).str.replace(",", "", regex=False)
        return pd.to_numeric(cleaned, errors="coerce")

    phrases = column("keyword phrase", "keyword").fillna("").astype(str)
    bids = column("suggested ppc bid", "ppc").astype(str).str.replace(",", "", regex=False)
    first_amount = bids.str.extract(r"(\d+(?:\.\d+)?|\.\d+)", expand=False)
    return pd.DataFrame({
        "keyword": phrases.str.casefold().str.split().str.join(" "),
        "volume": numeric("search volume"),
        "bid": pd.to_numeric(first_amount, errors="coerce"),
        "competition": numeric("competing products"),
        "rank": numeric("organic rank"),
        "source": path,
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--top", type=int, default=300)
    args = parser.parse_args()

    frames = []
    seen = {}
    for path in args.files:
        digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        if digest in seen:
            print(f"Duplicate export skipped: {path} (same as {seen[digest]})", file=sys.stderr)
            continue
        seen[digest] = path
        frames.append(read_export(path))

    data = pd.concat(frames, ignore_index=True)
    groups = data.loc[data["keyword"] != ""].groupby("keyword")
    result = groups.agg(
        search_volume=("volume", "max"),
        suggested_bid=("bid", "max"),
        competing_products=("competition", "max"),
        source_file_count=("source", "nunique"),
        source_files=("source", lambda paths: " | ".join(sorted(set(paths)))),
        best_rank=("rank", "min"),
    ).reset_index()
    ranked = result.sort_values(["source_file_count", "search_volume"], ascending=False)
    print(ranked.head(args.top).to_string(index=False))


if __name__ == "__main__":
    main()
