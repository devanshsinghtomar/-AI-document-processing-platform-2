function setOutput(text) {

    document.getElementById("output")
        .innerText = text;
}

/* UPLOAD */

async function uploadFile() {

    try {

        setOutput("Uploading files...");

        let fileInput =
            document.getElementById("fileInput");

        if(fileInput.files.length === 0) {

            setOutput(
                "Please select files first"
            );

            return;
        }

        let formData = new FormData();

        for(let i = 0; i < fileInput.files.length; i++) {

            formData.append(
                "file",
                fileInput.files[i]
            );
        }

        let response = await fetch("/upload", {

            method: "POST",

            body: formData
        });

        let data = await response.json();

        setOutput(data.message);

    } catch(error) {

        setOutput(
            "Upload Error:\n" + error
        );
    }
}

/* SUMMARY */

async function summarize() {

    try {

        setOutput(
            "Generating AI summary...\nPlease wait..."
        );

        let response = await fetch("/summarize", {

            method: "POST"
        });

        let data = await response.json();

        setOutput(data.summary);

    } catch(error) {

        setOutput(
            "Summary Error:\n" + error
        );
    }
}

/* TRANSLATE */

async function translateText() {

    try {

        setOutput(
            "Translating document..."
        );

        let response = await fetch("/translate", {

            method: "POST"
        });

        let data = await response.json();

        setOutput(data.translated);

    } catch(error) {

        setOutput(
            "Translation Error:\n" + error
        );
    }
}

/* EXTRACT */

async function extractData() {

    try {

        setOutput(
            "Extracting structured data..."
        );

        let response = await fetch("/extract", {

            method: "POST"
        });

        let data = await response.json();

        setOutput(
            JSON.stringify(data, null, 2)
        );

    } catch(error) {

        setOutput(
            "Extraction Error:\n" + error
        );
    }
}

/* CHAT */

async function chatDocument() {

    try {

        let question =
            document.getElementById("question").value;

        if(question === "") {

            setOutput(
                "Please enter a question"
            );

            return;
        }

        setOutput(
            "AI is analyzing document..."
        );

        let response = await fetch("/chat", {

            method: "POST",

            headers: {

                "Content-Type":
                "application/json"
            },

            body: JSON.stringify({

                question: question
            })
        });

        let data = await response.json();

        setOutput(data.answer);

    } catch(error) {

        setOutput(
            "Chat Error:\n" + error
        );
    }
}

/* EXPORT */

function downloadJSON() {

    let content =
        document.getElementById("output").innerText;

    let blob = new Blob(

        [content],

        {
            type: "application/json"
        }
    );

    let a =
        document.createElement("a");

    a.href =
        URL.createObjectURL(blob);

    a.download = "output.json";

    a.click();
}

/* CLEAR */

function clearOutput() {

    setOutput("");
}

/* HOME */

function showHome() {

    setOutput(
        "Welcome to AI Document Processing Platform"
    );
}