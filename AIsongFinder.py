import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import isodate

# Load environment variables from .env file
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)



def search_youtube(genre, min_duration=0):
    """Search for a music video on YouTube based on the given genre and minimum duration (in seconds)."""
    
    request = youtube.search().list(
        q=f"{genre} music",
        part="snippet",
        type="video",
        maxResults=10,  # Increase search depth for better filtering
        order="relevance"
    )

    response = request.execute()

    video_ids = [item["id"].get("videoId") for item in response["items"] if "videoId" in item["id"]]

    if not video_ids:
        return "No results found."

    # Get video details including duration
    details_request = youtube.videos().list(
        part="contentDetails",
        id=",".join(video_ids)  # Get details for all found videos
    )
    details_response = details_request.execute()

    for video in details_response["items"]:
        duration_str = video["contentDetails"]["duration"]
        duration_seconds = isodate.parse_duration(duration_str).total_seconds()  # Convert ISO 8601 to seconds

        if (duration_seconds/60) >= min_duration:
            return f"https://www.youtube.com/watch?v={video['id']}"

    return "No videos found with the required minimum length."
