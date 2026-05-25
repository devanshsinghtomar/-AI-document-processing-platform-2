<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>AI Document Translator</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:'Poppins',sans-serif;
}

body{
background:linear-gradient(135deg,#0f172a,#111827,#1e293b);
min-height:100vh;
color:white;
padding:20px;
}

.container{
max-width:1400px;
margin:auto;
}

.navbar{
display:flex;
justify-content:space-between;
align-items:center;
padding:20px 30px;
background:rgba(255,255,255,0.08);
border-radius:20px;
backdrop-filter:blur(15px);
margin-bottom:25px;
}

.logo{
font-size:28px;
font-weight:700;
}

.nav-links{
display:flex;
gap:15px;
align-items:center;
}

.nav-links a{
text-decoration:none;
color:white;
padding:10px 18px;
border-radius:12px;
background:rgba(255,255,255,0.08);
transition:0.3s;
}

.nav-links a:hover{
background:#2563eb;
}

.main-grid{
display:grid;
grid-template-columns:1fr 1fr;
gap:25px;
}

.card{
background:rgba(255,255,255,0.08);
padding:25px;
border-radius:25px;
backdrop-filter:blur(15px);
box-shadow:0 10px 30px rgba(0,0,0,0.3);
}

.card h2{
margin-bottom:20px;
font-size:24px;
}

.upload-box{
border:2px dashed rgba(255,255,255,0.2);
padding:30px;
text-align:center;
border-radius:20px;
cursor:pointer;
transition:0.3s;
margin-bottom:20px;
}

.upload-box:hover{
background:rgba(255,255,255,0.05);
}

.upload-box i{
font-size:50px;
margin-bottom:15px;
color:#38bdf8;
}

textarea{
width:100%;
height:350px;
background:rgba(255,255,255,0.06);
border:none;
outline:none;
resize:none;
border-radius:18px;
padding:20px;
color:white;
font-size:15px;
margin-top:15px;
}

.output-box{
height:550px;
overflow-y:auto;
background:rgba(255,255,255,0.06);
padding:20px;
border-radius:20px;
line-height:1.8;
white-space:pre-wrap;
}

.controls{
display:grid;
grid-template-columns:repeat(3,1fr);
gap:15px;
margin-top:20px;
}

button,select{
padding:14px;
border:none;
border-radius:14px;
font-size:15px;
font-weight:600;
}

select{
background:#1e293b;
color:white;
}

button{
cursor:pointer;
color:white;
transition:0.3s;
}

button:hover{
transform:translateY(-2px);
}

.btn-upload{
background:linear-gradient(135deg,#3b82f6,#06b6d4);
}

.btn-translate{
background:linear-gradient(135deg,#8b5cf6,#ec4899);
}

.btn-summary{
background:linear-gradient(135deg,#10b981,#14b8a6);
}

.btn-copy{
background:linear-gradient(135deg,#f59e0b,#f97316);
}

.btn-clear{
background:linear-gradient(135deg,#ef4444,#dc2626);
}

.btn-download{
background:linear-gradient(135deg,#06b6d4,#2563eb);
}

.btn-speech{
background:linear-gradient(135deg,#14b8a6,#0f766e);
}

.btn-tts{
background:linear-gradient(135deg,#6366f1,#4338ca);
}

.btn-pause{
background:linear-gradient(135deg,#f59e0b,#ea580c);
}

.btn-resume{
background:linear-gradient(135deg,#22c55e,#15803d);
}

.loading{
display:none;
text-align:center;
margin-top:15px;
}

.status-bar{
margin-top:20px;
padding:14px 18px;
background:rgba(37,99,235,0.2);
border:1px solid rgba(255,255,255,0.08);
border-radius:14px;
font-size:15px;
font-weight:500;
color:#e2e8f0;
}

.file-name{
margin-top:12px;
padding:12px 15px;
background:rgba(255,255,255,0.05);
border-radius:12px;
font-size:14px;
color:#cbd5e1;
word-break:break-word;
}

@media(max-width:1000px){

.main-grid{
grid-template-columns:1fr;
}

.controls{
grid-template-columns:1fr 1fr;
}

}

@media(max-width:600px){

.controls{
grid-template-columns:1fr;
}

.navbar{
flex-direction:column;
gap:15px;
}

}

</style>

</head>

<body>

<div class="container">

<div class="navbar">

<div class="logo">
🌍 AI Translator
</div>

<div class="nav-links">

<a href="/history-page">
<i class="fa-solid fa-clock-rotate-left"></i>
History
</a>

<a href="/logout">
<i class="fa-solid fa-right-from-bracket"></i>
Logout
</a>

</div>

</div>

<div class="main-grid">

<div class="card">

<h2>📂 Upload Document</h2>

<div class="upload-box"
onclick="document.getElementById('fileInput').click()">

<i class="fa-solid fa-cloud-arrow-up"></i>

<h3>Choose File</h3>

<p>Upload TXT, PDF or DOCX</p>

</div>

<input type="file" id="fileInput" hidden>

<div class="file-name" id="selectedFileName">
No file selected
</div>

<textarea
id="inputText"
placeholder="Uploaded text will appear here..."></textarea>

<div class="controls">

<select id="language">

<option value="hi">Hindi</option>
<option value="fr">French</option>
<option value="de">German</option>
<option value="es">Spanish</option>
<option value="it">Italian</option>
<option value="ja">Japanese</option>

</select>

<button class="btn-upload"
onclick="uploadFile()">
Upload
</button>

<button class="btn-translate"
onclick="translateText()">
Translate
</button>

<button class="btn-summary"
onclick="summarizeText()">
Summarize
</button>

<button class="btn-copy"
onclick="copyText()">
Copy
</button>

<button class="btn-clear"
onclick="clearText()">
Clear
</button>

<button class="btn-download"
onclick="downloadPDF()">
Download
</button>

<button class="btn-speech"
id="speechBtn">
🎤 Start Input
</button>

<button class="btn-pause"
onclick="stopSpeechInput()">
⏹ Stop Input
</button>

<button class="btn-tts"
onclick="speakOutput()">
🔊 Start Output
</button>

<button class="btn-pause"
onclick="pauseOutput()">
⏸ Pause Output
</button>

<button class="btn-resume"
onclick="resumeOutput()">
▶ Resume Output
</button>

<button class="btn-clear"
onclick="stopOutput()">
⏹ Stop Output
</button>

</div>

<div class="status-bar" id="statusBar">
✅ Ready
</div>

<div class="loading" id="loading">

<p>Processing...</p>

</div>

</div>

<div class="card">

<h2>📄 Output</h2>

<div class="output-box" id="output">

Your translated or summarized result will appear here...

</div>

</div>

</div>

</div>

<script>

let historyData = [];

/* =========================================
   STATUS BAR
========================================= */

function updateStatus(message){

const statusBar =
document.getElementById("statusBar");

if(statusBar){

statusBar.innerText = message;

}

}

/* =========================================
   SHOW SELECTED FILE NAME
========================================= */

const fileInput =
document.getElementById("fileInput");

if(fileInput){

fileInput.addEventListener("change",()=>{

const fileNameBox =
document.getElementById("selectedFileName");

if(fileInput.files.length > 0){

const fileName =
fileInput.files[0].name;

fileNameBox.innerText =
"📂 Selected File: " + fileName;

updateStatus(
"📤 File selected: " + fileName
);

}else{

fileNameBox.innerText =
"No file selected";

}

});

}

/* =========================================
   FILE UPLOAD
========================================= */

async function uploadFile(){

const file =
document.getElementById('fileInput').files[0];

if(!file){

alert('Please choose a file');

updateStatus(
"⚠ Please choose a file"
);

return;

}

const formData = new FormData();

formData.append('file', file);

try{

updateStatus(
"📤 Uploading file..."
);

const response = await fetch('/upload',{

method:'POST',
body:formData

});

const data = await response.json();

if(data.error){

alert(data.error);

updateStatus(
"❌ Upload failed"
);

return;

}

document.getElementById('inputText').value =
data.text;

document.getElementById('output').innerText =
'✅ File uploaded successfully';

updateStatus(
"✅ File uploaded successfully"
);

}catch(error){

console.log(error);

alert('Upload failed');

updateStatus(
"❌ Upload failed"
);

}

}

/* =========================================
   TRANSLATE TEXT
========================================= */

async function translateText(){

const text =
document.getElementById("inputText").value;

const language =
document.getElementById("language").value;

if(!text){

alert("Please enter or upload text");

updateStatus(
"⚠ Please enter or upload text"
);

return;

}

try{

updateStatus(
"🌍 Translating text..."
);

const response = await fetch("/translate",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
text:text,
language:language
})

});

const data = await response.json();

document.getElementById("output").innerText =
data.translation || data.result;

updateStatus(
"✅ Translation completed"
);

}catch(error){

console.log(error);

alert("Translation failed");

updateStatus(
"❌ Translation failed"
);

}

}

/* =========================================
   SUMMARIZE TEXT
========================================= */

async function summarizeText(){

const text =
document.getElementById("inputText").value;

const language =
document.getElementById("language").value;

if(!text){

alert("Please enter or upload text");

updateStatus(
"⚠ Please enter or upload text"
);

return;

}

try{

updateStatus(
"📝 Generating summary..."
);

const response = await fetch("/summarize",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
text:text,
language:language
})

});

const data = await response.json();

document.getElementById("output").innerText =
data.summary || data.result;

updateStatus(
"✅ Summary completed"
);

}catch(error){

console.log(error);

alert("Summary failed");

updateStatus(
"❌ Summary failed"
);

}

}

/* =========================================
   COPY OUTPUT
========================================= */

function copyText(){

const text =
document.getElementById("output").innerText;

if(!text){

alert("No text available");

updateStatus(
"⚠ No text available"
);

return;

}

navigator.clipboard.writeText(text);

alert("Copied Successfully");

updateStatus(
"✅ Output copied"
);

}

/* =========================================
   CLEAR DATA
========================================= */

function clearText(){

document.getElementById("inputText").value='';

document.getElementById("output").innerText=
'Output cleared';

updateStatus(
"🗑 Data cleared"
);

}

/* =========================================
   DOWNLOAD PDF
========================================= */

async function downloadPDF(){

const text =
document.getElementById("output").innerText;

if(!text ||
text === "Output cleared"){

alert("No output available");

updateStatus(
"⚠ No output available"
);

return;

}

try{

updateStatus(
"📄 Downloading PDF..."
);

const response = await fetch("/download",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
text:text
})

});

if(!response.ok){

alert("PDF generation failed");

updateStatus(
"❌ PDF generation failed"
);

return;

}

const blob = await response.blob();

const blobUrl =
window.URL.createObjectURL(
new Blob([blob],{
type:"application/pdf"
})
);

const link =
document.createElement("a");

link.href = blobUrl;

link.download =
"translated_document.pdf";

document.body.appendChild(link);

link.click();

link.remove();

window.URL.revokeObjectURL(blobUrl);

updateStatus(
"✅ PDF downloaded"
);

}catch(error){

console.log(error);

alert("Download failed");

updateStatus(
"❌ Download failed"
);

}

}

/* =========================================
   SPEECH TO TEXT FEATURE
========================================= */

const speechBtn =
document.getElementById("speechBtn");

let recognition;

if('webkitSpeechRecognition' in window ||
   'SpeechRecognition' in window){

const SpeechRecognition =
window.SpeechRecognition ||
window.webkitSpeechRecognition;

recognition =
new SpeechRecognition();

recognition.continuous = true;

recognition.interimResults = false;

recognition.maxAlternatives = 1;

function getSpeechLanguage(){

const selectedLanguage =
document.getElementById("language").value;

if(selectedLanguage === "hi"){
return "hi-IN";
}

if(selectedLanguage === "fr"){
return "fr-FR";
}

if(selectedLanguage === "de"){
return "de-DE";
}

if(selectedLanguage === "es"){
return "es-ES";
}

if(selectedLanguage === "it"){
return "it-IT";
}

if(selectedLanguage === "ja"){
return "ja-JP";
}

return "en-US";

}

speechBtn.addEventListener("click",()=>{

recognition.lang =
getSpeechLanguage();

recognition.start();

speechBtn.innerText =
"🎙 Listening...";

updateStatus(
"🎙 Listening..."
);

});

recognition.onresult = (event)=>{

const transcript =
event.results[event.results.length - 1][0].transcript;

const inputBox =
document.getElementById("inputText");

inputBox.value += " " + transcript;

updateStatus(
"✅ Speech converted to text"
);

};

recognition.onerror = ()=>{

speechBtn.innerText =
"🎤 Start Input";

updateStatus(
"❌ Speech recognition failed"
);

};

recognition.onend = ()=>{

speechBtn.innerText =
"🎤 Start Input";

};

}else{

speechBtn.disabled = true;

speechBtn.innerText =
"Speech Not Supported";

}

/* =========================================
   STOP INPUT
========================================= */

function stopSpeechInput(){

if(recognition){

recognition.stop();

updateStatus(
"⏹ Speech input stopped"
);

}

}

/* =========================================
   TEXT TO SPEECH FEATURE
========================================= */

let currentSpeech = null;

function speakOutput(){

const text =
document.getElementById("output").innerText;

if(!text ||
text === "Output cleared"){

alert("No output available");

updateStatus(
"⚠ No output available"
);

return;

}

window.speechSynthesis.cancel();

currentSpeech =
new SpeechSynthesisUtterance();

currentSpeech.text = text;

currentSpeech.volume = 1;
currentSpeech.rate = 1;
currentSpeech.pitch = 1;

const hindiRegex =
/[\u0900-\u097F]/;

const japaneseRegex =
/[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]/;

if(hindiRegex.test(text)){

currentSpeech.lang = "hi-IN";

}else if(japaneseRegex.test(text)){

currentSpeech.lang = "ja-JP";

}else{

currentSpeech.lang = "en-US";

}

const voices =
window.speechSynthesis.getVoices();

let matchedVoice =
voices.find(voice =>
voice.lang === currentSpeech.lang
);

if(!matchedVoice){

matchedVoice =
voices.find(voice =>
voice.lang.startsWith(
currentSpeech.lang.split("-")[0]
)
);

}

if(matchedVoice){

currentSpeech.voice = matchedVoice;

}

updateStatus(
"🔊 Reading output..."
);

window.speechSynthesis.speak(currentSpeech);

currentSpeech.onend = ()=>{

updateStatus(
"✅ Audio playback completed"
);

};

}

/* =========================================
   PAUSE OUTPUT
========================================= */

function pauseOutput(){

window.speechSynthesis.pause();

updateStatus(
"⏸ Audio paused"
);

}

/* =========================================
   RESUME OUTPUT
========================================= */

function resumeOutput(){

window.speechSynthesis.resume();

updateStatus(
"▶ Audio resumed"
);

}

/* =========================================
   STOP OUTPUT
========================================= */

function stopOutput(){

window.speechSynthesis.cancel();

updateStatus(
"⏹ Audio stopped"
);

}

/* =========================================
   LOAD VOICES
========================================= */

window.speechSynthesis.onvoiceschanged =
()=>{

window.speechSynthesis.getVoices();

};

/* =========================================
   INITIAL STATUS
========================================= */

window.onload = ()=>{

updateStatus(
"✅ Ready"
);

};

</script>

</body>
</html>
