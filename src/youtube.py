import os
import json
from pathlib import Path

import requests


API_KEY = os.environ["YOUTUBE_API_KEY"]
CACHE_DIR = Path(os.environ["CACHE_DIR"]) if "CACHE_DIR" in os.environ else Path("cache")
THUMBNAIL_PRIORITY = ["maxres", "high", "medium", "standard", "default"]


def cached_fetch(url, id, cache_dir, headers=None, params=None, verbose=False):
    if isinstance(id, list):
        id = ",".join(id)
    assert isinstance(id, str), id

    cache_path = Path(cache_dir) / f"{id}.json"
    if cache_path.exists():
        if verbose:
            print(f"Loaded data from cache {cache_path}.")
        with open(cache_path) as fp:
            data = json.load(fp)
    else:
        res = requests.get(url, headers=headers, params=params)
        if verbose:
            print("Fetched", res.request.url)
            print("Status code:", res.status_code)
        data = res.json()
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w") as fp:
            json.dump(data, fp)
    return data


def get_playlist_info(playlist_id):
    url = "https://content-youtube.googleapis.com/youtube/v3/playlists"
    headers = {
        "Accept": "application/json",
    }
    params = {
        "part": "snippet",  # required
        "maxResults": 50,
        "id": playlist_id,
        "key": API_KEY,  # required
    }
    res = requests.get(url, headers=headers, params=params)
    print("Fetched", res.request.url)
    print("Status code:", res.status_code)
    data = res.json()
    return data


def get_playlist_videos(playlist_id):
    url = "https://content-youtube.googleapis.com/youtube/v3/playlistItems"
    headers = {
        "Accept": "application/json",
    }
    params = {
        "part": "content_details",  # required
        "maxResults": 50,
        "playlistId": playlist_id,
        "key": API_KEY,  # required
    }
    res = requests.get(url, headers=headers, params=params)
    print("Fetched", res.request.url)
    print("Status code:", res.status_code)
    data = res.json()
    return data


def get_video_details(video_ids):
    url = "https://content-youtube.googleapis.com/youtube/v3/videos"
    headers = {
        "Accept": "application/json",
    }
    params = {
        "part": "snippet,statistics",  # required
        "maxResults": 50,
        "id": video_ids,
        "key": API_KEY,  # required
    }
    res = requests.get(url, headers=headers, params=params)
    print("Fetched", res.request.url)
    print("Status code:", res.status_code)
    data = res.json()
    return data


def get_channel(channel_ids):
    url = "https://www.googleapis.com/youtube/v3/channels"
    headers = {
        "Accept": "application/json",
    }
    params = {
        "part": "snippet",  # required
        "maxResults": 50,
        "id": channel_ids,
        "key": API_KEY,  # required
    }
    data = cached_fetch(url, channel_ids, CACHE_DIR / "channel", headers=headers, params=params)
    return data


def get_best_thumbnail_url(thumbnails):
    for key in THUMBNAIL_PRIORITY:
        if key in thumbnails:
            return thumbnails[key]["url"], key
    return None, None
