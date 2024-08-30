import scrapetube
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders import YoutubeAudioLoader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser
import os
from dotenv import load_dotenv
from youtubevideo import YoutubeVideo

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment variables
my_key_openai = os.getenv("OPENAI_API_KEY")

# 1. Transcription
def get_video_transcript(url):
    target_dir = "./audios/"

    # Create directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Initialize the loader with YouTube audio and OpenAI Whisper parser
    loader = GenericLoader(
        YoutubeAudioLoader(urls=[url], save_dir=target_dir),
        OpenAIWhisperParser(api_key=my_key_openai)
    )

    # Load and return the video transcript documents
    video_transcript_docs = loader.load()

    return video_transcript_docs

# 2. YouTube Search
def get_videos_for_search_term(search_term, video_count=1, sorting_criteria="Most Relevant"):
    # Map user-friendly sorting criteria to actual API values
    convert_sorting_option = {
        "Most Relevant": "relevance",
        "By Date": "upload_date",
        "By Views": "view_count",
        "By Likes": "rating"
    }

    # Ensure the provided sorting criteria is valid
    if sorting_criteria not in convert_sorting_option:
        raise ValueError(
            f"Invalid sorting criteria: {sorting_criteria}. Choose from: {list(convert_sorting_option.keys())}")

    # Call the scrapetube search function with the correct sorting option
    videos = scrapetube.get_search(query=search_term, limit=video_count,
                                   sort_by=convert_sorting_option[sorting_criteria])
    videolist = list(videos)

    youtube_videos = []

    # Parse the video details and store them in the YoutubeVideo class
    for video in videolist:
        new_video = YoutubeVideo(
            video_id=video["videoId"],
            video_title=video["title"]["runs"][0]["text"],
            video_url="https://www.youtube.com/watch?v=" + video["videoId"],
            channel_name=video["longBylineText"]["runs"][0]["text"],
            duration=video["lengthText"]["accessibility"]["accessibilityData"]["label"],
            publish_date=video["publishedTimeText"]["simpleText"]
        )

        youtube_videos.append(new_video)

    return youtube_videos
