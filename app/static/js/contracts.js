// Модуль для работы с контрактами
class ContractsModule {
    constructor() {
      this.allContracts = [];
      this.currentPage = 1;
      this.pageSize = 20;
    }
  
    async loadAll() {
      try {
        const response = await API.contracts.getAll();
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.allContracts = await response.json();
        this.currentPage = 1;
        this.render();
      } catch (error) {
        alert("Ошибка при получении контрактов: " + error.message);
      }
    }
  
    render() {
      const container = document.getElementById("contractList");
      container.innerHTML = "";
  
      if (!this.allContracts.length) {
        container.textContent = "Нет контрактов.";
        return;
      }
  
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      const pageItems = this.allContracts.slice(startIndex, endIndex);
  
      const table = document.createElement("table");
      table.className = "table table-sm table-bordered";
      
      const thead = document.createElement("thead");
      thead.innerHTML = `
        <tr>
          <th>ID</th><th>Номер</th><th>ID Студента</th><th>Сумма</th>
          <th>Скидка</th><th>Дата</th><th>Действует до</th><th>График</th>
        </tr>
      `;
      table.appendChild(thead);
  
      const tbody = document.createElement("tbody");
      pageItems.forEach(contract => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${contract.id}</td>
          <td>${contract.contract_number}</td>
          <td>${contract.student_id}</td>
          <td>${contract.total_amount}</td>
          <td>${contract.discount || 0}</td>
          <td>${contract.date_signed}</td>
          <td>${contract.valid_until || ""}</td>
          <td>${contract.payment_schedule || ""}</td>
        `;
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      container.appendChild(table);
  
      const totalPages = Math.ceil(this.allContracts.length / this.pageSize);
      renderPaginationButtons("contractPagination", this.currentPage, totalPages, (newPage) => {
        this.currentPage = newPage;
        this.render();
      });
    }
  
    async create() {
      const formData = {
        student_id: parseInt(document.getElementById("newContractStudentId").value),
        contract_number: document.getElementById("newContractNumber").value,
        date_signed: document.getElementById("newContractDateSigned").value || null,
        total_amount: parseFloat(document.getElementById("newContractTotalAmount").value),
        discount: parseFloat(document.getElementById("newContractDiscount").value) || 0,
        valid_until: document.getElementById("newContractValidUntil").value || null,
        payment_schedule: document.getElementById("newContractSchedule").value || "помесячно"
      };
  
      try {
        const response = await API.contracts.create(formData);
        if (response.ok) {
          showMessage("createContractMsg", "Контракт создан!");
          this.loadAll();
          this.clearCreateForm();
        } else {
          const error = await response.json();
          showMessage("createContractMsg", "Ошибка: " + (error.detail || response.status), true);
        }
      } catch (error) {
        showMessage("createContractMsg", "Ошибка: " + error.message, true);
      }
    }
  
    clearCreateForm() {
      document.getElementById("newContractStudentId").value = "";
      document.getElementById("newContractNumber").value = "";
      document.getElementById("newContractDateSigned").value = "";
      document.getElementById("newContractTotalAmount").value = "";
      document.getElementById("newContractDiscount").value = "";
      document.getElementById("newContractValidUntil").value = "";
      document.getElementById("newContractSchedule").value = "";
    }
  }
  
  // Создаем экземпляр модуля
  const contractsModule = new ContractsModule();
  
  // Глобальные функции для обратной совместимости
  function getContracts() {
    contractsModule.loadAll();
  }
  
  function createContract() {
    contractsModule.create();
  }