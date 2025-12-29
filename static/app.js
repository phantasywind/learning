const startButton = document.getElementById("start-btn");
const resetButton = document.getElementById("reset-btn");
const submitButton = document.getElementById("submit-btn");
const guessInput = document.getElementById("guess-input");
const statusMessage = document.getElementById("status-message");
const attemptsText = document.getElementById("attempts");
const historyText = document.getElementById("history");

const updateUI = (data) => {
  statusMessage.textContent = data.message;
  attemptsText.textContent = `已猜次数：${data.attempts ?? 0}`;
  if (Array.isArray(data.history) && data.history.length > 0) {
    historyText.textContent = `历史记录：${data.history.join(", ")}`;
  } else {
    historyText.textContent = "历史记录：暂无";
  }

  const isActive = Boolean(data.active);
  guessInput.disabled = !isActive;
  submitButton.disabled = !isActive;
  if (!isActive) {
    guessInput.value = "";
  }
};

const handleResponse = async (response) => {
  const data = await response.json();
  updateUI(data);
};

const postJSON = async (url, payload = {}) => {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  await handleResponse(response);
};

startButton.addEventListener("click", () => {
  postJSON("/api/start");
});

resetButton.addEventListener("click", () => {
  postJSON("/api/reset");
});

submitButton.addEventListener("click", () => {
  postJSON("/api/guess", { guess: guessInput.value });
});

guessInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    submitButton.click();
  }
});

updateUI({ message: "点击“开始游戏”开始。", attempts: 0, history: [], active: false });
