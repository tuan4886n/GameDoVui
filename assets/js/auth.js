// New User Registration
function registerUser() {
    const username = document.getElementById("register-username").value.trim();
    const password = document.getElementById("register-password").value.trim();

    if (!username || !password) {
        showNotification("Vui lòng nhập đầy đủ username và mật khẩu.", false);
        return;
    }

    fetch("https://gamedovui-production.up.railway.app/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status.includes("✅")) {
            showNotification("Đăng ký thành công!");
        } else {
            showNotification(data.status || "Có lỗi xảy ra. Vui lòng thử lại.", false);
        }
    })
    .catch(error => {
        console.error("Error registering user:", error);
        showNotification("Không thể đăng ký. Vui lòng thử lại.", false);
    });
}

// User Login
function loginUser() {
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value.trim();

    if (!username || !password) {
        showNotification("Vui lòng nhập đầy đủ username và mật khẩu.", false);
        return;
    }

    fetch("https://gamedovui-production.up.railway.app/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status.includes("✅")) {
            localStorage.setItem("currentUsername", username);
            showNotification("Đăng nhập thành công!");
            window.location.href = "/index.html";
        } else {
            showNotification(data.status || "Tên người dùng hoặc mật khẩu không đúng.", false);
        }
    })
    .catch(error => {
        console.error("Error logging in user:", error);
        showNotification("Không thể đăng nhập. Vui lòng thử lại.", false);
    });
}

function showNotification(message, isSuccess = true) {
    const notification = document.getElementById("notification");

    if (!notification) {
        console.error("Không tìm thấy phần tử thông báo.");
        return;
    }

    // Set notification content and color
    notification.textContent = message;
    notification.style.backgroundColor = isSuccess ? "#4CAF50" : "#f44336"; // Green for success, red for error
    notification.style.display = "block";

    // Appearance effect
    notification.style.opacity = "0";
    notification.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    notification.style.transform = "translateX(-50%) translateY(-20px)";
    setTimeout(() => {
        notification.style.opacity = "1";
        notification.style.transform = "translateX(-50%) translateY(0)";
    }, 10);

    // Automatically hide notifications after 3 seconds
    setTimeout(() => {
        notification.style.opacity = "0";
        notification.style.transform = "translateX(-50%) translateY(-20px)";
        setTimeout(() => {
            notification.style.display = "none";
        }, 500); // Delay time for fade effect to complete
    }, 3000);
}