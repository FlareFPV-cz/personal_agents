from langchain_community.tools import DuckDuckGoSearchRun
import time
from langchain.prompts import ChatPromptTemplate
from core.base_agent import BaseAgent
from utils.logger import AgentLogger
import os

class DuckDuckResearcher(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_tool = DuckDuckGoSearchRun()
        self.logger = AgentLogger("DuckDuckResearcher", log_file="logs/researcher.log")
        
    def _initialize_research_chain(self):
        self._initialize_chain(
            prompt_template="system Summarize the latest research on {topic} based on:\n{search_results}\nFocus on key trends, major players, and recent breakthroughs."
        )
    
    def _initialize_analysis_chain(self):
        self._initialize_chain(
            prompt_template="system Analyze the following research data for credibility, biases, and key insights:\n\n{research_data}\n\nProvide a critical summary."
        )
    
    def _initialize_writing_chain(self):
        self._initialize_chain(
            prompt_template="system Write a detailed report on {topic} based on the following analysis:\n{analysis_data}\n\nInclude an executive summary, key findings, and conclusions."
        )
    
    def research(self, topic):
        """Conducts research using DuckDuckGo with retries for rate limits."""
        self.logger.info(f"Starting research on topic: {topic}")
        start_time = time.time()
        
        max_retries = 3
        retry_delay = 5  # Base delay in seconds
        search_results = None
        
        for attempt in range(max_retries):
            try:
                search_results = self.search_tool.run(topic)
                if not search_results:
                    raise RuntimeError("No search results retrieved")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    sleep_time = retry_delay * (attempt + 1)
                    self.logger.warning(f"Search failed (attempt {attempt+1}): {str(e)}. Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                else:
                    self.logger.error(f"Failed after {max_retries} attempts: {str(e)}")
                    return "No valid search results retrieved."
        
        self.logger.debug(f"Retrieved search results for topic: {topic}")
        
        self._initialize_research_chain()
        result = self.chain.invoke({"topic": topic, "search_results": search_results}).content
        
        duration = time.time() - start_time
        self.logger.info(f"Research completed in {duration:.2f} seconds")
        return result
    
    def analyze(self, research_data):
        """Analyzes research data for credibility, patterns, and insights."""
        self.logger.info("Starting research data analysis")
        start_time = time.time()
        
        self._initialize_analysis_chain()
        result = self.chain.invoke({"research_data": research_data}).content
        
        duration = time.time() - start_time
        self.logger.info(f"Analysis completed in {duration:.2f} seconds")
        return result
    
    def write_report(self, topic, analysis_data):
        """Writes a well-structured report based on the analysis."""
        self.logger.info("Starting report writing")
        start_time = time.time()
        
        self._initialize_writing_chain()
        result = self.chain.invoke({"topic": topic, "analysis_data": analysis_data}).content
        
        duration = time.time() - start_time
        self.logger.info(f"Report writing completed in {duration:.2f} seconds")
        return result
    
    def run(self, topic):
        """Main execution flow"""
        try:
            self.logger.info(f"Starting research process for topic: {topic}")
            start_time = time.time()
            
            research_data = self.research(topic)
            if research_data == "No valid search results retrieved.":
                return {"success": False, "error": "Search failed. No valid results."}
            
            analysis_data = self.analyze(research_data)
            final_report = self.write_report(topic, analysis_data)
            
            total_duration = time.time() - start_time
            self.logger.info(f"Total research process completed in {total_duration:.2f} seconds")
            
            result = {
                'success': True,
                'topic': topic,
                'research_data': research_data,
                'analysis_data': analysis_data,
                'final_report': final_report
            }
            
            # Save report to file
            with open("final_report.txt", "w", encoding="utf-8") as f:
                f.write(final_report)
            
            print("\n✅ Report saved as 'final_report.txt'")
            return result
            
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return {"success": False, "error": str(e)}

# if __name__ == "__main__":
#     researcher = DuckDuckResearcher()
#     topic = input("Enter research topic: ")
#     result = researcher.run(topic)
    
#     if result['success']:
#         print("\n=== FINAL REPORT ===")
#         print(result['final_report'])
