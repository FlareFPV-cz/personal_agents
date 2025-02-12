# Example usage of MailAgent
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.mail_agent import MailAgent

def main():
    # Initialize the mail agent with a custom confidence threshold
    agent = MailAgent(confidence_threshold=0.7)
    
    # Example 1: Verify business email
    print("\n📧 Analyzing Business Email:")
    email = "contact@example.com"
    company = "Example Corp"
    website = "https://www.example.com"
    
    result = agent.run(email, company, website)
    
    if result.get('success'):
        data = result.get('data')
        print(f"""
Email Analysis Results:
Email: {data.get('email')}
Company: {data.get('company')}
Domain Match: {'✅ Yes' if data.get('domain_match') else '❌ No'}
Purpose Analysis: {'✅ Yes' if data.get('analysis', {}).get('purpose') == 'YES' else '❌ No'}
Historical Verification: {'✅ Yes' if data.get('analysis', {}).get('historical') == 'YES' else '❌ No'}
Newsletter Suitability: {'✅ Yes' if data.get('analysis', {}).get('suitability') == 'YES' else '❌ No'}
Confidence Score: {data.get('analysis', {}).get('confidence', 0.0):.2f}
Final Decision: {'✅ APPROVED' if data.get('approved') else '❌ REJECTED'}
""")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    # Example 2: Verify support email
    print("\n📧 Analyzing Support Email:")
    email = "support@techcompany.com"
    company = "Tech Company Inc."
    website = "https://www.techcompany.com"
    
    result = agent.run(email, company, website)
    
    if result.get('success'):
        data = result.get('data')
        print(f"""
Email Analysis Results:
Email: {data.get('email')}
Company: {data.get('company')}
Domain Match: {'✅ Yes' if data.get('domain_match') else '❌ No'}
Purpose Analysis: {'✅ Yes' if data.get('analysis', {}).get('purpose') == 'YES' else '❌ No'}
Historical Verification: {'✅ Yes' if data.get('analysis', {}).get('historical') == 'YES' else '❌ No'}
Newsletter Suitability: {'✅ Yes' if data.get('analysis', {}).get('suitability') == 'YES' else '❌ No'}
Confidence Score: {data.get('analysis', {}).get('confidence', 0.0):.2f}
Final Decision: {'✅ APPROVED' if data.get('approved') else '❌ REJECTED'}
""")
    else:
        print(f"❌ Error: {result.get('error')}")
    
if __name__ == "__main__":
    main()