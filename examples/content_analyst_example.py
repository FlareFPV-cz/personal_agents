# Example usage of WebContentAnalyst
from agents.content_analyst import WebContentAnalyst

def main():
    # Initialize the analyst with custom quality threshold
    analyst = WebContentAnalyst(quality_threshold=0.65)
    
    # Example 1: Analyze a URL
    print("\n🔗 Analyzing URL:")
    url = "https://www.example.com/blog/sustainability"
    url_result = analyst.run(url)
    
    if url_result['success']:
        data = url_result['data']
        print(f"""
        URL Analysis Results:
        Score: {data['score']:.2f}
        Type: {data['type']}
        Sentiment: {data['sentiment']}
        Approved: {'✅ Yes' if data['approved'] else '❌ No'}
        Recommendations:
        {chr(10).join(f' - {rec}' for rec in data['recommendations'])}\n""")
    else:
        print(f"❌ Error: {url_result['error']}")
    
    # Example 2: Analyze text content
    print("\n📝 Analyzing Text:")
    text_content = """
    Introducing our revolutionary new solar panel technology! 
    With 40% higher efficiency than conventional panels, our 
    patented design makes renewable energy accessible for all.
    #CleanEnergy #Innovation
    """
    
    text_result = analyst.run(text_content)
    
    if text_result['success']:
        data = text_result['data']
        print(f"""
        Text Analysis Results:
        Score: {data['score']:.2f}
        Type: {data['type']}
        Sentiment: {data['sentiment']}
        Approved: {'✅ Yes' if data['approved'] else '❌ No'}
        Recommendations:
        {chr(10).join(f' - {rec}' for rec in data['recommendations'])}\n""")
    else:
        print(f"❌ Error: {text_result['error']}")

if __name__ == "__main__":
    main()