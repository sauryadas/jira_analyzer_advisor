import pandas as pd
from langchain_ollama import ChatOllama

def analyze_and_generate_insights(df):
    print("Connecting to local Llama model for thematic analysis and insight generation...")
    
    # Initialize the local model via Ollama
    # Adjust the model name (e.g., "llama3", "mistral") as needed
    llm = ChatOllama(
        model="llama3.1",
        temperature=0.1,  # Lower temperature for more consistent analytical reports
        base_url="http://localhost:11434"
    )
    
    # Prepare data for the prompt
    # Note: Local models have smaller context windows than Gemini 2.5 Pro.
    # 150 samples is generally safe for Llama 3 (8k context), but adjust if needed.
    sample_size = min(len(df), 150) 
    summaries = df['summary'].head(sample_size).tolist()
    components = df['component'].value_counts().to_dict()
    
    prompt = f"""
    You are an expert Agile Data Analyst and DevOps Advisor. I am providing you with two pieces of data from our recent Jira tickets:
    1. The frequency distribution of ticket components: {components}
    2. A sample of recent ticket summaries: {summaries}

    Please provide an Executive Advisory Report formatted in Markdown. It must include:
    - **The Primary Bottleneck**: Based on the component frequency, what is driving the most noise?
    - **True Thematic Categories**: Look past the components and analyze the text of the summaries. Group the real underlying issues into 3-5 high-level themes.
    - **Strategic Recommendation**: Give 2 actionable recommendations to the engineering team to reduce this ticket volume.
    """

    # Local models use the .invoke() method in LangChain
    response = llm.invoke(prompt)
    
    return response.content