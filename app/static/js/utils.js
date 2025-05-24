// Утилиты
function renderPaginationButtons(containerId, currentPage, totalPages, onChangePage) {
    const cont = document.getElementById(containerId);
    cont.innerHTML = "";
    if (totalPages <= 1) return;
  
    const paginationDiv = document.createElement("div");
    paginationDiv.className = "btn-group";
  
    for (let p = 1; p <= totalPages; p++) {
      const btn = document.createElement("button");
      btn.className = "btn btn-outline-primary btn-sm";
      btn.textContent = p;
      if (p === currentPage) {
        btn.classList.add("active");
      }
      btn.onclick = () => onChangePage(p);
      paginationDiv.appendChild(btn);
    }
    cont.appendChild(paginationDiv);
  }
  
  function showMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    element.textContent = message;
    element.className = isError ? 'error mt-2' : 'mt-2';
  }
  
  function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
      const inputs = form.querySelectorAll('input, select, textarea');
      inputs.forEach(input => {
        if (input.type === 'checkbox' || input.type === 'radio') {
          input.checked = false;
        } else {
          input.value = '';
        }
      });
    }
  }
  
  // Загрузка HTML шаблонов
  async function loadTemplate(templatePath) {
    try {
      const response = await fetch(templatePath);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.text();
    } catch (error) {
      console.error('Error loading template:', error);
      return '';
    }
  }