from flask import Flask, render_template, request
import os
import subprocess
import tempfile
import shutil

app = Flask(__name__)

# Function to clone the GitHub repo
def clone_repo(repo_link):
    temp_dir = tempfile.mkdtemp()
    os.system(f"git clone {repo_link} {temp_dir}")
    return temp_dir

# Function to analyze the code
def analyze_code(repo_path):
    # Run Flake8 for style and basic errors
    flake8_result = subprocess.run(['flake8', repo_path], capture_output=True, text=True)

    # Run Bandit for security analysis
    bandit_result = subprocess.run(['bandit', '-r', repo_path], capture_output=True, text=True)

    report = "### Code Style Issues (Flake8)\n" + flake8_result.stdout + "\n"
    report += "### Security Vulnerabilities (Bandit)\n" + bandit_result.stdout
    return report

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    repo_link = request.form['repo_link']

    # Clone the repo
    repo_path = clone_repo(repo_link)

    # Analyze the code
    report = analyze_code(repo_path)

    # Clean up after analysis
    shutil.rmtree(repo_path)

    return render_template('index.html', report=report)

if __name__ == '__main__':
    app.run(debug=True)
