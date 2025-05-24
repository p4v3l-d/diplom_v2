// Модуль для работы со студентами
class StudentsModule {
    constructor() {
      this.allStudents = [];
      this.currentPage = 1;
      this.pageSize = 20;
    }
  
    async loadAll() {
      try {
        const response = await API.students.getAll();
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.allStudents = await response.json();
        this.currentPage = 1;
        this.render();
      } catch (error) {
        alert("Ошибка при получении списка студентов: " + error.message);
      }
    }
  
    render() {
      const container = document.getElementById("studentList");
      container.innerHTML = "";
      
      if (!this.allStudents.length) {
        container.textContent = "Нет студентов.";
        return;
      }
  
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      const pageItems = this.allStudents.slice(startIndex, endIndex);
  
      const table = document.createElement("table");
      table.className = "table table-sm table-striped";
      
      const thead = document.createElement("thead");
      thead.innerHTML = "<tr><th>ID</th><th>ФИО</th><th>Группа</th><th>Специальность</th></tr>";
      table.appendChild(thead);
  
      const tbody = document.createElement("tbody");
      pageItems.forEach(student => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${student.id}</td>
          <td>${student.full_name || ""}</td>
          <td>${student.group || ""}</td>
          <td>${student.specialty || ""}</td>
        `;
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      container.appendChild(table);
  
      const totalPages = Math.ceil(this.allStudents.length / this.pageSize);
      renderPaginationButtons("studentPagination", this.currentPage, totalPages, (newPage) => {
        this.currentPage = newPage;
        this.render();
      });
    }
  
    async create() {
      const formData = {
        full_name: document.getElementById("newStudentName").value,
        group: document.getElementById("newStudentGroup").value || null,
        specialty: document.getElementById("newStudentSpecialty").value || null,
        birth_date: document.getElementById("newStudentBirth").value || null,
        passport_number: document.getElementById("newStudentPassport").value || null,
        contacts: document.getElementById("newStudentContacts").value || null
      };
  
      try {
        const response = await API.students.create(formData);
        if (response.ok) {
          showMessage("createStudentMsg", "Студент создан!");
          this.loadAll();
          this.clearCreateForm();
        } else {
          const error = await response.json();
          showMessage("createStudentMsg", "Ошибка: " + (error.detail || response.status), true);
        }
      } catch (error) {
        showMessage("createStudentMsg", "Ошибка: " + error.message, true);
      }
    }
  
    async search() {
      const searchParams = {};
      const fullName = document.getElementById("searchFullName").value;
      const group = document.getElementById("searchGroup").value;
      const specialty = document.getElementById("searchSpecialty").value;
  
      if (fullName) searchParams.full_name = fullName;
      if (group) searchParams.group = group;
      if (specialty) searchParams.specialty = specialty;
  
      try {
        const response = await API.students.search(searchParams);
        if (response.ok) {
          const results = await response.json();
          this.renderSearchResults(results);
        } else {
          alert("Ошибка при поиске студентов: " + response.status);
        }
      } catch (error) {
        alert("Ошибка при поиске студентов: " + error.message);
      }
    }
  
    renderSearchResults(students) {
      const container = document.getElementById("searchResults");
      container.innerHTML = "";
      
      if (!students.length) {
        container.textContent = "Поиск не дал результатов.";
        return;
      }
  
      const table = document.createElement("table");
      table.className = "table table-sm table-striped";
      
      const thead = document.createElement("thead");
      thead.innerHTML = "<tr><th>ID</th><th>ФИО</th><th>Группа</th><th>Специальность</th></tr>";
      table.appendChild(thead);
  
      const tbody = document.createElement("tbody");
      students.forEach(student => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${student.id}</td>
          <td>${student.full_name || ""}</td>
          <td>${student.group || ""}</td>
          <td>${student.specialty || ""}</td>
        `;
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      container.appendChild(table);
    }
  
    clearCreateForm() {
      document.getElementById("newStudentName").value = "";
      document.getElementById("newStudentGroup").value = "";
      document.getElementById("newStudentSpecialty").value = "";
      document.getElementById("newStudentBirth").value = "";
      document.getElementById("newStudentPassport").value = "";
      document.getElementById("newStudentContacts").value = "";
    }
  }
  
  // Создаем экземпляр модуля
  const studentsModule = new StudentsModule();
  
  // Глобальные функции для обратной совместимости
  function getStudents() {
    studentsModule.loadAll();
  }
  
  function createStudent() {
    studentsModule.create();
  }
  
  function searchStudents() {
    studentsModule.search();
  }