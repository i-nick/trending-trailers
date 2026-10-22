#!/usr/bin/env python3
"""Validate the public catalogs without network access or third-party packages."""

import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
PLATFORMS = {"apple-tv", "netflix", "hulu", "disney-plus", "hbo-max", "prime-video"}
YOUTUBE = re.compile(r"https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}\Z")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
REQUIRED = {
    "id", "title", "year", "platform", "rank", "youtube_url", "youtube_channel",
    "availability_url", "trending_source_url", "verified_at",
}


def validate(filename, kind):
    data = json.loads((ROOT / filename).read_text(encoding="utf-8"))
    assert data["schema_version"] == 1, f"{filename}: unsupported schema_version"
    assert data["region"] == "US", f"{filename}: expected US region"
    assert data["kind"] == kind, f"{filename}: wrong kind"
    updated = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
    assert updated.utcoffset().total_seconds() == 0, f"{filename}: updated_at must be UTC"
    assert updated <= datetime.now(timezone.utc), f"{filename}: updated_at is in the future"
    entries = data["items"]
    assert isinstance(entries, list), f"{filename}: items must be an array"
    counts, ranks, ids, videos = Counter(), defaultdict(list), set(), set()
    for item in entries:
        label = f"{filename}: {item.get('id', '?')}"
        assert REQUIRED <= item.keys(), f"{label}: missing {REQUIRED - item.keys()}"
        assert SLUG.fullmatch(item["id"]), f"{label}: invalid stable slug"
        assert item["id"] not in ids, f"{label}: duplicate id"
        ids.add(item["id"])
        for field in ("title", "youtube_channel"):
            assert isinstance(item[field], str) and item[field].strip(), f"{label}: empty {field}"
        assert type(item["year"]) is int and 1888 <= item["year"] <= updated.year, f"{label}: invalid year"
        assert item["platform"] in PLATFORMS, f"{label}: unknown platform"
        assert type(item["rank"]) is int and 1 <= item["rank"] <= 5, f"{label}: invalid rank"
        assert YOUTUBE.fullmatch(item["youtube_url"]), f"{label}: invalid canonical YouTube watch URL"
        assert item["youtube_url"] not in videos, f"{label}: repeated trailer in one catalog"
        videos.add(item["youtube_url"])
        for field in ("availability_url", "trending_source_url"):
            url = urlparse(item[field])
            assert url.scheme == "https" and url.netloc, f"{label}: invalid {field}"
        verified = date.fromisoformat(item["verified_at"])
        assert verified <= updated.date(), f"{label}: verification is in the future"
        basis = item.get("selection_basis")
        assert basis in {"provider_chart", "editorial_recent_release", "editorial_availability"}, f"{label}: missing selection basis"
        source_date = date.fromisoformat(item["trending_source_date"])
        assert source_date <= verified, f"{label}: source is newer than verification"
        if basis == "provider_chart":
            assert type(item.get("source_rank")) is int and item["source_rank"] >= 1, f"{label}: missing published source rank"
        if "trailer_published_at" in item:
            assert date.fromisoformat(item["trailer_published_at"]) <= verified, f"{label}: future trailer"
        assert item.get("trailer_type", "trailer") == "trailer", f"{label}: expected a full trailer"
        counts[item["platform"]] += 1
        ranks[item["platform"]].append(item["rank"])
    assert set(counts) == PLATFORMS, f"{filename}: missing provider"
    for platform, count in counts.items():
        assert 2 <= count <= 5, f"{filename}: {platform} needs 2–5 entries"
        assert ranks[platform] == list(range(1, count + 1)), f"{filename}: {platform} ranks must be consecutive and ordered"
    print(f"{filename}: {len(entries)} entries; " + ", ".join(f"{p}={counts[p]}" for p in sorted(PLATFORMS)))


if __name__ == "__main__":
    validate("movies.json", "movie")
    validate("tv-shows.json", "tv")
    print("Catalog validation passed.")
