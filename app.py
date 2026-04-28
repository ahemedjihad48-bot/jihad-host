# app.py
from flask import Flask, request, redirect, render_template_string
import os
import subprocess
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "bots"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

bots = {}

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>JIHAD X CODEX</title>

<style>
body{
margin:0;
padding:20px;
background:#05070d;
font-family:Arial;
color:white;
}

.box{
max-width:750px;
margin:auto;
}

.card{
background:#111827;
padding:20px;
border-radius:18px;
margin-top:15px;
border:1px solid #1f2937;
}

h1{
text-align:center;
color:#d946ef;
}

input,button{
width:100%;
padding:12px;
margin-top:10px;
border:none;
border-radius:12px;
font-size:16px;
}

button{
background:#d946ef;
color:white;
font-weight:bold;
}

.red{
background:red;
}

.orange{
background:orange;
color:black;
}

.console{
background:black;
padding:15px;
border-radius:15px;
min-height:260px;
font-family:monospace;
white-space:pre-wrap;
overflow:auto;
margin-top:10px;
}

.copybtn{
width:auto;
padding:8px 15px;
float:right;
margin-top:0;
}

.top{
display:flex;
justify-content:space-between;
align-items:center;
}
</style>
</head>

<body>

<div class="box">

<h1>JIHAD X CODEX</h1>

<div class="card">
<form action="/upload" method="post" enctype="multipart/form-data">
<input type="file" name="file" required>
<button type="submit">Upload Python Bot</button>
</form>
</div>

{% for id, bot in bots.items() %}
<div class="card">

<h3>{{bot["name"]}}</h3>
<p>Status: {{bot["status"]}}</p>

<a href="/start/{{id}}"><button>Start</button></a>
<a href="/stop/{{id}}"><button class="red">Stop</button></a>
<a href="/restart/{{id}}"><button class="orange">Restart</button></a>

<div class="card">
<div class="top">
<b>CONSOLE</b>
<button class="copybtn" onclick="copyText()">Copy</button>
</div>

<div class="console" id="console">
[INFO] {{bot["name"]}}
[INFO] Status: {{bot["status"]}}
[INFO] Waiting...
</div>
</div>

</div>
{% endfor %}

</div>

<script>
function copyText(){
let text=document.getElementById("console").innerText;
navigator.clipboard.writeText(text);
alert("Copied");
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, bots=bots)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
        file_id = str(uuid.uuid4())[:8]
        filename = file.filename
        path = os.path.join(UPLOAD_FOLDER, file_id + "_" + filename)
        file.save(path)

        bots[file_id] = {
            "name": filename,
            "path": path,
            "process": None,
            "status": "Stopped"
        }
    return redirect("/")

@app.route("/start/<id>")
def start(id):
    bot = bots[id]
    if bot["process"] is None or bot["process"].poll() is not None:
        bot["process"] = subprocess.Popen(["python", bot["path"]])
        bot["status"] = "Running"
    return redirect("/")

@app.route("/stop/<id>")
def stop(id):
    bot = bots[id]
    if bot["process"] and bot["process"].poll() is None:
        bot["process"].terminate()
        bot["status"] = "Stopped"
    return redirect("/")

@app.route("/restart/<id>")
def restart(id):
    bot = bots[id]
    if bot["process"] and bot["process"].poll() is None:
        bot["process"].terminate()

    bot["process"] = subprocess.Popen(["python", bot["path"]])
    bot["status"] = "Running"
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)