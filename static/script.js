let historyData = [];

function uploadFile(){

document.getElementById("fileInput").click();

}

async function translateText(){

const text = document.getElementById("inputText").value;

const language = document.getElementById("language").value;

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

document.getElementById("output").innerText=data.translation;

saveHistory("Translation completed");

}

async function summarizeText(){

const text = document.getElementById("inputText").value;

const language = document.getElementById("language").value;

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

document.getElementById("output").innerText=data.summary;

saveHistory("Summary completed");

}

function copyOutput(){

const text = document.getElementById("output").innerText;

navigator.clipboard.writeText(text);

alert("Copied");

}

function clearData(){

document.getElementById("inputText").value="";

document.getElementById("output").innerText="";

}

function saveHistory(text){

historyData.push(text);

const historyList=document.getElementById("historyList");

historyList.innerHTML="";

historyData.forEach(item=>{

const li=document.createElement("li");

li.innerText=item;

historyList.appendChild(li);

});

}

function downloadPDF(){

window.print();

}
