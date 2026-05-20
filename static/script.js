const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const output = document.getElementById("output");
const loader = document.getElementById("loader");

/* Show File Name */

fileInput.addEventListener("change", () => {

    if(fileInput.files.length > 0){

        fileName.textContent = fileInput.files[0].name;

    }else{

        fileName.textContent = "No file selected";

    }

});

/* Upload Document */

document.getElementById("uploadForm")
.addEventListener("submit", async function(e){

    e.preventDefault();

    const file = fileInput.files[0];

    if(!file){

        alert("Please select a file");

        return;
    }

    loader.classList.remove("hidden");

    const formData = new FormData();

    formData.append("file", file);

    try{

        const response = await fetch("/upload", {

            method:"POST",
            body:formData

        });

        const result = await response.json();

        loader.classList.add("hidden");

        output.innerHTML = `
            <h2 style="color:lightgreen;">
                Upload Successful ✅
            </h2>

            <p>${result.message}</p>
        `;

    }catch(error){

        loader.classList.add("hidden");

        output.innerHTML = `
            <p style="color:red;">
                Upload failed.
            </p>
        `;
    }

});

/* Summarize */

document.getElementById("summarizeBtn")
.addEventListener("click", async function(){

    loader.classList.remove("hidden");

    try{

        const response = await fetch("/summarize");

        const result = await response.json();

        loader.classList.add("hidden");

        typeWriter(result.summary, "output");

    }catch(error){

        loader.classList.add("hidden");

        output.innerHTML = `
            <p style="color:red;">
                Summary failed.
            </p>
        `;
    }

});

/* Translate */

document.getElementById("translateBtn")
.addEventListener("click", async function(){

    const text = output.innerText;

    const target = document.getElementById("languageSelect").value;

    loader.classList.remove("hidden");

    try{

        const response = await fetch("/translate", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                text:text,
                target:target
            })

        });

        const result = await response.json();

        loader.classList.add("hidden");

        typeWriter(result.translated_text, "output");

    }catch(error){

        loader.classList.add("hidden");

        output.innerHTML = `
            <p style="color:red;">
                Translation failed.
            </p>
        `;
    }

});

/* Typewriter Animation */

function typeWriter(text, elementId, speed = 20){

    let i = 0;

    const element = document.getElementById(elementId);

    element.innerHTML = "";

    function typing(){

        if(i < text.length){

            element.innerHTML += text.charAt(i);

            i++;

            setTimeout(typing, speed);

        }

    }

    typing();

}