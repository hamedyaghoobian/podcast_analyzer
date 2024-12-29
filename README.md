# YouTube Transcript Analyzer

This project scrapes transcripts from YouTube videos in a playlist and analyzes them using CrewAI to identify paper recommendations, book recommendations, calls for papers, and article recommendations.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Scrape transcripts from all videos in the specified YouTube playlist
2. Save the transcripts to `transcripts.json`
3. Analyze the transcripts using CrewAI to identify:
   - Paper recommendations
   - Book recommendations
   - Calls for papers
   - Article recommendations
4. Save the analysis results to `analysis_results.txt`

## Output

The analysis results will be saved in two files:
- `transcripts.json`: Raw transcripts from the YouTube videos
- `analysis_results.txt`: Organized findings including paper recommendations, book recommendations, calls for papers, and article recommendations

Each recommendation includes:
- Title/Name
- Context of the recommendation
- Source video link 