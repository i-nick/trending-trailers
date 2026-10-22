# Trending trailers

Two public JSON catalogs of official YouTube trailers for movies and TV shows available in the United States on Apple TV, Netflix, Hulu, Disney+, HBO Max, and Prime Video.

- [Movies](movies.json): 16 entries, 2–3 per service.
- [TV shows](tv-shows.json): 17 entries, 2–3 per service.
- Verified October 22, 2026. These are manually reviewed snapshots; they do not refresh automatically.

## Public URLs

```text
https://raw.githubusercontent.com/i-nick/trending-trailers/main/movies.json
https://raw.githubusercontent.com/i-nick/trending-trailers/main/tv-shows.json
```

## Selection and sources

The catalogs contain selected charting titles, ordered for display within each service. `rank` is that consecutive display order. `source_rank` preserves a title's position in the cited provider chart; it can differ from `rank`. Chart positions are ordinal popularity signals, not audited viewing totals or estimates of viewing hours.

32 entries use the US provider charts below, dated October 21, 2026 and checked October 22. Availability was cross-checked against service/studio pages and US JustWatch or Rotten Tomatoes title pages. Apple TV means its subscription catalog; store rentals and purchases are excluded. Hulu selections use its streaming library, excluding titles requiring the HBO Max add-on.

| Service | Chart source |
| --- | --- |
| Apple TV | [StreamRank US](https://streamrank.io/apple/us) |
| Netflix | [StreamRank US](https://streamrank.io/netflix/us) |
| Hulu | [StreamRank US](https://streamrank.io/hulu/us) |
| Disney+ | [StreamRank US](https://streamrank.io/disney/us) |
| HBO Max | [StreamRank US](https://streamrank.io/max/us) |
| Prime Video | [StreamRank US](https://streamrank.io/prime/us) |

The live-action **Moana (2026)** is explicitly `editorial_recent_release`, with no `source_rank`: [Disney's US announcement, revised October 21](https://www.disneyplus.com/explore/articles/moana-live-action), confirms it is now streaming. It is not presented as a measured chart placement. The chart's other same-name Moana entry has inconsistent year metadata and is not used for this film.

Additional primary corroboration includes [Netflix's US weekly top 10](https://www.netflix.com/tudum/top10/united-states), [Netflix's October 20 report](https://www.netflix.com/tudum/articles/top-10-october-12-2026), and [Amazon's October 2026 lineup](https://www.aboutamazon.com/news/entertainment/prime-video-october-films-shows-sports-2026).

Every trailer links to a studio, network, or streaming service publisher. Some service pages redirect by location or require sign-in; title-specific US availability aggregators are retained where direct service pages could not be resolved. Provider catalogs, chart pages, video availability, and season coverage can change after verification.

## Schema version 1

Each file contains:

```json
{
  "schema_version": 1,
  "updated_at": "2026-10-22T07:40:48Z",
  "region": "US",
  "kind": "movie",
  "items": []
}
```

`kind` is `movie` or `tv`. Each item supplies `id`, `title`, `year`, `platform`, `rank`, `youtube_url`, `youtube_channel`, `availability_url`, `trending_source_url`, and `verified_at`.

- `id`: stable lowercase slug; preserve it when replacing a trailer or reordering a title.
- `year`: service release year for a movie, series debut year for a TV show. Sacrifice uses Netflix's 2026 display year, with its 2025 festival premiere noted separately.
- `platform`: `apple-tv`, `netflix`, `hulu`, `disney-plus`, `hbo-max`, or `prime-video`.
- `rank`: consecutive 1–5 within a provider and catalog.
- `youtube_url`: canonical `https://www.youtube.com/watch?v=<11-character-ID>`.
- `selection_basis`, `trending_source_date`, `source_rank`, `trailer_season`, `trailer_published_at`, and `notes`: supporting provenance where applicable.

Readers should ignore additional metadata fields they do not recognize.

## Validation and updates

```sh
python3 validate.py
```

The dependency-free validator checks both schemas, six-provider coverage, 2–5 entries per provider, stable unique IDs, consecutive ranks, canonical YouTube URLs, source metadata, and dates. It does not make network requests. At initial publication, separate live checks verified 1080p video, an audio stream, and successful media access for all 33 listed trailers; `playback_verified_at` and `playback_verified_height` record that check.

Before updating, recheck US subscription availability, the dated popularity evidence, the official publisher, and playback. Retain `source_rank` only for a documented chart placement. Label editorial selections explicitly and update verification dates only after checking the sources. Initial playback checks excluded a private Coven Academy upload, Grown Ups' 720p-only trailer, and animated Moana trailers whose 1080p streams could not be verified; the lists remain within the requested 2–5 entries per provider.

This repository stores metadata and links; the videos remain hosted by their publishers on YouTube.
