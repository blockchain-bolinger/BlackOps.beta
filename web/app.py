#!/usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import subprocess
import json
import os

app = Flask(__name__)

# In-Memory "Datenbank" für Sessions
sessions = []

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/v1/tools')
def list_tools():
    tools = []
    for root, dirs, files in os.walk("tools"):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                tools.append(os.path.join(root, file))
    return jsonify(tools)

@app.route('/api/v1/run', methods=['POST'])
def run_tool():
    data = request.json
    tool_path = data.get('tool')
    args = data.get('args', [])
    try:
        result = subprocess.run(['python3', tool_path] + args, capture_output=True, text=True, timeout=30)
        return jsonify({'stdout': result.stdout, 'stderr': result.stderr, 'returncode': result.returncode})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/sessions', methods=['GET', 'POST'])
def handle_sessions():
    if request.method == 'GET':
        return jsonify(sessions)
    elif request.method == 'POST':
        session = request.json
        sessions.append(session)
        return jsonify(session), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)