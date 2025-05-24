//============================
//    APPLICATION INIT
//============================

// Глобальная переменная для токена
let token = null;

// Инициализация приложения после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
  // Можно добавить дополнительную инициализацию здесь
  console.log('Приложение загружено');
  
  // Проверяем, есть ли сохраненный токен (если нужно)
  // const savedToken = localStorage.getItem('token');
  // if (savedToken) {
  //   token = savedToken;
  //   showAppSection();
  // }
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