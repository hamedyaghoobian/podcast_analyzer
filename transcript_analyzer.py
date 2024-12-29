import json
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
from typing import Dict, List

class TranscriptAnalyzer:
    def __init__(self, transcripts_file='transcripts.json'):
        self.transcripts_file = transcripts_file
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            api_key=os.getenv('OPENAI_API_KEY')
        )
    
    def _load_transcripts(self) -> Dict:
        """Load transcripts from JSON file."""
        with open(self.transcripts_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _chunk_text(self, text: str, max_length: int = 4000) -> List[str]:
        """Split text into smaller chunks while preserving sentence boundaries."""
        # Split into sentences (roughly) by looking for period + space
        sentences = text.replace('. ', '.|').split('|')
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length > max_length:
                if current_chunk:  # Save current chunk if it exists
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
                    current_length = sentence_length
                else:  # Handle very long sentences by force-splitting
                    words = sentence.split()
                    while words:
                        chunk = []
                        chunk_length = 0
                        while words and chunk_length + len(words[0]) < max_length:
                            word = words.pop(0)
                            chunk.append(word)
                            chunk_length += len(word) + 1
                        chunks.append(' '.join(chunk))
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        if current_chunk:  # Don't forget the last chunk
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def analyze(self):
        """Analyze transcripts using CrewAI agents."""
        transcripts = self._load_transcripts()
        
        # Create agents
        summarizer = Agent(
            role='Content Summarizer',
            goal='Create focused summaries of podcast segments',
            backstory='Expert at extracting key information and main points from discussions',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        researcher = Agent(
            role='Research Analyst',
            goal='Identify and catalog academic content',
            backstory='Specialist in identifying academic references and research opportunities',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        synthesizer = Agent(
            role='Content Synthesizer',
            goal='Combine and organize findings into a coherent report',
            backstory='Expert at organizing and connecting information from multiple sources',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
        
        # Create tasks
        tasks = []
        episode_summaries = {}
        
        # First pass: Process each podcast episode in chunks
        for video_id, transcript in transcripts.items():
            episode_summaries[video_id] = []
            full_text = ' '.join([entry['text'] for entry in transcript])
            chunks = self._chunk_text(full_text)
            
            for i, chunk in enumerate(chunks):
                # Analyze chunk for main points
                summary_task = Task(
                    description=f"""
                    Analyze this segment (Part {i+1}) and identify:
                    1. Main topic or theme
                    2. Key points discussed
                    3. Important insights
                    4. Any academic references
                    
                    Text:
                    {chunk}
                    """,
                    agent=summarizer,
                    expected_output="A focused summary of the main points and academic references in this segment."
                )
                tasks.append(summary_task)
                episode_summaries[video_id].append(f"Part {i+1}")
        
        # Second pass: Synthesize episode summaries
        for video_id, parts in episode_summaries.items():
            synthesis_task = Task(
                description=f"""
                Create a coherent summary of the entire episode by combining the analyses of parts {', '.join(parts)}.
                Include:
                1. Overall theme and focus
                2. Main arguments and insights
                3. Academic content and references
                4. Key takeaways
                """,
                agent=synthesizer,
                expected_output="A comprehensive summary of the entire episode."
            )
            tasks.append(synthesis_task)
        
        # Final synthesis task
        final_task = Task(
            description="""
            Create a final report with:
            
            1. Episode Summaries
               - Main themes and topics
               - Key insights and arguments
               - Important examples and cases
            
            2. Academic Content
               - Papers and citations
               - Research opportunities
               - Books and resources
               - Theoretical frameworks
            
            3. Key Findings
               - Major themes across episodes
               - Important debates and perspectives
               - Emerging research directions
            
            Keep the focus on the most significant and well-supported points.
            """,
            agent=synthesizer,
            expected_output="A clear, organized report of the key findings and academic content."
        )
        tasks.append(final_task)
        
        # Create and run the crew
        crew = Crew(
            agents=[summarizer, researcher, synthesizer],
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )
        
        result = crew.kickoff()
        
        # Save results to file
        with open('analysis_results.txt', 'w', encoding='utf-8') as f:
            f.write(str(result))
        
        return str(result)

if __name__ == "__main__":
    analyzer = TranscriptAnalyzer()
    results = analyzer.analyze()
    print("\nAnalysis complete! Results saved to analysis_results.txt") 