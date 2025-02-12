import os
import re
from urllib.parse import urlparse
import tldextract
import time
from langchain.prompts import ChatPromptTemplate
from core.base_agent import BaseAgent
from utils.logger import AgentLogger

class MailAgent(BaseAgent):
    def __init__(self, confidence_threshold=0.7, **kwargs):
        super().__init__(**kwargs)
        self.confidence_threshold = confidence_threshold
        self.logger = AgentLogger("MailAgent", log_file="logs/mail_agent.log")
        self._initialize_chain(
            prompt_template="""system
You are an expert in email verification and lead generation. 
Your task is to determine if the email {email} from {company} (official website: {official_url}) 
is suitable for receiving newsletters. Follow the structured evaluation below.

### **Domain Match** (Pre-verified)
The email domain {domain_description} the company's official website domain.

### **Purpose Analysis**
Analyze whether the email is used for:
- General inquiries
- Customer support
- Business communications
Answer 'YES' if suitable, 'NO' if personal/unrelated.

### **Historical Verification**
Based on common patterns, does this email type typically appear on company websites?
(Note: No live web access - using typical patterns)
Answer 'YES' or 'NO'.

### **Newsletter Suitability**
Final recommendation considering:
- Domain verification status
- Email purpose
- Typical business practices
Answer 'YES' with reason if suitable, 'NO' with reasoning if not.

### **Confidence Score**
Numerical confidence (0.0-1.0) based on available information.

**Strict Response Format:**
Purpose Analysis: YES|NO
Historical Verification: YES|NO
Newsletter Suitability: YES|NO - [Brief Reason]
Confidence Score: [0.0-1.0]"""
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
            # Compute domain_description based on verification result
            domain_description = "✅ MATCHES" if domain_match else "❌ DOES NOT MATCH"
            
            # Get LLM analysis by passing domain_description rather than inline expression
            response = self.chain.invoke({
                "email": email,
                "company": company,
                "official_url": official_url,
                "domain_description": domain_description
            })
            self.logger.debug("LLM analysis completed")
            
            # Ensure response is a string for parsing.
            if isinstance(response, dict):
                response_text = response.content
            else:
                response_text = response.content if hasattr(response, 'content') else str(response)

            parsed = self._parse_response(response_text)

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