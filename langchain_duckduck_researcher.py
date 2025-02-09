from langchain_groq import ChatGroq
from langchain.tools import DuckDuckGoSearchRun
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
import os

# Set Groq API key
os.environ["GROQ_API_KEY"] = ""  # Replace with your Groq API key

# Initialize LLM
groq_llm = ChatGroq(temperature=0.7, model_name="mixtral-8x7b-32768")

# Initialize search tool
search_tool = DuckDuckGoSearchRun()

# ========== Research Step ==========
def research(topic):
    """ Conducts research using DuckDuckGo. """
    print(f"🔍 Researching: {topic}")
    search_results = search_tool.run(topic)
    
    # Process results using LLM
    research_prompt = PromptTemplate(
        input_variables=["topic", "search_results"],
        template="Summarize the latest research on {topic} based on:\n{search_results}\nFocus on key trends, major players, and recent breakthroughs."
    )
    research_chain = LLMChain(llm=groq_llm, prompt=research_prompt)
    
    return research_chain.run({"topic": topic, "search_results": search_results})

# ========== Analysis Step ==========
def analyze(research_data):
    """ Analyzes research data for credibility, patterns, and insights. """
    print("📊 Analyzing research data...")
    
    analysis_prompt = PromptTemplate(
        input_variables=["research_data"],
        template="Analyze the following research data for credibility, biases, and key insights:\n\n{research_data}\n\nProvide a critical summary."
    )
    analysis_chain = LLMChain(llm=groq_llm, prompt=analysis_prompt)
    
    return analysis_chain.run({"research_data": research_data})

# ========== Writing Step ==========
def write_report(topic, analysis_data):
    """ Writes a well-structured report based on the analysis. """
    print("📝 Writing final report...")
    
    writing_prompt = PromptTemplate(
        input_variables=["topic", "analysis_data"],
        template="Write a detailed report on {topic} based on the following analysis:\n{analysis_data}\n\nInclude an executive summary, key findings, and conclusions."
    )
    writing_chain = LLMChain(llm=groq_llm, prompt=writing_prompt)
    
    return writing_chain.run({"topic": topic, "analysis_data": analysis_data})

# ========== Main Execution ==========
if __name__ == "__main__":
    topic = input("Enter research topic: ")
    
    research_data = research(topic)
    analysis_data = analyze(research_data)
    final_report = write_report(topic, analysis_data)
    
    print("\n\n=== FINAL REPORT ===")
    print(final_report)

    # Save report to file
    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write(final_report)
    
    print("\n✅ Report saved as 'final_report.txt'")
