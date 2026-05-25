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

async function downloadPDF(){

const text =
document.getElementById("output").innerText;

if(!text){

alert("No output available");

return;

}

try{

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

}catch(error){

console.log(error);

alert("Download failed");

}

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

/* =========================================
   SETTINGS
========================================= */

recognition.continuous = false;

recognition.interimResults = false;

recognition.maxAlternatives = 1;

/* =========================================
   DETECT LANGUAGE FROM DROPDOWN
========================================= */

function getSpeechLanguage(){

const selectedLanguage =
document.getElementById("language").value;

/* Hindi */

if(selectedLanguage === "hi"){

return "hi-IN";

}

/* French */

if(selectedLanguage === "fr"){

return "fr-FR";

}

/* German */

if(selectedLanguage === "de"){

return "de-DE";

}

/* Spanish */

if(selectedLanguage === "es"){

return "es-ES";

}

/* Italian */

if(selectedLanguage === "it"){

return "it-IT";

}

/* Japanese */

if(selectedLanguage === "ja"){

return "ja-JP";

}

/* Default English */

return "en-US";

}

/* =========================================
   START RECORDING
========================================= */

speechBtn.addEventListener("click",()=>{

recognition.lang =
getSpeechLanguage();

recognition.start();

speechBtn.innerText =
"🎙 Listening...";

});

/* =========================================
   SPEECH RESULT
========================================= */

recognition.onresult = (event)=>{

const transcript =
event.results[0][0].transcript;

const inputBox =
document.getElementById("inputText");

inputBox.value += " " + transcript;

speechBtn.innerText =
"🎤 Speech Input";

};

/* =========================================
   SPEECH ERROR
========================================= */

recognition.onerror = (event)=>{

speechBtn.innerText =
"🎤 Speech Input";

console.log(event.error);

alert(
"Speech recognition failed. Please use Google Chrome."
);

};

/* =========================================
   SPEECH END
========================================= */

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

/* STOP PREVIOUS SPEECH */

window.speechSynthesis.cancel();

const speech =
new SpeechSynthesisUtterance();

speech.text = text;

speech.volume = 1;

speech.rate = 1;

speech.pitch = 1;

/* =========================================
   AUTO LANGUAGE DETECTION
========================================= */

const hindiRegex =
/[\u0900-\u097F]/;

const japaneseRegex =
/[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]/;

if(hindiRegex.test(text)){

speech.lang = "hi-IN";

}else if(japaneseRegex.test(text)){

speech.lang = "ja-JP";

}else{

speech.lang = "en-US";

}

/* =========================================
   LOAD BEST AVAILABLE VOICE
========================================= */

const voices =
window.speechSynthesis.getVoices();

let matchedVoice =
voices.find(voice =>
voice.lang === speech.lang
);

/* FALLBACK MATCH */

if(!matchedVoice){

matchedVoice =
voices.find(voice =>
voice.lang.startsWith(
speech.lang.split("-")[0]
)
);

}

if(matchedVoice){

speech.voice = matchedVoice;

}

/* =========================================
   SPEAK
========================================= */

window.speechSynthesis.speak(speech);

}

/* =========================================
   LOAD VOICES FOR CHROME
========================================= */

window.speechSynthesis.onvoiceschanged =
()=>{

window.speechSynthesis.getVoices();

};
