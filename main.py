from youtube_scraper import YouTubeTranscriptScraper
from transcript_analyzer import TranscriptAnalyzer
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    # YouTube playlist URL
    playlist_url = "https://www.youtube.com/playlist?list=PL2k_Y6RURkfBkfQYotza0qMhmXAMRP6Cp"
    
    try:
        # Initialize the scraper
        scraper = YouTubeTranscriptScraper(playlist_url)
        print("Scraping transcripts from the playlist...")
        
        # Scrape and save transcripts
        scraper.scrape_all_transcripts()
        print("Transcripts saved successfully!")
        
        # Initialize the analyzer
        analyzer = TranscriptAnalyzer()
        print("\nAnalyzing transcripts...")
        
        # Analyze transcripts
        analyzer.analyze()
        print("Analysis completed! Results saved to analysis_results.txt")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 