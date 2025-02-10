import os
import re
import time
import requests
from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from base_agent import BaseAgent
from utils.logger import AgentLogger

class WebContentAnalyst(BaseAgent):
    def __init__(self, quality_threshold=0.7, **kwargs):
        super().__init__(**kwargs)
        self.quality_threshold = quality_threshold
        self.logger = AgentLogger("WebContentAnalyst", log_file="logs/content_analyst.log")
        self._initialize_chain(
            input_variables=["content", "source", "content_type"],
            prompt_template="""
            Analyze this web content from {source} ({content_type}):
            ---
            {content}
            ---
            
            Perform comprehensive analysis:
            
            1. Content Quality (0-1):
            - Readability (0.2)
            - Engagement (0.3)
            - SEO (0.25)
            - Mobile-friendliness (0.25)
            
            2. Content Type Identification:
            [Blog/News/Product/Technical/Forum/Other]
            
            3. Sentiment Analysis:
            [Positive/Neutral/Negative]
            
            4. Key Recommendations (3 bullet points)
            
            Response Format STRICTLY:
            ---
            Score: X.XX
            Type: [Type]
            Sentiment: [Sentiment]
            Recommendations:
            - Rec 1
            - Rec 2
            - Rec 3
            ---
            """
        )
    
    def _fetch_url_content(self, url):
        """Fetch and clean web content with error handling"""
        self.logger.info(f"Fetching content from URL: {url}")
        start_time = time.time()
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.5'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unnecessary elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'form']):
                element.decompose()
            
            # Extract main content
            main_content = soup.find('article') or soup.find('main') or soup.body
            content = ' '.join(main_content.get_text(separator=' ', strip=True).split()[:2000])
            
            duration = time.time() - start_time
            self.logger.info(f"Content fetched successfully in {duration:.2f} seconds")
            return content
            
        except Exception as e:
            self.logger.error(f"Error fetching URL content: {str(e)}")
            return self._handle_error(e, "fetching URL content")['data']

    def run(self, url):
        """Main execution flow for content analysis"""
        self.logger.info(f"Starting content analysis for URL: {url}")
        start_time = time.time()
        
        try:
            content = self._fetch_url_content(url)
            self.logger.debug("Content fetched, starting analysis")
            
            response = self.chain.run({
                "content": content,
                "source": url,
                "content_type": "webpage"
            })
            self.logger.debug("LLM analysis completed")
            
            analysis = self._parse_analysis(response)
            duration = time.time() - start_time
            self.logger.info(f"Analysis completed in {duration:.2f} seconds")
            
            return self._format_response(analysis)
            
        except Exception as e:
            self.logger.error(f"Error during content analysis: {str(e)}")
            return self._handle_error(e, "content analysis")

    def _parse_analysis(self, text):
        """Parse LLM response with robust error handling"""
        result = {
            'score': 0.0,
            'type': 'Unknown',
            'sentiment': 'Neutral',
            'recommendations': [],
            'approved': False
        }
        
        try:
            # Score extraction
            score_match = re.search(r"Score:\s*([0-9.]+)", text)
            if score_match:
                result['score'] = min(float(score_match.group(1)), 1.0)
            
            # Type extraction
            type_match = re.search(r"Type:\s*([A-Za-z]+)", text)
            if type_match:
                result['type'] = type_match.group(1).capitalize()
            
            # Sentiment extraction
            sentiment_match = re.search(r"Sentiment:\s*([A-Za-z]+)", text, re.IGNORECASE)
            if sentiment_match:
                result['sentiment'] = sentiment_match.group(1).capitalize()
            
            # Recommendations extraction
            recs = re.findall(r"- (.*?)\n", text)
            if recs:
                result['recommendations'] = [rec.strip() for rec in recs[:3]]
            
            result['approved'] = result['score'] >= self.quality_threshold
            return result
            
        except Exception as e:
            return self._handle_error(e, "parsing analysis")['data'] or result

    def run(self, input_source):
        """Main analysis method handling both URLs and text"""
        analysis_result = {
            'source': input_source if input_source.startswith('http') else 'Text Input',
            'content': '',
            'score': 0.0,
            'type': 'Unknown',
            'sentiment': 'Neutral',
            'recommendations': [],
            'approved': False
        }
        
        try:
            # URL handling
            if input_source.startswith(('http://', 'https://')):
                print(f"🌐 Fetching content from: {input_source}")
                content = self._fetch_url_content(input_source)
                if not content:
                    return self._format_response(analysis_result)
                content_type = 'webpage'
                
            # Text handling
            else:
                content = ' '.join(input_source.split()[:2000])  # Limit to 2000 words
                content_type = 'text'
            
            # Run analysis
            llm_response = self.chain.run({
                'content': content,
                'source': input_source,
                'content_type': content_type
            })
            
            # Parse and merge results
            parsed = self._parse_analysis(llm_response)
            analysis_result.update(parsed)
            analysis_result['content'] = content[:500] + '...'  # Store preview
            
            return self._format_response(analysis_result)
            
        except Exception as e:
            return self._handle_error(e, "analysis")

# if __name__ == "__main__":
#     # Example usage
#     analyst = WebContentAnalyst(quality_threshold=0.65)
    
#     # Analyze URL
#     print("\n🔗 Analyzing URL:")
#     url_result = analyst.analyze("https://example.com/blog/sustainability")
#     print(f"""
#     URL Analysis Results:
#     Score: {url_result['score']:.2f}
#     Type: {url_result['type']}
#     Sentiment: {url_result['sentiment']}
#     Approved: {'✅ Yes' if url_result['approved'] else '❌ No'}
#     Recommendations:
#     {chr(10).join(f' - {rec}' for rec in url_result['recommendations'])}
#     """)
#     # Analyze text
#     print("\n📝 Analyzing Text:")
#     text_content = """
#     Introducing our revolutionary new solar panel technology! 
#     With 40% higher efficiency than conventional panels, our 
#     patented design makes renewable energy accessible for all.
#     #CleanEnergy #Innovation
#     """
#     text_result = analyst.analyze(text_content)
#     print(f"""
#     Text Analysis Results:
#     Score: {text_result['score']:.2f}
#     Type: {text_result['type']}
#     Sentiment: {text_result['sentiment']}
#     Approved: {'✅ Yes' if text_result['approved'] else '❌ No'}
#     Recommendations:
#     {chr(10).join(f' - {rec}' for rec in text_result['recommendations'])}
#     """)