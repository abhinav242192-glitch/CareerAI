const form = document.getElementById("chatForm");
const input = document.getElementById("message");
const chat = document.getElementById("chat");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;
  chat.innerHTML += `<div class="msg user">${escapeHtml(message)}</div>`;
  input.value = "";
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message})
  });
  const data = await res.json();
  chat.innerHTML += `<div class="msg bot">${escapeHtml(data.reply)}</div>`;
  chat.scrollTop = chat.scrollHeight;
});
function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
