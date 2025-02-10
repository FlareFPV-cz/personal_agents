import os
import re
from urllib.parse import urlparse
import tldextract
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("❌ GROQ_API_KEY is missing! Make sure it's in the .env file.")

groq_llm = ChatGroq(temperature=0.2, model_name="mixtral-8x7b-32768")

class MailAgent:
    def __init__(self, llm=groq_llm, confidence_threshold=0.7):
        self.llm = llm
        self.confidence_threshold = confidence_threshold
        self.prompt = PromptTemplate(
            input_variables=["email", "company", "official_url", "domain_match"],
            template=(
                "You are an expert in email verification and lead generation. "
                "Your task is to determine if the email {email} from {company} (official website: {official_url}) "
                "is suitable for receiving newsletters. Follow the structured evaluation below.\n\n"
                
                "### **Domain Match** (Pre-verified)\n"
                "The email domain {'✅ MATCHES' if domain_match else '❌ DOES NOT MATCH'} the company's official website domain.\n\n"
                
                "### **Purpose Analysis**\n"
                "Analyze whether the email is used for:\n"
                "- General inquiries\n"
                "- Customer support\n"
                "- Business communications\n"
                "Answer 'YES' if suitable, 'NO' if personal/unrelated.\n\n"
                
                "### **Historical Verification**\n"
                "Based on common patterns, does this email type typically appear on company websites?\n"
                "(Note: No live web access - using typical patterns)\n"
                "Answer 'YES' or 'NO'.\n\n"
                
                "### **Newsletter Suitability**\n"
                "Final recommendation considering:\n"
                "- Domain verification status\n"
                "- Email purpose\n"
                "- Typical business practices\n"
                "Answer 'YES' with reason if suitable, 'NO' with reasoning if not.\n\n"
                
                "### **Confidence Score**\n"
                "Numerical confidence (0.0-1.0) based on available information.\n\n"
                
                "**Strict Response Format:**\n"
                "Purpose Analysis: YES|NO\n"
                "Historical Verification: YES|NO\n"
                "Newsletter Suitability: YES|NO - [Brief Reason]\n"
                "Confidence Score: [0.0-1.0]"
            )
        )
        self.relevance_chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def _extract_domain(self, email, url):
        """Extract and compare domains using tldextract."""
        email_domain = email.split('@')[-1].lower()
        extracted = tldextract.extract(url)
        official_domain = f"{extracted.domain}.{extracted.suffix}".lower()
        return email_domain == official_domain or email_domain.endswith(f".{official_domain}")

    def _parse_response(self, text):
        """Robust response parsing with regex."""
        patterns = {
            "purpose": r"Purpose Analysis:\s*(YES|NO)",
            "historical": r"Historical Verification:\s*(YES|NO)",
            "suitability": r"Newsletter Suitability:\s*(YES|NO)",
            "confidence": r"Confidence Score:\s*([0-9.]+)"
        }
        results = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                results[key] = match.group(1).strip().upper()
            else:
                results[key] = "NO" if key != "confidence" else 0.0
        
        try:
            results["confidence"] = float(results.get("confidence", 0.0))
        except ValueError:
            results["confidence"] = 0.0
            
        return results

    def evaluate_relevance(self, email, company, official_url):
        """Enhanced evaluation with domain check and structured parsing."""
        print(f"🔍 Evaluating: {email}")
        
        try:
            # Programmatic domain verification
            domain_match = self._extract_domain(email, official_url)
            
            # Get LLM analysis
            response = self.relevance_chain.run({
                "email": email,
                "company": company,
                "official_url": official_url,
                "domain_match": domain_match
            })

            # Parse response
            parsed = self._parse_response(response)
            print(f"📊 Parsed Results: {parsed}")
            
            # Decision logic
            conditions = [
                domain_match,
                parsed.get("purpose") == "YES",
                parsed.get("historical") == "YES",
                parsed.get("suitability") == "YES",
                parsed.get("confidence", 0) >= self.confidence_threshold
            ]
            
            relevant = all(conditions)
            print(f"✅ Final Decision: {'APPROVED' if relevant else 'REJECTED'}")
            return relevant
            
        except Exception as e:
            print(f"⚠️ Evaluation Error: {str(e)}")
            return False