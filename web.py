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
        .text-block {
            border: 1px solid #ddd;
            padding: 15px;
            margin: 20px auto;
            width: 60%;
            background-color: #f9f9f9;
        }
        .data-block {
            margin: 20px auto;
            font-size: 18px;
        }
        .image-block {
            margin: 20px auto;
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
    
    <!-- Display the most recent temperature and distance data -->
    <div class="data-block">
        <p><strong>Current Distance:</strong> {{ recent_distance }}</p>
        <p><strong>Current Temperature:</strong> {{ recent_temperature }}</p>
    </div>
    
    <!-- Display the content from web.txt -->
    <div class="text-block">
        <p>{{ web_text }}</p>
    </div>
    
    <!-- Display the guest image -->
    <div class="image-block">
        <img src="{{ guest_image_url }}" alt="Guest Image" style="max-width: 100%; height: auto;">
    </div>
</body>
</html>
"""


def read_recent_data(file_path):
    """Read the most recent entry from a data file."""
    if not os.path.exists(file_path):
        return None
    try:
        data = pd.read_csv(file_path, header=None, names=["timestamp", "location", "value"])
        # Convert timestamp to datetime for proper sorting
        data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
        data = data.dropna().sort_values(by="timestamp", ascending=False)
        # Return the most recent value
        return data.iloc[0]["value"] if not data.empty else "No data"
    except Exception as e:
        return f"Error reading data: {e}"


def read_web_text(file_path):
    """Read the content of web.txt."""
    if not os.path.exists(file_path):
        return "No content available"
    try:
        with open(file_path, "r") as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {e}"


def read_data(file_path):
    """Read and parse the last 10 rows of a data file into a pandas DataFrame."""
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=["timestamp", "location", "value"])
    
    # Read only the last 10 rows into a DataFrame
    data = pd.read_csv(file_path, header=None, names=["timestamp", "location", "value"]).tail(10)
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
    """Monitor page displaying text, the most recent values, and an image."""
    web_text = read_web_text("web.txt")
    recent_distance = read_recent_data(DISTANCE_DATA_FILE)
    recent_temperature = read_recent_data(TEMPERATURE_DATA_FILE)
    guest_image_url = "/static/guest_image.jpg"
    return render_template_string(
        MONITOR_TEMPLATE, 
        web_text=web_text, 
        recent_distance=recent_distance, 
        recent_temperature=recent_temperature, 
        guest_image_url=guest_image_url
    )


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
