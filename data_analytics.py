import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import io

# Initialize Flask App
app = Flask(__name__)

##### DATA ANALYTICS (EDA) #####
@app.route("/eda", methods=["POST"])
def eda():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    df = pd.read_csv(io.StringIO(file.stream.read().decode("utf-8")))
    
    # Basic Info
    eda_summary = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict(),
        "describe": df.describe().to_dict()
    }
    
    # Visualization (Save & Return a Plot)
    plt.figure(figsize=(10,6))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.savefig("heatmap.png")
    
    return jsonify({"eda_summary": eda_summary, "heatmap": "heatmap.png"})

if __name__ == "__main__":
    app.run(debug=True)
