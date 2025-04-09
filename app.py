from flask import Flask, request, render_template, send_file
import os
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
env = Environment(loader=FileSystemLoader("templates"))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    project_name = request.form["project_name"]
    service = request.form["service"]

    # Generate YAML
    template = env.get_template("github-actions.yml.j2")
    yaml_content = template.render(workflow_name=f"{service}-workflow", service=service)

    # Save to a temp file
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    yaml_path = os.path.join(temp_dir, f"{service}.yml")
    with open(yaml_path, "w") as f:
        f.write(yaml_content)

    # Send file
    return send_file(yaml_path, as_attachment=True, download_name=f"{service}.yml")

if __name__ == "__main__":
    app.run(debug=True)