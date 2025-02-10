# Example usage of DuckDuckResearcher
from agents.researcher import DuckDuckResearcher

def main():
    # Initialize the researcher
    researcher = DuckDuckResearcher()
    
    # Example: Research a topic
    print("\n🔍 Starting Research Process:")
    topic = "Artificial Intelligence in Healthcare"
    
    result = researcher.run(topic)
    
    if result['success']:
        data = result['data']
        print(f"""
        Research Results:
        Topic: {data['topic']}
        
        === Research Data ===
        {data['research_data']}
        
        === Analysis ===
        {data['analysis_data']}
        
        === Final Report ===
        {data['final_report']}
        
        ✅ Report has been saved to 'final_report.txt'
        """)
    else:
        print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    main()