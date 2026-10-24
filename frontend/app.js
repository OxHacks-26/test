async function checkHealth() {
  const statusEl = document.getElementById("status");
  try {
    const response = await fetch("/api/health");
    const data = await response.json();
    statusEl.textContent = data.status;
  } catch {
    statusEl.textContent = "unreachable";
  }
}

checkHealth();
