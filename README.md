🎥 VidChat: Chat with YouTube! 🚀

Overview

VidChat is your gateway to an interactive YouTube experience! 🌟 This sleek and powerful Streamlit app allows you to dive deep into any YouTube video, ask questions, and get insightful answers — all powered by cutting-edge AI technologies like LangChain and OpenAI's GPT-4. Whether you want to understand a tutorial better or just explore the content of a video in more depth, VidChat has got you covered! 💬

✨ Key Features

🔍 Video Search: Look up videos on YouTube based on your search terms and sorting preferences.
📄 Transcript-Based Q&A: Ask questions about a video, and VidChat will use the transcript to provide precise answers.
⚙️ Intelligent Retrieval: VidChat utilizes advanced retrieval mechanisms to find the most relevant parts of a video’s transcript to answer your queries.
🚀 Technologies Used

1. Streamlit 🖥️
Streamlit allows us to create a beautiful and responsive UI with minimal code. It powers the entire VidChat interface, making it both user-friendly and interactive.

2. LangChain 🔗
LangChain enables the integration of powerful language models into applications. In VidChat, it's the engine behind splitting video transcripts, creating embeddings, and retrieving relevant data.

3. OpenAI GPT-4 🤖
The heart of VidChat's intelligence! GPT-4 generates human-like responses based on the video transcript, providing you with accurate answers to your questions.

4. FAISS 🧠
FAISS is used to efficiently search through the video transcript vectors, ensuring that VidChat retrieves the most relevant information for your query.

5. scrapetube 🎥
scrapetube lets us seamlessly search for videos on YouTube, helping you find the content you want to interact with.

6. OpenAI Whisper 🗣️
Whisper is used to transcribe the audio from YouTube videos, converting spoken words into text that VidChat can process and understand.

📂 Code Structure

1. videohelper.py 🎞️
Handles video-related tasks, including:
get_video_transcript(url): Transcribes the video at the provided URL and returns it as a document.
get_videos_for_search_term(search_term, video_count, sorting_criteria): Searches YouTube and returns a list of videos based on your search criteria.

3. raghelperr.py 🧩
Manages the core RAG (Retrieval-Augmented Generation) process:
ask_openai(prompt): Sends a prompt to GPT-4 and returns the response.
rag_with_video_transcript(transcript_docs, prompt): Splits the transcript, retrieves relevant chunks, and generates an answer using GPT-4.

3. appp.py 🛠️
The main application file that:
Builds the Streamlit Interface: Manages user interactions, including video search and Q&A.
Handles Session Management: Ensures a smooth experience by caching video URLs and transcripts.

5. youtubevideo.py 🎬
Defines the YoutubeVideo class to encapsulate video details such as:
video_id, video_title, video_url, channel_name, duration, publish_date.

Usage
🔗 URL Mode: Paste a YouTube video URL, enter your question, and click "Ask". The app will transcribe the video and provide an answer based on the transcript.
🔍 Search Mode: Enter search terms to find YouTube videos, select a video, and ask your question. The app will handle the rest!

