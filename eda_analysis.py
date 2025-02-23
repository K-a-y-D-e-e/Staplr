import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def perform_eda(file_path):
    """Performs basic Exploratory Data Analysis (EDA) on a CSV file."""
    try:
        if not file_path.endswith(".csv"):
            return "Unsupported file type. Please upload a CSV file."

        # Load the dataset
        df = pd.read_csv(file_path)

        # Basic info
        summary = {
            "Shape": df.shape,
            "Columns": list(df.columns),
            "Missing Values": df.isnull().sum().to_dict(),
            "Basic Stats": df.describe().to_dict()
        }

        # Save a correlation heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
        heatmap_path = "eda_heatmap.png"
        plt.savefig(heatmap_path)
        plt.close()

        return summary, heatmap_path

    except Exception as e:
        return f"Error during EDA: {e}"
