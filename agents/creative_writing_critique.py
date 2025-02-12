import os
import re
import time
import requests
from bs4 import BeautifulSoup
from langchain.prompts import ChatPromptTemplate
from core.base_agent import BaseAgent
from utils.logger import AgentLogger

class CreativeWritingCritic(BaseAgent):
    def __init__(self, quality_threshold=0.7, **kwargs):
        super().__init__(**kwargs)
        self.quality_threshold = quality_threshold
        self.logger = AgentLogger("CreativeWritingCritic", log_file="logs/creative_critic.log")
        self._initialize_chain(
            prompt_template="""system
Analyze this creative writing piece from {source} ({content_type}):
---
{content}
---

Perform a comprehensive critique focusing on:

1. Narrative Quality (0-1):
   - Narrative Structure (0.25)
   - Character Development (0.25)
   - Language & Style (0.25)
   - Emotional Impact (0.25)

2. Genre Identification:
   [Fantasy / Science Fiction / Romance / Mystery / Non-Fiction / Poetry / Other]

3. Tone Analysis:
   [Melancholic / Uplifting / Dark / Humorous / Neutral]

4. Key Suggestions for Improvement (3 bullet points)

Response Format STRICTLY:
---
Rating: X.XX
Genre: [Genre]
Tone: [Tone]
Suggestions:
- Suggestion 1
- Suggestion 2
- Suggestion 3
---
"""
        )
    
    def _fetch_url_content(self, url):
        """
        Fetches and cleans creative writing content from a URL.
        It removes extraneous elements and extracts a clean text snippet.
        """
        self.logger.info(f"Fetching creative writing content from URL: {url}")
        start_time = time.time()
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.5'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove elements that are not relevant to creative writing (e.g., navigation, ads)
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'form']):
                element.decompose()
            
            # Attempt to extract the creative content from <article>, <main>, or fallback to the body
            main_content = soup.find('article') or soup.find('main') or soup.body
            content = ' '.join(main_content.get_text(separator=' ', strip=True).split()[:2000])
            
            duration = time.time() - start_time
            self.logger.info(f"Content fetched successfully in {duration:.2f} seconds")
            return content
            
        except Exception as e:
            self.logger.error(f"Error fetching URL content: {str(e)}")
            return self._handle_error(e, "fetching creative writing content")['data']
    
    def _parse_analysis(self, text):
        """
        Parses the LLM's response for the creative writing critique.
        Expected output is a strictly formatted text block containing:
          - A rating (0-1)
          - Genre classification
          - Tone analysis
          - Three suggestions for improvement
        """
        # In case the text is wrapped in a dict, extract the string.
        if isinstance(text, dict):
            text = text.get("text", str(text))
            
        result = {
            'rating': 0.0,
            'genre': 'Unknown',
            'tone': 'Neutral',
            'suggestions': [],
            'approved': False
        }
        
        try:
            # Extract rating
            rating_match = re.search(r"Rating:\s*([0-9.]+)", text)
            if rating_match:
                result['rating'] = min(float(rating_match.group(1)), 1.0)
            
            # Extract genre
            genre_match = re.search(r"Genre:\s*\[?([A-Za-z\s]+)\]?", text)
            if genre_match:
                result['genre'] = genre_match.group(1).strip().title()
            
            # Extract tone
            tone_match = re.search(r"Tone:\s*\[?([A-Za-z\s]+)\]?", text)
            if tone_match:
                result['tone'] = tone_match.group(1).strip().title()
            
            # Extract suggestions (limit to the first 3 bullet points)
            suggestions = re.findall(r"- (.*?)\n", text)
            if suggestions:
                result['suggestions'] = [s.strip() for s in suggestions[:3]]
            
            # Determine if the writing meets the quality threshold
            result['approved'] = result['rating'] >= self.quality_threshold
            return result
            
        except Exception as e:
            return self._handle_error(e, "parsing creative writing critique")['data'] or result
    
    def run(self, input_source):
        """
        Main method for analyzing creative writing pieces.
        Accepts either a URL or direct text input.
        """
        analysis_result = {
            'source': input_source if input_source.startswith('http') else 'Text Input',
            'content': '',
            'rating': 0.0,
            'genre': 'Unknown',
            'tone': 'Neutral',
            'suggestions': [],
            'approved': False
        }
        
        try:
            # URL handling: fetch content from the provided URL
            if input_source.startswith(('http://', 'https://')):
                print(f"🌟 Fetching creative writing content from: {input_source}")
                content = self._fetch_url_content(input_source)
                if not content:
                    return self._format_response(analysis_result)
                content_type = 'webpage'
            
            # Text handling: process provided creative writing text directly
            else:
                content = ' '.join(input_source.split()[:2000])  # Limit to 2000 words
                content_type = 'text'
            
            # Invoke the language model to run the creative critique
            llm_response = self.chain.invoke({
                'content': content,
                'source': input_source,
                'content_type': content_type
            })
            
            parsed = self._parse_analysis(llm_response.content)
            
            analysis_result.update(parsed)
            analysis_result['content'] = content[:500] + '...'  # Save a preview of the text
            
            return self._format_response(analysis_result)
            
        except Exception as e:
            return self._handle_error(e, "creative writing critique analysis")
