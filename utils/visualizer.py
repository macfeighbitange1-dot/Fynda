import matplotlib.pyplot as plt
import numpy as np

def generate_comparison_chart(output_path="performance_chart.png"):
    labels = ['Latency (ms)', 'Memory (GB)', 'Cost (Relative)']
    slm_data = [50, 2, 1]  # Based on your synthesis results
    llm_data = [500, 50, 10]
    
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, slm_data, width, label='SLM (Edge)', color='#00cf91')
    ax.bar(x + width/2, llm_data, width, label='LLM (Cloud/LoRA)', color='#ff4b4b')

    ax.set_ylabel('Scaled Units')
    ax.set_title('SLM vs LLM Edge Deployment Metrics')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_yscale('log') # Log scale because LLM metrics are orders of magnitude higher

    plt.savefig(output_path)
    plt.close()