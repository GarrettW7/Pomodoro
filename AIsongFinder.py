import os
from googleapiclient.discovery import build
from groq import Groq
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
client = Groq(api_key=os.getenv('GROQ_API_KEY'))



def search_youtube(genre):
    """Search for a music video on YouTube based on the given genre."""
    request = youtube.search().list(
        q=f"{genre} music",
        part="snippet",
        type="video",
        maxResults=5,  # Increase search depth
        order="relevance"
    )
    response = request.execute()

    for item in response["items"]:
        video_id = item["id"].get("videoId")
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

    return "No results found."

def get_song(genre):
    """Ask Groq for a refined genre and fetch a fresh YouTube video."""
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Refine the music genre for a better YouTube search."},
            {"role": "user", "content": genre}
        ],
        model="mixtral-8x7b-32768",
        temperature=0.7,
        max_completion_tokens=50
    )

    suggested_genre = chat_completion.choices[0].message.content.strip()
    
    return search_youtube(suggested_genre)

# def getSong(message):

#     chat_completion = client.chat.completions.create(
#         #
#         # Required parameters
#         #
#         messages=[
#             # Set an optional system message. This sets the behavior of the
#             # assistant and can be used to provide specific instructions for
#             # how it should behave throughout the conversation.
#             {
#                 "role": "system",
#                 # "content": "You give the most correct answer possible. Reguardless of the question, you will always give the most correct answer."
#                 # "content" : "You will make fun of anything that i say and then make a haiku to finish your thoughts."
#                 "content": """
#                 You are an AI that finds music for me. I only want music from current YouTube videos. 

#                 You will only respond with a **valid** and **non-meme** URL to a YouTube video that plays music. 

#                 ❌ Do NOT return links to Rick Astley, meme music, or joke videos.  
#                 ✅ Only return links to **real** music videos from diverse genres.
#                 """
#             },
#             # Set a user message for the assistant to respond to.
#             {
#                 "role": "user",
#                 "content": f"{message}"
#             }
#         ],

#         # The language model which will generate the completion.
#         model="gemma2-9b-it",

#         #
#         # Optional parameters
#         #

#         # Controls randomness: lowering results in less random completions.
#         # As the temperature approaches zero, the model will become deterministic
#         # and repetitive.
#         temperature=.9,

#         # The maximum number of tokens to generate. Requests can use up to
#         # 32,768 tokens shared between prompt and completion.
#         max_completion_tokens=1024,

#         # Controls diversity via nucleus sampling: 0.5 means half of all
#         # likelihood-weighted options are considered.
#         top_p=1,

#         # A stop sequence is a predefined or user-specified text string that
#         # signals an AI to stop generating content, ensuring its responses
#         # remain focused and concise. Examples include punctuation marks and
#         # markers like "[end]".
#         stop=None,

#         # If set, partial message deltas will be sent.
#         stream=False,
#     )

    # Print the completion returned by the LLM.
    return(chat_completion.choices[0].message.content)