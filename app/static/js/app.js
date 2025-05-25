let token = null;

document.addEventListener('DOMContentLoaded', function() {
  console.log('Приложение загружено');
});

// Вспомогательная функция для показа основного раздела приложения
function showAppSection() {
  document.getElementById("appSection").style.display = "";
  document.getElementById("loginSection").style.display = "none";
}

// Вспомогательная функция для показа раздела логина
function showLoginSection() {
  document.getElementById("appSection").style.display = "none";
  document.getElementById("loginSection").style.display = "";
}