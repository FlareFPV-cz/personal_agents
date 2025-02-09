import os
import re
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("❌ GROQ_API_KEY is missing! Make sure it's in the .env file.")

groq_llm = ChatGroq(temperature=0.2, model_name="mixtral-8x7b-32768")

class MaiilAgent:
    def __init__(self, llm=groq_llm):
        self.llm = llm
        self.prompt = PromptTemplate(
            input_variables=["email", "company", "official_url"],
            template=(
                "You are an expert in email verification and lead generation. "
                "Your task is to determine if the email {email} from {company} (official website: {official_url}) "
                "is suitable for receiving newsletters. Follow the structured evaluation below.\n\n"
                
                "### **Step 1: Domain Match**\n"
                "Does the email domain match the company's official website domain?\n"
                "- Answer 'yes' or 'no'.\n"
                
                "### **Step 2: Purpose of Email**\n"
                "Analyze whether the email is used for general inquiries, customer support, or business communications.\n"
                "- Answer 'yes' if it's for general or business use.\n"
                "- Answer 'no' if it's personal or unrelated.\n"
                
                "### **Step 3: Official Website Verification**\n"
                "Check if this email is listed on {official_url} as a contact point.\n"
                "- Answer 'yes' or 'no'.\n"
                
                "### **Step 4: Newsletter Suitability**\n"
                "Should we send newsletters here? Consider if it is a **generic, business, or corporate email**.\n"
                "- Answer 'yes' if the email is suitable and explain why.\n"
                "- Answer 'no' if it is unsuitable and provide reasoning.\n"
                
                "### **Step 5: Confidence Score**\n"
                "Give a confidence score (0.0 - 1.0) based on the evaluation.\n\n"
                
                "**Example Response:**\n"
                "- **Domain Match:** Yes\n"
                "- **Purpose of Email:** Yes, it's a business contact.\n"
                "- **Official Website Verification:** Yes, listed on the site.\n"
                "- **Newsletter Suitability:** Yes, it's a company-wide contact email.\n"
                "- **Confidence Score:** 0.92"
            )
        )
        self.relevance_chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def extract_confidence(self, response):
        """Extract confidence score from LLM response."""
        match = re.search(r"Confidence score: ([0-9.]+)", response)
        return float(match.group(1)) if match else 0.0

    def evaluate_relevance(self, email, company, official_url):
        """Use AI to determine if an email is relevant, with structured analysis."""
        print(f"🔍 Evaluating: {email}")

        response = self.relevance_chain.run({
            "email": email,
            "company": company,
            "official_url": official_url
        })

        confidence = self.extract_confidence(response)
        relevant = "yes" in response.lower() and confidence >= 0.7  # Require 70% confidence

        print(f"🤖 AI Response:\n{response}\n➡ Confidence: {confidence:.2f}")
        return relevant
