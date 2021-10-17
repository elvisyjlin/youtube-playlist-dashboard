import re
import json
from datetime import datetime
from collections import defaultdict

import pandas as pd

from .youtube import (
    CACHE_DIR,
    get_playlist_info,
    get_playlist_videos,
    get_video_details,
    get_channel,
)


def normalize_title(title):
    m = re.match(r"(\[[\w ]+\] )?([^\|]+)( (\||dance cover).+)", title, re.IGNORECASE)
    if m is not None:
        return m.group(2)
    return title


def retrieve_data_from_playlist(playlist_id, save_as_files=True):
    playlist_videos_cache_dir = CACHE_DIR / "playlist_videos"
    video_details_cache_dir = CACHE_DIR / "video_details"
    playlist_videos_cache_dir.mkdir(parents=True, exist_ok=True)
    video_details_cache_dir.mkdir(parents=True, exist_ok=True)

    data = get_playlist_info(playlist_id)
    playlist_title = data["items"][0]["snippet"]["title"]

    data = get_playlist_videos(playlist_id)
    timestamp = int(datetime.utcnow().timestamp())
    if save_as_files:
        with open(playlist_videos_cache_dir / f"{playlist_id}_{timestamp}.json", "w") as fp:
            json.dump(data, fp)

    video_ids = [item["contentDetails"]["videoId"] for item in data["items"]]
    data = get_video_details(video_ids)
    timestamp = int(datetime.utcnow().timestamp())
    if save_as_files:
        with open(video_details_cache_dir / f"{playlist_id}_{timestamp}.json", "w") as fp:
            json.dump(data, fp)
    
    date_now = datetime.utcnow()

    result = defaultdict(list)
    stats = {}
    total_view_count = 0
    total_comment_count = 0
    total_like_count = 0
    total_dislike_count = 0
    for item in data["items"]:
        video_id = item["id"]
        title = normalize_title(item["snippet"]["title"])
        channel_id = item["snippet"]["channelId"]
        channel_data = get_channel(channel_id)
        channel_name = channel_data["items"][0]["snippet"]["title"]
        view_count = int(item["statistics"]["viewCount"])
        like_count = int(item["statistics"]["likeCount"])
        dislike_count = int(item["statistics"]["dislikeCount"])
        comment_count = int(item["statistics"]["commentCount"])
        thumbnail_url = item["snippet"]["thumbnails"]["default"]["url"]
        date_publish = datetime.strptime(item["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        days_since_publish = (date_now - date_publish).days + 1
        seconds_since_publish = (date_now - date_publish).total_seconds() + 1

        total_view_count += view_count
        total_comment_count += comment_count
        total_like_count += like_count
        total_dislike_count += dislike_count

        result["Id"].append(video_id)
        result["Title"].append(title)
        result["Channel"].append(channel_name)
        result["Publish Days"].append(days_since_publish)
        result["View Count"].append(view_count)
        result["Daily View Count"].append(view_count / days_since_publish)
        result["Estimated Daily View Count"].append(view_count / seconds_since_publish * 24 * 60 * 60)
        result["Comment Count"].append(comment_count)
        result["Like Count"].append(like_count)
        result["Dislike Count"].append(dislike_count)
        result["Like Rate"].append(
            like_count / (like_count + dislike_count) * 100
        )
        result["Thumbnail Url"].append(thumbnail_url)

    stats["playlist_title"] = playlist_title
    stats["total_view_count"] = total_view_count
    stats["total_comment_count"] = total_comment_count
    stats["total_like_count"] = total_like_count
    stats["total_dislike_count"] = total_dislike_count
    return pd.DataFrame(result), stats
