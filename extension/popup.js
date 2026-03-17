document.addEventListener("DOMContentLoaded", function () {

    // get elements safely
    const analyzeBtn = document.getElementById("analyzeBtn");
    const askBtn = document.getElementById("askBtn");
    const questionInput = document.getElementById("question");

    // if elements missing → stop error
    if (!analyzeBtn || !askBtn || !questionInput) {
        console.error("❌ HTML elements not found");
        return;
    }

    // 🔥 ANALYZE BUTTON
    analyzeBtn.addEventListener("click", function () {

        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {

            chrome.tabs.sendMessage(
                tabs[0].id,
                { action: "GET_TRANSCRIPT" },
                async function (response) {

                    if (!response || !response.text) {
                        alert("❌ Open transcript on YouTube first");
                        return;
                    }

                    try {
                        let res = await fetch("http://127.0.0.1:8000/analyze", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({
                                text: response.text,
                                title: document.title
                            })
                        });

                        let data = await res.json();

                        console.log(data.result);
                        alert("✅ Analysis Done (Check F12)");

                    } catch (err) {
                        console.error(err);
                        alert("❌ Backend error");
                    }
                }
            );
        });
    });

    // 🔥 ASK BUTTON
    askBtn.addEventListener("click", async function () {

        let question = questionInput.value;

        if (!question) {
            alert("⚠️ Enter a question");
            return;
        }

        try {
            let res = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            });

            let data = await res.json();

            console.log(data.answer);
            alert(data.answer);

        } catch (err) {
            console.error(err);
            alert("❌ Backend error");
        }
    });

});