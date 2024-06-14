from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
import json
import os
from outline_agents import generate_learning_path

app = Flask(__name__, static_folder='Frontend/assets', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/forgotpass')
def forgotPass():
    return render_template('forgotpass.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/dash')
def dash():
    # Load course outline from JSON file
    file_path = 'db/course_outline.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            course_outline = json.load(file)
            print(course_outline)
    else:
        course_outline = {"title": "No Course Available", "sections": []}
    
    return render_template('dash.html', course_outline=course_outline)

@app.route('/generate', methods=['POST'])
def generate():
    print("Generating course outline...")
    data = request.json
    topic = data.get('topic')
    file_path = "config.yaml"  # Default file path or fetch from config if needed
    model = "gpt-3.5-turbo"        # Default model or fetch from config if needed
    api_key = ""         # Default API key or fetch from config if needed
    
    llm_config = {"model": model, "api_key": api_key}

    # Create LLM agents and generate outline
    learning_path = generate_learning_path(topic, llm_config)

    with open(f'db/course_outline.json', 'w') as file:
        json.dump(learning_path, file, indent=4)

    return jsonify({"message": "Course outline generated successfully!"})

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('Frontend/assets', path)

@app.route('/db/<path:path>')
def send_db(path):
    return send_from_directory('db', path)


if __name__ == "__main__":
    app.run(debug=True)
