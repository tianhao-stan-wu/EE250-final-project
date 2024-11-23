import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid macOS issues

from flask import Flask, render_template_string, send_file
import pandas as pd
import matplotlib.pyplot as plt
import os
import io

app = Flask(__name__)

# Paths to data files
DISTANCE_DATA_FILE = "distance_data.txt"
TEMPERATURE_DATA_FILE = "temperature_data.txt"

# HTML template with navigation bar and centered content
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
        }
        nav {
            margin-bottom: 20px;
        }
        nav a {
            margin: 0 15px;
            text-decoration: none;
            font-size: 18px;
            color: #007BFF;
        }
        nav a:hover {
            text-decoration: underline;
        }
        img {
            display: block;
            margin: 20px auto;
        }
        table {
            margin: 20px auto;
            border-collapse: collapse;
            width: 80%;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: center;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <nav>
        <a href="/">Monitor</a>
        <a href="/distance">Distance Data</a>
        <a href="/temperature">Temperature Data</a>
    </nav>
    <hr>
    <h1>{{ title }} Time Series</h1>
    
    <img src="{{ plot_url }}" alt="Time Series Plot">

    <table>
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Sensor</th>
                <th>Sensor Value</th>
            </tr>
        </thead>
        <tbody>
            {% for index, row in data.iterrows() %}
            <tr>
                <td>{{ row['timestamp'] }}</td>
                <td>{{ row['location'] }}</td>
                <td>{{ row['value'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

# HTML template for the monitor page with centered content
MONITOR_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Monitor Page</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
        }
        nav {
            margin-bottom: 20px;
        }
        nav a {
            margin: 0 15px;
            text-decoration: none;
            font-size: 18px;
            color: #007BFF;
        }
        nav a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <nav>
        <a href="/">Monitor</a>
        <a href="/distance">Distance Data</a>
        <a href="/temperature">Temperature Data</a>
    </nav>
    <hr>
    <h1>Monitor Page</h1>
    <p>This page is under development.</p>
</body>
</html>
"""

def read_data(file_path):
    """Read and parse a data file into a pandas DataFrame."""
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=["timestamp", "location", "value"])
    
    # Read the file into a DataFrame
    data = pd.read_csv(file_path, header=None, names=["timestamp", "location", "value"])
    # Convert timestamp to datetime and value to numeric
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    return data.dropna()  # Remove invalid rows

def generate_plot(data, title):
    """Generate a time series plot for the given data."""
    if data.empty:
        return None
    
    # Filter the data to include only the 10 most recent entries
    data = data.sort_values(by="timestamp").tail(10)
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(data["timestamp"], data["value"], marker="o", linestyle="-", label="Sensor Value")
    plt.title("")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    
    # Save the plot to an in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()  # Close the plot to release resources
    return buf

@app.route("/")
def monitor():
    """Monitor page (placeholder for now)."""
    return MONITOR_TEMPLATE

@app.route("/distance")
def distance_page():
    """Render the distance data page."""
    data = read_data(DISTANCE_DATA_FILE)
    # Sort the data by timestamp in descending order and keep only the last 10 entries
    data = data.sort_values(by="timestamp", ascending=False).head(10)
    return render_template_string(HTML_TEMPLATE, title="Distance Data", data=data, plot_url="/plot/distance")

@app.route("/temperature")
def temperature_page():
    """Render the temperature data page."""
    data = read_data(TEMPERATURE_DATA_FILE)
    # Sort the data by timestamp in descending order and keep only the last 10 entries
    data = data.sort_values(by="timestamp", ascending=False).head(10)
    return render_template_string(HTML_TEMPLATE, title="Temperature Data", data=data, plot_url="/plot/temperature")

@app.route("/plot/<data_type>")
def plot(data_type):
    """Generate and return the time series plot for the specified data type."""
    if data_type == "distance":
        data = read_data(DISTANCE_DATA_FILE)
        title = "Distance Data Time Series (Last 10 Entries)"
    elif data_type == "temperature":
        data = read_data(TEMPERATURE_DATA_FILE)
        title = "Temperature Data Time Series (Last 10 Entries)"
    else:
        return "Invalid data type", 404

    # Generate the plot
    plot_buf = generate_plot(data, title)
    if plot_buf is None:
        return "No data available", 404
    return send_file(plot_buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5050)
