import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.creative_writing_critique import CreativeWritingCritic

def main():
    # Initialize the critic with a custom quality threshold
    critic = CreativeWritingCritic(quality_threshold=0.7)
    
    # Example 1: Analyze a URL
    print("\n🔗 Analyzing Creative Writing from URL:")
    url = "https://blog.reedsy.com/short-story/vciu6c/"
    url_result = critic.run(url)
    
    if url_result['success']:
        data = url_result['data']
        print(f"""
        URL Analysis Results:
        Rating: {data['rating']:.2f}
        Genre: {data['genre']}
        Tone: {data['tone']}
        Approved: {'✅ Yes' if data['approved'] else '❌ No'}
        Suggestions:
        {chr(10).join(f' - {rec}' for rec in data['suggestions'])}\n""")
    else:
        print(f"❌ Error: {url_result['error']}")
    
    # Example 2: Analyze text content
    print("\n📝 Analyzing Creative Writing Text:")
    text_content = """
    The old lighthouse stood tall against the crashing waves, its beacon flickering
    in the storm. Beneath its guiding light, a lone figure trudged through the sand,
    clutching a letter that could change everything...
    """
    
    text_result = critic.run(text_content)
    
    if text_result['success']:
        data = text_result['data']
        print(f"""
        Text Analysis Results:
        Rating: {data['rating']:.2f}
        Genre: {data['genre']}
        Tone: {data['tone']}
        Approved: {'✅ Yes' if data['approved'] else '❌ No'}
        Suggestions:
        {chr(10).join(f' - {rec}' for rec in data['suggestions'])}\n""")
    else:
        print(f"❌ Error: {text_result['error']}")

if __name__ == "__main__":
    main()
