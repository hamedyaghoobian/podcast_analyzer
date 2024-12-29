from youtube_transcript_api import YouTubeTranscriptApi
from pytube import Playlist
import json
import re

class YouTubeTranscriptScraper:
    def __init__(self, playlist_url):
        self.playlist_url = playlist_url
        self.transcripts = {}
    
    def get_video_ids(self):
        """Extract video IDs from the playlist."""
        playlist = Playlist(self.playlist_url)
        # Use regex to extract video IDs from URLs
        video_ids = [re.search(r'v=([^&]+)', url).group(1) for url in playlist.video_urls]
        return video_ids
    
    def get_transcript(self, video_id):
        """Get transcript for a single video."""
        try:
            # First try to get English transcript
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            except:
                # If English not available, try to get any transcript and translate to English
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                transcript = transcript_list.find_generated_transcript(['de', 'es', 'fr', 'it'])
                if transcript:
                    transcript = transcript.translate('en').fetch()
                else:
                    # If no generated transcript found, try manual transcripts
                    try:
                        transcript = transcript_list.find_manually_created_transcript(['de', 'es', 'fr', 'it'])
                        transcript = transcript.translate('en').fetch()
                    except:
                        print(f"No suitable transcript found for video {video_id}")
                        return None
            return transcript
        except Exception as e:
            print(f"Could not get transcript for video {video_id}: {str(e)}")
            return None
    
    def scrape_all_transcripts(self):
        """Scrape transcripts for all videos in the playlist."""
        video_ids = self.get_video_ids()
        
        for video_id in video_ids:
            transcript = self.get_transcript(video_id)
            if transcript:
                self.transcripts[video_id] = transcript
        
        # Save transcripts to file
        self.save_transcripts()
    
    def save_transcripts(self):
        """Save transcripts to a JSON file."""
        with open('transcripts.json', 'w', encoding='utf-8') as f:
            json.dump(self.transcripts, f, ensure_ascii=False, indent=2)
        return 'transcripts.json'

if __name__ == "__main__":
    PLAYLIST_URL = "https://youtube.com/playlist?list=PL2k_Y6RURkfBkfQYotza0qMhmXAMRP6Cp"
    scraper = YouTubeTranscriptScraper(PLAYLIST_URL)
    output_file = scraper.save_transcripts()
    print(f"Transcripts saved to {output_file}") 