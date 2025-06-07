// List of simulator experts with pictures and names
const experts = [
    { name: "Dr. Witty Owl", img: "./images/owl.png" },
    { name: "Professor Cat", img: "./images/cat.png" },
    { name: "Mr. Foxy Clever", img: "./images/fox.png" },
    { name: "Ms. Bunny Bright", img: "./images/bunny.png" },
    { name: "Captain Panda", img: "./images/panda.png" }
];
let expertHint = false; // Expert suggested status check variable

let remainingAnswers = []; // Global variable to store remaining answers after 50/50

// 50/50 help 
function handle5050Hint() {
    const hint50Button = document.getElementById("hint-50-50");
    if (hint50Button) {
        hint50Button.style.visibility = "hidden"; // Hide help button after pressing
    }

    // console.log("Đang sử dụng trợ giúp 50/50...");

    // Find the correct answer button
    const correctAnswerElement = Array.from(document.querySelectorAll(".answer-btn")).find(answer =>
        answer.getAttribute("onclick").includes("true")
    );
    if (!correctAnswerElement) {
        console.error("Không tìm thấy đáp án đúng trong DOM.");
        return; // Stop if not found
    }
    const correctAnswer = correctAnswerElement.textContent;

    // Get all answers from DOM
    const allAnswers = Array.from(document.querySelectorAll(".answer-btn")).map(answer => answer.textContent);

    // console.log("Trước khi gọi API, remainingAnswers:", remainingAnswers);

    // Send a request to the 50/50 help API
    fetch("https://tuanspace.uk/help/50-50", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correct_answer: correctAnswer, all_answers: allAnswers })
    })
    .then(response => response.json())
    .then(data => {
        const remainingChoices = data.remaining_choices;
        // console.log("Phản hồi từ API, remainingChoices:", remainingChoices);

        // Update remainingAnswers
        remainingAnswers = remainingChoices;
        // console.log("Sau khi gọi API và cập nhật, remainingAnswers:", remainingAnswers);

        // Hide answers that are not in the remaining list
        const answers = document.querySelectorAll(".answer-btn");
        answers.forEach(answer => {
            if (!remainingChoices.includes(answer.textContent)) {
                answer.style.visibility = "hidden"; // Hide answers not on the remaining list
            }
        });

        document.querySelectorAll(".answer-btn").forEach(answer => {
            // console.log(`Đáp án "${answer.textContent}" trạng thái:`, answer.style.visibility);
        });
    })
    .catch(error => {
        console.error("Lỗi khi gọi API:", error);
    });
}

// help call expert
function handlePhoneAFriend() {
    expertHint = true; // Mark that expert help has been used

    // Hide "Call Expert" button after pressing
    const hintPhoneButton = document.getElementById("hint-phone");
    if (hintPhoneButton) {
        hintPhoneButton.style.visibility = "hidden"; // Ẩn nút
        hintPhoneButton.disabled = true; // Vô hiệu hóa nút
    }

    // console.log("Đang sử dụng trợ giúp Chuyên gia...");

    // Get a list of answers to suggest (preferably from `remainingAnswers` if available)
    const answers = remainingAnswers.length > 0 
        ? remainingAnswers 
        : Array.from(document.querySelectorAll(".answer-btn")).map(answer => answer.textContent);

    // console.log("Trước khi gọi Chuyên gia, remainingAnswers:", remainingAnswers);

    // Find the correct answer from DOM
    const correctAnswerElement = Array.from(document.querySelectorAll(".answer-btn")).find(answer =>
        answer.getAttribute("onclick").includes("true")
    );
    if (!correctAnswerElement) {
        console.error("Không tìm thấy đáp án đúng trong DOM.");
        return; // Stop if not found
    }
    const correctAnswer = correctAnswerElement.textContent;

    // console.log("Tất cả đáp án để gợi ý:", answers);
    // console.log("Đáp án đúng:", correctAnswer);

    // Displays the container containing the list of experts
    const phoneContainer = document.getElementById("phone-a-friend-container");
    if (phoneContainer) {
        phoneContainer.style.display = "block"; // Show list of experts
    }

    const expertsList = document.getElementById("experts-list");
    if (expertsList) {
        expertsList.innerHTML = ""; // Delete old expert list
        experts.forEach((expert, index) => {
            const expertButton = document.createElement("button");
            expertButton.className = "expert-btn";
            expertButton.innerHTML = `
                <img src="${expert.img || "default-expert.png"}" alt="${expert.name}" class="expert-img">
                <span>${expert.name}</span>
            `;
            expertButton.onclick = () => selectExpert(index, correctAnswer, answers);
            expertsList.appendChild(expertButton);
        });
    }
}

// Handling when player chooses expert
function selectExpert(index, correctAnswer, allAnswers) {
    const selectedExpert = experts[index];

    // Call phone API to get suggestion
    fetch("https://tuanspace.uk/help/phone", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            correct_answer: correctAnswer,
            all_answers: allAnswers 
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display selected expert and answer from expert
        const expertContainer = document.getElementById("expert-response-container");
        const expertImage = document.getElementById("expert-image");
        const expertName = document.getElementById("expert-name");
        const expertSuggestion = document.getElementById("expert-suggestion");

        expertImage.src = selectedExpert.img;
        expertImage.alt = selectedExpert.name;
        expertName.textContent = `Chuyên gia: ${selectedExpert.name}`;
        expertSuggestion.textContent = `Gợi ý của chuyên gia: ${data.suggestion}`; // Display response from API

        expertContainer.style.display = "block"; // Show expert area
    })
    .catch(error => {
        console.error("Lỗi khi gọi API phone_a_friend:", error);
        alert("Không thể thực hiện trợ giúp.");
    });

    // Hide expert list after selection
    const phoneContainer = document.getElementById("phone-a-friend-container");
    if (phoneContainer) {
        phoneContainer.style.display = "none";
    }
}

// Show expert status
function showSimpleStatus(isCorrect, expertName, expertImage) {
    const statusContainer = document.getElementById("expert-status-container");
    const statusImage = document.getElementById("status-expert-image");
    const statusMessage = document.getElementById("status-expert-message");

    if (isCorrect) {
        // Message for the correct case
        statusImage.src = expertImage;
        statusMessage.textContent = `${expertName}: Tôi đã nói rồi mà! Tôi là một chuyên gia thực thụ!`;
    } else {
        // Message for wrong case
        statusImage.src = expertImage;
        statusMessage.textContent = `${expertName}: Rất tiếc, có vẻ bạn đã gọi lộn số...`;
    }

    statusContainer.style.display = "block"; // Show message

    // Hide message after 5 seconds
    setTimeout(() => {
        statusContainer.style.display = "none";
    }, 5000);
}

function resetExpertContainer() {
    const expertContainer = document.getElementById("expert-response-container");
    const expertImage = document.getElementById("expert-image");
    const expertName = document.getElementById("expert-name");
    const expertSuggestion = document.getElementById("expert-suggestion");

    if (expertContainer) {
        expertContainer.style.display = "none"; // Hide area and remove expert information
    }
    if (expertImage) {
        expertImage.src = "";
        expertImage.alt = "";
    }
    if (expertName) {
        expertName.textContent = "";
    }
    if (expertSuggestion) {
        expertSuggestion.textContent = "";
    }
}

let isFetching = false; // State variables to control consecutive function calls

// help audience
function handleAudiencePoll() {
    if (isFetching) {
        console.log("Đang xử lý, vui lòng đợi.");
        return;
    }
    isFetching = true; // Set processing status

    // console.log("Hàm handleAudiencePoll được gọi.");

    // Get the answer list from `remainingAnswers` if available, otherwise use the entire DOM
    const answers = remainingAnswers.length > 0 
        ? remainingAnswers 
        : Array.from(document.querySelectorAll(".answer-btn")).map(answer => answer.textContent);

    // console.log("Danh sách đáp án sử dụng:", answers);

    // Find the correct answer from DOM
    const correctAnswerElement = Array.from(document.querySelectorAll(".answer-btn")).find(answer =>
        answer.getAttribute("onclick").includes("true")
    );
    if (!correctAnswerElement) {
        console.error("Không tìm thấy đáp án đúng trong DOM.");
        isFetching = false;
        return; // Stop if not found
    }
    const correctAnswer = correctAnswerElement.textContent;

    // console.log("Đáp án đúng:", correctAnswer);

    // Send API request
    fetch("https://tuanspace.uk/help/audience", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ all_answers: answers, correct_answer: correctAnswer })
    })
    .then(response => response.json())
    .then(data => {
        // console.log("Phản hồi API:", data);

        if (!data.poll) {
            console.error("Phản hồi API không hợp lệ:", data);
            isFetching = false;
            return;
        }

        // Show container before drawing chart
        const audiencePollContainer = document.getElementById("audience-poll-container");
        if (!audiencePollContainer) {
            console.error("Không tìm thấy phần tử audience-poll-container.");
            isFetching = false;
            return;
        }
        audiencePollContainer.style.display = "block";

        // Make sure the canvas exists
        const canvas = document.getElementById("audience-poll-chart");
        const ctx = canvas.getContext("2d");
        if (window.myChart) window.myChart.destroy(); // Xóa biểu đồ cũ nếu có

        // Create new chart with API data
        window.myChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: answers,
                datasets: [{
                    label: "Tỷ lệ ý kiến khán giả (%)",
                    data: answers.map(answer => data.poll[answer] || 0),
                    backgroundColor: ["rgba(75, 192, 192, 0.2)", "rgba(255, 99, 132, 0.2)", "rgba(255, 206, 86, 0.2)", "rgba(54, 162, 235, 0.2)"],
                    borderColor: ["rgba(75, 192, 192, 1)", "rgba(255, 99, 132, 1)", "rgba(255, 206, 86, 1)", "rgba(54, 162, 235, 1)"],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true, max: 100 }
                }
            }
        });

        // console.log("Biểu đồ mới đã được vẽ thành công.");

        // Disable "Help Audience" button after use
        const hintAudienceButton = document.getElementById("hint-audience");
        if (hintAudienceButton) {
            hintAudienceButton.style.visibility = "hidden";
            hintAudienceButton.disabled = true;
        }

        isFetching = false; // Reset status
    })
    .catch(error => {
        console.error("Lỗi khi gọi API:", error);
        isFetching = false;
    });
}

function resetAudiencePoll() {
    // Get container and canvas
    const audiencePollContainer = document.getElementById("audience-poll-container");
    const canvas = document.getElementById("audience-poll-chart");

    // Hide container and remove chart if present
    if (audiencePollContainer) {
        audiencePollContainer.style.display = "none";
    }
    if (window.myChart) {
        window.myChart.destroy(); 
        window.myChart = null;
    }

    // console.log("Đã reset container và biểu đồ.");
}

let skipHintUsed = false; // Declare global variable

// switch question
function handleSwitchQuestion() {
    // Check if help has been used before
    if (skipHintUsed) {
        // console.log("Trợ giúp Đổi câu hỏi đã được sử dụng! Không thể sử dụng lại.");
        return; // Prevent players from reusing
    }

    // console.log("Đang đổi câu hỏi...");
    skipHintUsed = true; // Mark that help has been used

    // Disable the "Change Question" button
    const hintSkipButton = document.getElementById("hint-skip");
    if (hintSkipButton) {
        hintSkipButton.style.visibility = "hidden";
        hintSkipButton.disabled = true;
    }

    const currentQuestion = questions[currentQuestionIndex];
    if (!currentQuestion) {
        console.error("Không tìm thấy câu hỏi hiện tại.");
        return;
    }

    fetch("https://tuanspace.uk/help/switch_question", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            current_question_id: currentQuestion.id, 
            current_difficulty: currentQuestion.difficulty 
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error("Lỗi từ API:", data.error);
            alert("Không thể đổi câu hỏi: " + data.error);
            return;
        }

        // console.log("Câu hỏi mới từ API:", data.new_question);

        // Convert format before updating question list
        const formattedQuestion = {
            id: data.new_question.id,
            category: data.new_question.category || "Unknown", 
            difficulty: data.new_question.difficulty,
            question: data.new_question.question,
            correctAnswer: data.new_question.correct_answer, 
            incorrectAnswers: Object.values(data.new_question.answers).filter(ans => ans !== data.new_question.correct_answer) 
        };

        // Replace the current question in the list
        questions.splice(currentQuestionIndex, 1, formattedQuestion);

        // console.log("Danh sách câu hỏi sau khi cập nhật:", questions);

        // Show new questions
        displayQuestion();
    })
    .catch(error => {
        console.error("Lỗi khi gọi API:", error);
        alert("Không thể kết nối để đổi câu hỏi.");
    });
}