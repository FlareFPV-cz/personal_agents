from langchain.tools import DuckDuckGoSearchRun
import time
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from base_agent import BaseAgent
from utils.logger import AgentLogger

class DuckDuckResearcher(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_tool = DuckDuckGoSearchRun()
        self.logger = AgentLogger("DuckDuckResearcher", log_file="logs/researcher.log")
        
    def _initialize_research_chain(self):
        self._initialize_chain(
            input_variables=["topic", "search_results"],
            prompt_template="Summarize the latest research on {topic} based on:\n{search_results}\nFocus on key trends, major players, and recent breakthroughs."
        )
    
    def _initialize_analysis_chain(self):
        self._initialize_chain(
            input_variables=["research_data"],
            prompt_template="Analyze the following research data for credibility, biases, and key insights:\n\n{research_data}\n\nProvide a critical summary."
        )
    
    def _initialize_writing_chain(self):
        self._initialize_chain(
            input_variables=["topic", "analysis_data"],
            prompt_template="Write a detailed report on {topic} based on the following analysis:\n{analysis_data}\n\nInclude an executive summary, key findings, and conclusions."
        )
    
    def research(self, topic):
        """Conducts research using DuckDuckGo."""
        self.logger.info(f"Starting research on topic: {topic}")
        start_time = time.time()
        
        search_results = self.search_tool.run(topic)
        self.logger.debug(f"Retrieved search results for topic: {topic}")
        
        self._initialize_research_chain()
        result = self.chain.run({"topic": topic, "search_results": search_results})
        
        duration = time.time() - start_time
        self.logger.info(f"Research completed in {duration:.2f} seconds")
        return result
    
    def analyze(self, research_data):
        """Analyzes research data for credibility, patterns, and insights."""
        self.logger.info("Starting research data analysis")
        start_time = time.time()
        
        self._initialize_analysis_chain()
        result = self.chain.run({"research_data": research_data})
        
        duration = time.time() - start_time
        self.logger.info(f"Analysis completed in {duration:.2f} seconds")
        return result
    
    def write_report(self, topic, analysis_data):
        """Writes a well-structured report based on the analysis."""
        self.logger.info("Starting report writing")
        start_time = time.time()
        
        self._initialize_writing_chain()
        result = self.chain.run({"topic": topic, "analysis_data": analysis_data})
        
        duration = time.time() - start_time
        self.logger.info(f"Report writing completed in {duration:.2f} seconds")
        return result
    
    def run(self, topic):
        """Main execution flow"""
        try:
            self.logger.info(f"Starting research process for topic: {topic}")
            start_time = time.time()
            
            research_data = self.research(topic)
            analysis_data = self.analyze(research_data)
            final_report = self.write_report(topic, analysis_data)
            
            total_duration = time.time() - start_time
            self.logger.info(f"Total research process completed in {total_duration:.2f} seconds")
            
            result = {
                'topic': topic,
                'research_data': research_data,
                'analysis_data': analysis_data,
                'final_report': final_report
            }
            
            # Save report to file
            with open("final_report.txt", "w", encoding="utf-8") as f:
                f.write(final_report)
            
            print("\n✅ Report saved as 'final_report.txt'")
            return self._format_response(result)
            
        except Exception as e:
            return self._handle_error(e, "research process")

if __name__ == "__main__":
    researcher = DuckDuckResearcher()
    topic = input("Enter research topic: ")
    result = researcher.run(topic)
    
    if result['success']:
        print("\n=== FINAL REPORT ===")
        print(result['data']['final_report'])