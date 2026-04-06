import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
from src.jira_client import fetch_jira_data
from src.visualizer import generate_pareto
from src.analyzer import analyze_and_generate_insights
import os

def main():
    # 1. Configuration
    PROJECT_KEY = "SUP" # Replace with your actual Jira Project Key
    
    # 2. Extract Data
    df = fetch_jira_data(project_key=PROJECT_KEY, days_back=60, limit=500)
    
    if df.empty:
        print("No data found. Exiting.")
        return

    # 3. Generate Pareto Chart
    generate_pareto(df, column='component', output_filename='outputs/component_pareto.png')
    
    # 4. Generate AI Insights
    report = analyze_and_generate_insights(df)
    
    # 5. Save the final report
    report_path = "outputs/executive_summary.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
        
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE")
    print("="*50)
    print(f"- Pareto Chart saved to: outputs/component_pareto.png")
    print(f"- Executive Report saved to: {report_path}")
    print("\nPreview of the Executive Report:\n")
    print(report[:500] + "...\n(See full file for more)")

if __name__ == "__main__":
    main()