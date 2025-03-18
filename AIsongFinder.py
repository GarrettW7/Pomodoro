import os
from googleapiclient.discovery import build
from groq import Groq
from dotenv import load_dotenv
import isodate


# Load environment variables from .env file
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
client = Groq(api_key=os.getenv('GROQ_API_KEY'))



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

# def get_song(genre):
#     """Ask Groq for a refined genre and fetch a fresh YouTube video."""
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {"role": "system", "content": "Refine the music genre for a better YouTube search."},
#             {"role": "user", "content": genre}
#         ],
#         model="mixtral-8x7b-32768",
#         temperature=0.7,
#         max_completion_tokens=50
#     )

#     suggested_genre = chat_completion.choices[0].message.content.strip()
    
#     return search_youtube(suggested_genre)
