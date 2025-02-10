# Example usage of MailAgent
from agents.mail_agent import MailAgent

def main():
    # Initialize the mail agent with custom confidence threshold
    agent = MailAgent(confidence_threshold=0.7)
    
    # Example 1: Verify business email
    print("\n📧 Analyzing Business Email:")
    email = "contact@example.com"
    company = "Example Corp"
    website = "https://www.example.com"
    
    result = agent.run(email, company, website)
    
    if result['success']:
        data = result['data']
        print(f"""
        Email Analysis Results:
        Email: {data['email']}
        Company: {data['company']}
        Domain Match: {'✅ Yes' if data['domain_match'] else '❌ No'}
        Purpose Analysis: {'✅ Yes' if data['analysis']['purpose'] == 'YES' else '❌ No'}
        Historical Verification: {'✅ Yes' if data['analysis']['historical'] == 'YES' else '❌ No'}
        Newsletter Suitability: {'✅ Yes' if data['analysis']['suitability'] == 'YES' else '❌ No'}
        Confidence Score: {data['analysis']['confidence']:.2f}
        Final Decision: {'✅ APPROVED' if data['approved'] else '❌ REJECTED'}\n""")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Example 2: Verify support email
    print("\n📧 Analyzing Support Email:")
    email = "support@techcompany.com"
    company = "Tech Company Inc."
    website = "https://www.techcompany.com"
    
    result = agent.run(email, company, website)
    
    if result['success']:
        data = result['data']
        print(f"""
        Email Analysis Results:
        Email: {data['email']}
        Company: {data['company']}
        Domain Match: {'✅ Yes' if data['domain_match'] else '❌ No'}
        Purpose Analysis: {'✅ Yes' if data['analysis']['purpose'] == 'YES' else '❌ No'}
        Historical Verification: {'✅ Yes' if data['analysis']['historical'] == 'YES' else '❌ No'}
        Newsletter Suitability: {'✅ Yes' if data['analysis']['suitability'] == 'YES' else '❌ No'}
        Confidence Score: {data['analysis']['confidence']:.2f}
        Final Decision: {'✅ APPROVED' if data['approved'] else '❌ REJECTED'}\n""")
    else:
        print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    main()