// Save question list and current status
let questions = []; // List of questions
let currentQuestionIndex = 0; // Current question index

// Restart the game
function startGame() {
    const currentUsername = localStorage.getItem("currentUsername");

    console.log("Đang khởi động trò chơi cho người dùng:", currentUsername);

    if (!currentUsername || currentUsername === "null") {
        alert("Không xác định được username. Vui lòng đăng nhập lại.");
        window.location.href = "register_login.html"; // Navigate to the login page
        return;
    }

    // Hide Game Over interface if displayed
    const gameOverElement = document.getElementById("game-over");
    if (gameOverElement) {
        gameOverElement.style.display = "none";
    }

    // Reset game state
    currentQuestionIndex = 0; // Reset question order
    questions = []; // Clear question list (if new download is needed)
    document.getElementById("current_score").innerText = "Điểm hiện tại: 0"; // Reset current point
    document.getElementById("highest_score").innerText = "Điểm cao nhất: 0"; // Reset highest score

    // Reset help button state
    resetHints();
    resetExpertContainer();
    resetAudiencePoll();

    // Reset the number of displayed questions (if question display is integrated)
    const questionCounterElement = document.getElementById("current-question-number");
    if (questionCounterElement) {
        questionCounterElement.textContent = currentQuestionIndex + 1; // Reset to first sentence
    }

    // Show loading status
    const gameAreaElement = document.getElementById("game-area");
    if (!gameAreaElement) {
        console.error("Không tìm thấy phần tử #game-area!");
        alert("Lỗi hệ thống: Không thể khởi tạo giao diện trò chơi.");
        return;
    }
    gameAreaElement.innerHTML = "<p>Đang tải câu hỏi...</p>";

    // Call API to start game
    fetch("http://13.228.79.3:8080/start_game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: currentUsername })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Phản hồi từ API:", data);

        if (!data || typeof data.total_sessions === "undefined" || typeof data.current_game_score === "undefined") {
            console.error("Phản hồi không hợp lệ từ API:", data);
            alert("Lỗi khi bắt đầu trò chơi.");
            return;
        }

        // Update play and score information from API
        document.getElementById("total_sessions").innerText = "Lần chơi: " + data.total_sessions;
        document.getElementById("current_score").innerText = "Điểm hiện tại: " + data.current_game_score;

        // Download game questions
        loadQuiz();
    })
    .catch(error => {
        console.error("Lỗi khi gọi API /start_game:", error);
        alert("Không thể bắt đầu trò chơi. Vui lòng thử lại.");
    });
}

// Load question list from API
function loadQuiz() {
    console.log("Đang tải câu hỏi...");
    fetch("http://13.228.79.3:8080/quiz")
    .then(response => response.json())
    .then(data => {
        console.log("Danh sách câu hỏi nhận được:", data.quiz);

        if (!data.quiz || !Array.isArray(data.quiz) || data.quiz.length === 0) {
            document.getElementById("game-area").innerHTML = "<p>Không có câu hỏi nào được tải.</p>";
            return;
        }

        questions = data.quiz;
        currentQuestionIndex = 0; // Reset first question index
        displayQuestion();
    })
    .catch(error => {
        console.error("Lỗi khi tải câu hỏi:", error);
        document.getElementById("game-area").innerHTML = "<p>Không thể tải câu hỏi. Vui lòng thử lại.</p>";
    });
}

// Show current questions in order
function displayQuestion() {
    // Reset remainingAnswers to prepare for new questions
    remainingAnswers = [];
    console.log("remainingAnswers đã được reset:", remainingAnswers);

    // Check if all questions are completed
    if (currentQuestionIndex >= questions.length) {
        const gameAreaElement = document.getElementById("game-area");
        if (!gameAreaElement) {
            console.error("Không tìm thấy phần tử #game-area.");
            return;
        }
        gameAreaElement.innerHTML = "<p>Đã hoàn thành tất cả câu hỏi!</p>";
        return;
    }

    // Reset audience and expert containers before displaying new questions
    resetAudiencePoll();
    resetExpertContainer();

    // Update current question number
    const questionCounterElement = document.getElementById("current-question-number");
    if (questionCounterElement) {
        questionCounterElement.textContent = currentQuestionIndex + 1; // Show number of questions
    }

    // Get the current question from the question list
    const question = questions[currentQuestionIndex];
    if (!question || !question.correctAnswer || !Array.isArray(question.incorrectAnswers)) {
        console.error("Định dạng câu hỏi không hợp lệ:", question);
        const gameAreaElement = document.getElementById("game-area");
        if (gameAreaElement) {
            gameAreaElement.innerHTML = "<p>Lỗi khi hiển thị câu hỏi. Vui lòng thử lại.</p>";
        }
        return;
    }

    // Collect all answers (right and wrong)
    const allAnswers = [...question.incorrectAnswers.map(answer => ({
        text: answer,
        isCorrect: false
    })), {
        text: question.correctAnswer,
        isCorrect: true
    }];

    // Fisher-Yates Shuffle
    for (let i = allAnswers.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [allAnswers[i], allAnswers[j]] = [allAnswers[j], allAnswers[i]];
    }

    // Create HTML interface to display questions and answers
    const gameAreaElement = document.getElementById("game-area");
    if (!gameAreaElement) {
        console.error("Không tìm thấy phần tử #game-area.");
        return;
    }

    // Display question and create answer button
    let questionHTML = `
        <p id="question-text">${question.question}</p>
        <div id="answers-area" class="answers-container">
            ${allAnswers.map(answer =>
                `<button class="answer-btn" onclick="submitAnswer('${question.id}', ${answer.isCorrect})">${answer.text}</button>`
            ).join("")}
        </div>
    `;
    gameAreaElement.innerHTML = questionHTML;
}

// Submit response and further processing
function submitAnswer(questionId, isCorrect) {
    const currentUsername = localStorage.getItem("currentUsername");

    console.log("Gửi câu trả lời cho câu hỏi:", questionId, "Đúng:", isCorrect);

    // Check username
    if (!currentUsername || currentUsername === "null") {
        alert("Không xác định được username. Vui lòng đăng nhập lại.");
        window.location.href = "register_login.html"; // Chuyển về giao diện đăng nhập
        return;
    }

    // Check Question ID
    if (!questionId) {
        console.error("Lỗi: Thiếu ID câu hỏi.");
        alert("Lỗi khi gửi câu trả lời. Vui lòng thử lại.");
        return;
    }

    const difficulty = "medium"; // Difficulty (temporarily fixed)

    fetch("http://13.228.79.3:8080/submit_score", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: currentUsername,
            question_id: questionId,
            correct: isCorrect,
            difficulty: difficulty
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Phản hồi từ API /submit_score:", data);

        if (!data || typeof data.current_game_score === "undefined" || typeof data.highest_score === "undefined") {
            console.error("Dữ liệu không hợp lệ từ API /submit_score:", data);
            alert("Có lỗi xảy ra khi cập nhật điểm. Vui lòng thử lại.");
            return;
        }

        // Update point interface
        document.getElementById("current_score").innerText = "Điểm hiện tại: " + data.current_game_score;
        document.getElementById("highest_score").innerText = "Điểm cao nhất: " + data.highest_score;

        // Check expert status if hint has been used
        if (expertHint) {
            const expertName = document.getElementById("expert-name").textContent || "Chuyên gia";
            const expertImage = document.getElementById("expert-image").src;

            // Call the function that displays the expert status from help_question.js
            showSimpleStatus(isCorrect, expertName, expertImage);
        }

        // Reset expert suggestion status
        expertHint = false;

        // If the answer is wrong, display Game Over and exit.
        if (!isCorrect) {
            setTimeout(() => {
                showGameOverScreen(data.current_game_score); // Show Game Over interface
            }, 1000);
            return;
        }

        // Show next question
        currentQuestionIndex++;
        displayQuestion();
    })
    .catch(error => {
        console.error("Lỗi khi gửi câu trả lời:", error);
        alert("Không thể gửi câu trả lời. Vui lòng thử lại.");
    });
}

// Show Game Over interface
function showGameOverScreen(score, difficulty, correct) {
    const gameOverElement = document.getElementById("game-over");
    const gameOverMessageElement = document.getElementById("game-over-message");

    if (!gameOverElement || !gameOverMessageElement) {
        console.error("Không tìm thấy phần tử giao diện Game Over. Kiểm tra HTML.");
        return;
    }

    // Update Game Over notification
    gameOverMessageElement.innerText = `Game Over! Bạn đã đạt được ${score} điểm.`;

    // Submit new score to server via submit_score API
    const username = localStorage.getItem("currentUsername");
    fetch("http://13.228.79.3:8080/submit_score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, difficulty: difficulty, correct: correct })
    })
    .then(response => {
        if (!response.ok) throw new Error("Không thể gửi điểm lên server.");
        return response.json();
    })
    .then(data => {
        console.log("Điểm số đã được gửi thành công:", data);

        // Refresh the leaderboard immediately after the score is updated
        fetchLeaderboard();
    })
    .catch(error => {
        console.error("Lỗi khi gửi điểm số:", error);
    });

    // Show Game Over interface
    gameOverElement.style.display = "flex";
}

// Download leaderboard data
function fetchLeaderboard(page = 1) {
    console.log(`Đang tải bảng xếp hạng cho trang ${page}...`);

    fetch(`http://13.228.79.3:8080/leaderboard?page=${page}`)
    .then(response => {
        if (!response.ok) throw new Error("Không thể tải bảng xếp hạng từ server.");
        return response.json();
    })
    .then(data => {
        console.log("Dữ liệu bảng xếp hạng nhận được:", data);

        const leaderboardList = document.getElementById("leaderboard-list");
        if (!leaderboardList) {
            console.error("Không tìm thấy phần tử để hiển thị bảng xếp hạng.");
            return;
        }

        // Delete old data before rendering
        leaderboardList.innerHTML = "";

        if (data && Array.isArray(data.leaderboard) && data.leaderboard.length > 0) {
            data.leaderboard.forEach((player, index) => {
                const listItem = document.createElement("li");
                listItem.textContent = `${(page - 1) * 10 + index + 1}. ${player.username}: ${player.highest_score} điểm`;
                leaderboardList.appendChild(listItem);
            });
        } else {
            leaderboardList.innerHTML = "<p>Không có dữ liệu xếp hạng.</p>";
        }
    })
    .catch(error => {
        console.error("Lỗi khi tải bảng xếp hạng:", error);
        const leaderboardList = document.getElementById("leaderboard-list");
        if (leaderboardList) {
            leaderboardList.innerHTML = "<p>Không thể tải bảng xếp hạng. Vui lòng thử lại.</p>";
        }
    });
}

// Call to automatically load the leaderboard when the page is loaded
document.addEventListener("DOMContentLoaded", function () {
    fetchLeaderboard();
});

// Function to reset all help buttons (return to original state)
function resetHints() {
    // Reset remainingAnswers
    remainingAnswers = [];

    // Reset help button 50/50
    const hint50Button = document.getElementById("hint-50-50");
    if (hint50Button) {
        hint50Button.style.visibility = "visible";
        hint50Button.disabled = false;
    }

    // Reset "Call Expert" help button
    const hintPhoneButton = document.getElementById("hint-phone");
    if (hintPhoneButton) {
        hintPhoneButton.style.visibility = "visible";
        hintPhoneButton.disabled = false;
    }

    // Reset "Ask the audience" help button
    const hintAudienceButton = document.getElementById("hint-audience");
    if (hintAudienceButton) {
        hintAudienceButton.style.visibility = "visible";
        hintAudienceButton.disabled = false;
    }

    // Reset the "Change question" help button
    const hintSkipButton = document.getElementById("hint-skip");
    if (hintSkipButton) {
        hintSkipButton.style.visibility = "visible";
        hintSkipButton.disabled = false;
    }
}