from flask import Flask, request, render_template
from text2img import *
import json
import subprocess
app = Flask(__name__,template_folder="templates")

@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('index.html')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form.get('promptInput')
        negative_prompt = request.form.get('negativpromptInput')
        num_inference_step=int(60)
        json_data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt
        }
        json_data = json.dumps(json_data, indent=4, ensure_ascii=False)
        with open("info.json", "w", encoding="utf-8") as f:
            f.write(json_data)
        # Ghi promp và negative prompt vào file json
        # image = generate(prompt,negative_prompt,num_inference_step)
        subprocess.call("python3 text2img.py", shell=True)
        # generate(prompt,negative_prompt,num_inference_step)
        return render_template('index.html')
    return render_template('index.html')

@app.route('/upload',methods=['GET', 'POST'])
def service():
    return render_template('upload.html')

@app.route("/information", methods=["GET", "POST"])
def infomation():
    return render_template("information.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port="8000")
