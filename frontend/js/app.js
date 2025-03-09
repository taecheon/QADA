import { sendDataToFastAPI } from "./api.js";

async function handleFileUpload(event) {
    const file = event.target.files[0];

    if (!file) {
        alert("파일을 선택해주세요!");
        return;
    }

    const reader = new FileReader();

    reader.onload = async function (event) {
        try {
            const jsonData = JSON.parse(event.target.result);
            console.log("파일에서 읽은 데이터:", jsonData);

            const result = await sendDataToFastAPI(jsonData);
            if (result) {
                document.getElementById("result").innerText = JSON.stringify(result, null, 2);
            }
        } catch (error) {
            console.error("JSON 파일 처리 중 오류 발생:", error);
            alert("올바른 JSON 파일을 업로드해주세요.");
        }
    };

    reader.readAsText(file);
}

document.getElementById("jsonFileInput").addEventListener("change", handleFileUpload);
