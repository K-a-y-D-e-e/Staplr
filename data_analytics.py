import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import io
import os

# Initialize Flask App
app = Flask(__name__)

##### DATA ANALYTICS (EDA) #####
@app.route("/eda", methods=["POST"])
def eda():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()

    # Only allow CSV files
    if extension != ".csv":
        return jsonify({"error": "Unsupported file format. Only CSV is allowed."}), 400

    try:
        df = pd.read_csv(io.StringIO(file.stream.read().decode("utf-8")))
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 400

    # Basic EDA for structured data
    eda_summary = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict(),
        "describe": df.describe().to_dict()
    }
    result = {"eda_summary": eda_summary}

    # Generate a correlation heatmap if numeric data is present and more than one column exists
    numeric_df = df.select_dtypes(include=["number"])
    if numeric_df.shape[1] > 1:
        plt.figure(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
        plt.savefig("heatmap.png")
        plt.close()
        result["heatmap"] = "heatmap.png"

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)