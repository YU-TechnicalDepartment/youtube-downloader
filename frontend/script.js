async function downloadVideo() {
    const url = document.getElementById("videoUrl").value;
    const result = document.getElementById("result");

    if (!url) {
        result.innerText = "URLを入力してください！";
        return;
    }

    result.innerText = "ダウンロード中...";
    
    const response = await fetch("https://your-render-api-url.com/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
    });

    const data = await response.json();
    result.innerText = data.message ? data.message : "エラー: " + data.error;
}
