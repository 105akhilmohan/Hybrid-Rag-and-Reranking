
async function uploadPDFs() {
    const files = document.getElementById("pdfFiles").files;
    const status = document.getElementById("uploadStatus");
    const button = document.getElementById("uploadButton");

    if (files.length === 0) {
        status.textContent = "Please select PDF files.";
        return;
    }

    const formData = new FormData();

    for (const file of files) {
        formData.append("files", file);
    }

    formData.append(
        "use_ocr",
        document.getElementById("useOcr").checked
    );

    button.disabled = true;
    status.textContent = "Processing PDFs and building indexes...";

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "PDF upload failed.");
        }

        status.textContent =
            `${data.message} ${data.chunk_count} chunks created.`;

        document.getElementById("documentList").innerHTML =
            "<h3>Indexed Documents</h3>" +
            data.documents.map(name =>
                `<p>${escapeHTML(name)}</p>`
            ).join("");

    } catch (error) {
        status.textContent = error.message;
    } finally {
        button.disabled = false;
    }
}


async function askQuestion() {
    const question = document.getElementById("question").value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    const button = document.getElementById("askButton");
    const answerSection = document.getElementById("answerSection");
    const passagesSection = document.getElementById("passagesSection");

    button.disabled = true;
    answerSection.textContent =
        "Retrieving, reranking and generating answer...";

    passagesSection.innerHTML = "";

    const requestData = {
        question: question,
        ollama_url: document.getElementById("ollamaUrl").value,
        ollama_model: document.getElementById("ollamaModel").value,
        candidate_k: Number(document.getElementById("candidateK").value),
        final_k: Number(document.getElementById("finalK").value)
    };

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to generate answer.");
        }

        answerSection.innerHTML =
            `<h2>Answer</h2><p>${escapeHTML(data.answer)}</p>`;

        passagesSection.innerHTML = "<h2>Retrieved Passages</h2>";

        data.passages.forEach(item => {
            const passage = document.createElement("details");
            const heading = document.createElement("summary");
            const text = document.createElement("p");

            heading.textContent =
                `${item.rank}. ${item.source} — Page ${item.page} ` +
                `(Reranker score: ${item.score})`;

            text.textContent = item.text;

            passage.appendChild(heading);
            passage.appendChild(text);
            passagesSection.appendChild(passage);
        });

    } catch (error) {
        answerSection.textContent = error.message;
    } finally {
        button.disabled = false;
    }
}


function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[character]);
}
