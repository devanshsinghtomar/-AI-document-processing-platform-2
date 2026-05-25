let historyData = [];

/* =========================================
   FILE UPLOAD
========================================= */

function uploadFile(){

document.getElementById("fileInput").click();

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

return;

}

try{

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

saveHistory("✅ Translation completed");

}catch(error){

console.log(error);

alert("Translation failed");

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

return;

}

try{

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

saveHistory("✅ Summary completed");

}catch(error){

console.log(error);

alert("Summary failed");

}

}

/* =========================================
   COPY OUTPUT
========================================= */

function copyOutput(){

const text =
document.getElementById("output").innerText;

if(!text){

alert("No text available");

return;

}

navigator.clipboard.writeText(text);

alert("Copied Successfully");

}

/* =========================================
   CLEAR DATA
========================================= */

function clearData(){

document.getElementById("inputText").value = "";

document.getElementById("output").innerText = "";

}

/* =========================================
   HISTORY
========================================= */

function saveHistory(text){

historyData.push(text);

const historyList =
document.getElementById("historyList");

if(historyList){

historyList.innerHTML = "";

historyData.forEach(item=>{

const li =
document.createElement("li");

li.innerText = item;

historyList.appendChild(li);

});

}

}

/* =========================================
   DOWNLOAD PDF
========================================= */

function downloadPDF(){

const text =
document.getElementById("output").innerText;

if(!text){

alert("No output available");

return;

}

window.print();

}

/* =========================================
   SPEECH TO TEXT FEATURE
========================================= */

const speechBtn =
document.getElementById("speechBtn");

if(speechBtn){

if('webkitSpeechRecognition' in window ||
   'SpeechRecognition' in window){

const SpeechRecognition =
window.SpeechRecognition ||
window.webkitSpeechRecognition;

const recognition =
new SpeechRecognition();

recognition.continuous = false;

recognition.interimResults = false;

recognition.lang = "en-US";

speechBtn.addEventListener("click",()=>{

recognition.start();

speechBtn.innerText = "🎙 Listening...";

});

recognition.onresult = (event)=>{

const transcript =
event.results[0][0].transcript;

document.getElementById("inputText").value +=
" " + transcript;

speechBtn.innerText =
"🎤 Speech Input";

};

recognition.onerror = ()=>{

speechBtn.innerText =
"🎤 Speech Input";

alert("Speech recognition failed");

};

recognition.onend = ()=>{

speechBtn.innerText =
"🎤 Speech Input";

};

}else{

speechBtn.disabled = true;

speechBtn.innerText =
"Speech Not Supported";

}

}

/* =========================================
   TEXT TO SPEECH FEATURE
========================================= */

function speakOutput(){

const text =
document.getElementById("output").innerText;

if(!text){

alert("No output available");

return;

}

const speech =
new SpeechSynthesisUtterance();

speech.text = text;

speech.volume = 1;

speech.rate = 1;

speech.pitch = 1;

speech.lang = "en-US";

window.speechSynthesis.speak(speech);

}
