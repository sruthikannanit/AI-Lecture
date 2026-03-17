function getTranscript() {
    let transcriptElement = document.querySelector("ytd-transcript-renderer");

    if (!transcriptElement) {
        return "Transcript not available. Please open transcript on YouTube.";
    }

    return transcriptElement.innerText;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "GET_TRANSCRIPT") {
        sendResponse({ text: getTranscript() });
    }
})