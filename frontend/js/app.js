import { sendDataToFastAPI } from "./api.js";

document.getElementById("jsonFileInput").addEventListener("change", handleFileUpload);

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
                displayData(result); // ✅ 데이터 표시
                drawCharts(result);  // ✅ 그래프 그리기
            }
        } catch (error) {
            console.error("JSON 파일 처리 중 오류 발생:", error);
            alert("올바른 JSON 파일을 업로드해주세요.");
        }
    };

    reader.readAsText(file);
}

// ✅ 1. 기본 정보 표시
function displayData(data) {
    document.getElementById("avgPassageLength").innerText = data.sample_num_info.avg_passage_length.toFixed(2);
    document.getElementById("avgQueryLength").innerText = data.sample_num_info.avg_query_length.toFixed(2);
    document.getElementById("avgAnswerLength").innerText = data.sample_num_info.avg_answer_length.toFixed(2);
    document.getElementById("avgQpPrecision").innerText = data.sample_num_info.avg_qp_precision.toFixed(2);
}

// ✅ 2. 차트 그리기
function drawCharts(data) {
    createBarChart("passageChart", "Passage 길이 분포", data.distribution.passage_length);
    createBarChart("queryChart", "Query 길이 분포", data.distribution.query_length);
    createBarChart("answerChart", "Answer 길이 분포", data.distribution.answer_length);
    createBarChart("qpPrecisionChart", "QP Precision 분포", data.distribution.qp_precision);
}

// ✅ 3. Chart.js를 이용해 막대 그래프 생성
function createBarChart(canvasId, label, dataset) {
    const ctx = document.getElementById(canvasId).getContext("2d");
    const labels = Object.keys(dataset);
    const values = Object.values(dataset);

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: values,
                backgroundColor: "rgba(75, 192, 192, 0.5)",
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
