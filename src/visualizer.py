import matplotlib.pyplot as plt
import os

def generate_pareto(df, column='component', output_filename='outputs/pareto_chart.png'):
    print(f"Generating Pareto chart for column: '{column}'...")
    
    # Ensure output directory exists
    os.makedirs('outputs', exist_ok=True)

    # Count frequency and sort
    counts = df[column].value_counts().to_frame()
    counts.columns = ['frequency']
    counts = counts.sort_values(by='frequency', ascending=False)
    
    # Calculate cumulative percentage
    counts['cumulative_perc'] = counts['frequency'].cumsum() / counts['frequency'].sum() * 100

    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.bar(counts.index, counts['frequency'], color="C0")
    ax1.set_ylabel("Ticket Count", color="C0")
    ax1.tick_params(axis='y', labelcolor="C0")

    ax2 = ax1.twinx()
    ax2.plot(counts.index, counts['cumulative_perc'], color="C1", marker="D", ms=7)
    ax2.axhline(80, color="red", linestyle="--", label="80% Cutoff")
    ax2.set_ylabel("Cumulative Percentage (%)", color="C1")
    ax2.tick_params(axis='y', labelcolor="C1")
    ax2.set_ylim([0, 105])

    # Formatting
    ax1.set_xticklabels(counts.index, rotation=45, ha='right')
    plt.title(f"Pareto Analysis of Ticket {column.capitalize()}s")
    fig.tight_layout()

    # Save and close
    plt.savefig(output_filename)
    plt.close()
    print(f"Pareto chart saved to {output_filename}")