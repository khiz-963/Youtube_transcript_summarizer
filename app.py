import streamlit as st
from dotenv import load_dotenv
load_dotenv() ##load all the environment variables
import os
import google.generativeai as genai
import requests 
from PIL import Image 
from io import BytesIO 
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Youtube video summarizer, You will be taking the transcript text and summarizing the entire video and providing the important summary in points within 250 words. Please provide the summary of the text given here :"""

## getting the transcript data from youtube videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

    
        transcript = " ".join([i["text"] for i in transcript_text])

        return transcript

    except Exception as e:
       ##raise e
       st.error("Error extracting transcript.Please check the video URL")
       st.stop()

## displaying the youtube thumbnail
def get_thumbnail_image(video_id):
    try:
        response = requests.get(f"http://img.youtube.com/vi/{video_id}/0.jpg")
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.warning("Thumbnail image not available.")
        return None
    
## getting summary based on prompt from google gemini pro
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("YouTube Transcript Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    ##print(video_id)
    
    thumbnail = get_thumbnail_image(video_id)
    if thumbnail:
        st.image(thumbnail, caption="YouTube Video Thumbnail", use_column_width=True)
    

if st.button("Get Detailed Summary"):
    transcript_text=extract_transcript_details(youtube_link)
    
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Summary:")
        st.write(summary)

