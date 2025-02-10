import os
import re
from urllib.parse import urlparse
import tldextract
import time
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from base_agent import BaseAgent
from utils.logger import AgentLogger

class MailAgent(BaseAgent):
    def __init__(self, confidence_threshold=0.7, **kwargs):
        super().__init__(**kwargs)
        self.confidence_threshold = confidence_threshold
        self.logger = AgentLogger("MailAgent", log_file="logs/mail_agent.log")
        self._initialize_chain(
            input_variables=["email", "company", "official_url", "domain_match"],
            prompt_template=(
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

    def run(self, email, company, official_url):
        """Enhanced evaluation with domain check and structured parsing."""
        self.logger.info(f"Starting evaluation for email: {email}")
        start_time = time.time()
        
        try:
            # Programmatic domain verification
            domain_match = self._extract_domain(email, official_url)
            self.logger.debug(f"Domain match result: {domain_match}")
            
            # Get LLM analysis
            response = self.chain.run({
                "email": email,
                "company": company,
                "official_url": official_url,
                "domain_match": domain_match
            })
            self.logger.debug("LLM analysis completed")

            # Parse response
            parsed = self._parse_response(response)
            duration = time.time() - start_time
            self.logger.info(f"Evaluation completed in {duration:.2f} seconds")
            
            # Format result
            result = {
                'email': email,
                'company': company,
                'domain_match': domain_match,
                'analysis': parsed,
                'approved': parsed['confidence'] >= self.confidence_threshold
            }
            
            return self._format_response(result)
            
        except Exception as e:
            self.logger.error(f"Error during email evaluation: {str(e)}")
            return self._handle_error(e, "email evaluation")