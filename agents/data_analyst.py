# data_analyst.py
from typing import Dict, Any, List, Union
import pandas as pd
import matplotlib.pyplot as plt
from core.base_agent import BaseAgent

class DataAnalystAgent(BaseAgent):
    def __init__(self, temperature: float = 0.3):
        super().__init__(temperature=temperature)
        
        # Initialize with data analysis prompt
        self._initialize_chain("""
        You are a data analysis assistant. Help analyze data and provide insights.
        Data context: {data_context}
        User request: {query}
        Provide a structured analysis with insights and visualization recommendations.
        """)
    
    def load_data(self, data: Union[str, pd.DataFrame]) -> Dict[str, Any]:
        """Load data from file path or DataFrame"""
        try:
            if isinstance(data, str):
                if data.endswith('.csv'):
                    self.df = pd.read_csv(data)
                elif data.endswith(('.xls', '.xlsx')):
                    self.df = pd.read_excel(data)
                else:
                    raise ValueError("Unsupported file format")
            elif isinstance(data, pd.DataFrame):
                self.df = data
            else:
                raise ValueError("Input must be a file path or DataFrame")
                
            return self._format_response({"shape": self.df.shape, "columns": list(self.df.columns)})
        except Exception as e:
            return self._handle_error(e, "data_loading")
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate basic statistical summary of the data"""
        try:
            summary = {
                "basic_stats": self.df.describe().to_dict(),
                "missing_values": self.df.isnull().sum().to_dict(),
                "data_types": self.df.dtypes.astype(str).to_dict()
            }
            return self._format_response(summary)
        except Exception as e:
            return self._handle_error(e, "summary_generation")
    
    def create_visualization(self, plot_type: str, x_col: str, y_col: str = None) -> Dict[str, Any]:
        """Create basic data visualizations"""
        try:
            plt.figure(figsize=(10, 6))
            
            if plot_type == "histogram":
                self.df[x_col].hist()
                plt.title(f"Histogram of {x_col}")
            elif plot_type == "scatter" and y_col:
                plt.scatter(self.df[x_col], self.df[y_col])
                plt.title(f"Scatter plot of {x_col} vs {y_col}")
            elif plot_type == "bar":
                self.df[x_col].value_counts().plot(kind='bar')
                plt.title(f"Bar plot of {x_col}")
            else:
                raise ValueError("Unsupported plot type")
                
            plt.tight_layout()
            return self._format_response({"message": f"{plot_type} plot created successfully"})
        except Exception as e:
            return self._handle_error(e, "visualization")
    
    def run(self, query: str) -> Dict[str, Any]:
        """Process data analysis queries and provide insights"""
        try:
            data_context = {
                "shape": self.df.shape if hasattr(self, 'df') else None,
                "columns": list(self.df.columns) if hasattr(self, 'df') else None,
                "sample": self.df.head().to_dict() if hasattr(self, 'df') else None
            }
            
            response = self.chain.invoke({
                "data_context": data_context,
                "query": query
            })
            return self._format_response(str(response.content))
        except Exception as e:
            return self._handle_error(e, "analysis")