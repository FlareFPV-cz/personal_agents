import sys
import os
import textwrap

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.code_analyst import CodeHelper

def main():
    # Initialize analyzer with enhanced configuration
    analyzer = CodeHelper(
        quality_threshold=8.5,
        model_name="llama3-70b-8192",
        temperature=0.2,
        config_path=".cqarc"
    )

    # Example 1: Analyze code string
    print("\n🔍 Analyzing Code String:")
    sample_code = textwrap.dedent('''
        def calculate(a, b):
            # Add two numbers
            return a + b

        def multiply(x, y):
            result = x * y
            return result
    ''')
    
    analysis = analyzer.analyze(sample_code)
    
    if analysis['success']:
        data = analysis['data']
        print(f"""
        🏆 Quality Score: {data['quality_score']:.1f}/10
        ✅ Approved: {'Yes' if data['quality_score'] >= 8.5 else 'No'}
        
        📊 Key Metrics:
        - Security Score: {data['security']['score']}/100
        - Max Complexity: {data['complexity']['max_complexity']} (Threshold: {data['complexity']['threshold']})
        - Doc Coverage: {data['documentation']['coverage']:.1f}%
        - Duplication: {data['duplication']['percentage']:.1f}%
        - Test Coverage: {data['coverage']['coverage']}%
        
        ⚠️ Top Issues:
        {chr(10).join(f' - {issue}' for issue in data['security']['issues'][:2])}
        {chr(10).join(f' - Complexity: {data['complexity']['max_complexity']} in calculate')}
        
        💡 Recommendations:
        {chr(10).join(f' - {rec}' for rec in data['llm_suggestions'][:3])}
        
        🛠️ Auto-Fixes Available:
        {chr(10).join(f' - {fix}' for fix in data['auto_fixes'][:2])}
        
        """)
    else:
        print(f"❌ Analysis failed: {analysis['error']}")

if __name__ == "__main__":
    main()