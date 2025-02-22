# data_analyst_example.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.data_analyst import DataAnalystAgent
from utils.logger import AgentLogger
import pandas as pd
import numpy as np

# Initialize logger
logger = AgentLogger("data_analyst")

# Create data analyst agent
agent = DataAnalystAgent()

# Create sample dataset
data = {
    'age': np.random.normal(35, 10, 100),
    'income': np.random.normal(60000, 15000, 100),
    'education_years': np.random.randint(12, 22, 100),
    'satisfaction': np.random.choice(['low', 'medium', 'high'], 100)
}
df = pd.DataFrame(data)

# Load data into agent
result = agent.load_data(df)
logger.info(f"Data loaded: {result['data']}")

# Generate summary statistics
summary = agent.generate_summary()
logger.info(f"Data summary: {summary['data']}")

# Create visualizations
agent.create_visualization('histogram', 'age')
logger.info("Created age distribution histogram")

agent.create_visualization('scatter', 'education_years', 'income')
logger.info("Created education vs income scatter plot")

# Get insights
query = "What are the key patterns in the relationship between education, income, and satisfaction?"
insights = agent.run(query)
logger.info(f"Analysis insights: {insights['data']}")