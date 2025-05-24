// Модуль аутентификации
let token = null;

async function login() {
  const uname = document.getElementById("username").value;
  const pw = document.getElementById("password").value;
  const body = new URLSearchParams({ username: uname, password: pw });

  const response = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: body
  });

  if (response.ok) {
    const data = await response.json();
    token = data.access_token;
    document.getElementById("loginMessage").textContent = "Успешный вход!";
    document.getElementById("appSection").style.display = "";
    document.getElementById("loginSection").style.display = "none";
    
    // Загружаем компоненты приложения после успешного входа
    await loadAppComponents();
  } else {
    document.getElementById("loginMessage").textContent = "Ошибка авторизации!";
  }
}

function logout() {
  token = null;
  document.getElementById("loginMessage").textContent = "";
  document.getElementById("appSection").style.display = "none";
  document.getElementById("loginSection").style.display = "";
  
  // Очищаем компоненты приложения
  document.getElementById("mainAccordion").innerHTML = "";
}

// Экспортируем функцию для получения токена
function getToken() {
  return token;
}