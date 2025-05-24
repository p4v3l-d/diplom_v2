// Модуль для работы с платежами
class PaymentsModule {
    constructor() {
      this.allPayments = [];
    }
  
    async loadAll() {
      try {
        const response = await API.payments.getAll();
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.allPayments = await response.json();
        this.render(this.allPayments, "paymentList");
      } catch (error) {
        alert("Ошибка при получении платежей: " + error.message);
      }
    }
  
    async create() {
      const formData = {
        contract_id: parseInt(document.getElementById("newPaymentContractId").value),
        amount: parseFloat(document.getElementById("newPaymentAmount").value),
        payment_date: document.getElementById("newPaymentDate").value,
        payment_method: document.getElementById("newPaymentMethod").value,
        status: document.getElementById("newPaymentStatus").value
      };
  
      try {
        const response = await API.payments.create(formData);
        if (response.ok) {
          showMessage("createPaymentMsg", "Платёж создан!");
          this.loadAll();
          this.clearCreateForm();
        } else {
          const error = await response.json();
          showMessage("createPaymentMsg", "Ошибка: " + (error.detail || response.status), true);
        }
      } catch (error) {
        showMessage("createPaymentMsg", "Ошибка: " + error.message, true);
      }
    }
  
    render(payments, containerId) {
      const container = document.getElementById(containerId);
      container.innerHTML = "";
  
      if (!payments.length) {
        container.textContent = "Нет платежей.";
        return;
      }
  
      const table = document.createElement("table");
      table.className = "table table-sm table-bordered";
      
      const thead = document.createElement("thead");
      thead.innerHTML = `
        <tr>
          <th>ID</th><th>ID Контракта</th><th>Сумма</th><th>Дата</th>
          <th>Способ</th><th>Статус</th><th></th><th></th>
        </tr>
      `;
      table.appendChild(thead);
  
      const tbody = document.createElement("tbody");
      payments.forEach(payment => {
        const tr = document.createElement("tr");
  
        const receiptButton = `<button class="btn btn-sm btn-outline-info" onclick="getReceipt(${payment.id})">Квитанция</button>`;
  
        let changeStatusButton = "";
        if (payment.status === "unpaid") {
          changeStatusButton = `<button class="btn btn-sm btn-warning" onclick="markPaymentPaid(${payment.id})">Оплатить</button>`;
        } else if (payment.status === "paid") {
          changeStatusButton = `<button class="btn btn-sm btn-secondary" onclick="markPaymentUnpaid(${payment.id})">Отменить оплату</button>`;
        }
  
        tr.innerHTML = `
          <td>${payment.id}</td>
          <td>${payment.contract_id}</td>
          <td>${payment.amount}</td>
          <td>${payment.payment_date}</td>
          <td>${payment.payment_method || ""}</td>
          <td>${payment.status || ""}</td>
          <td>${receiptButton}</td>
          <td>${changeStatusButton}</td>
        `;
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      container.appendChild(table);
    }
  
    async updateStatus(paymentId, status) {
      try {
        const response = await API.payments.updateStatus(paymentId, status);
        if (response.ok) {
          alert(`Статус изменён на '${status}'`);
          this.loadAll();
        } else {
          const error = await response.json();
          alert("Ошибка: " + (error.detail || response.status));
        }
      } catch (error) {
        alert("Ошибка: " + error.message);
      }
    }
  
    async getReceipt(paymentId) {
      try {
        const response = await API.payments.getReceipt(paymentId);
        if (response.ok) {
          const data = await response.json();
          alert(data.receipt);
        } else {
          alert("Ошибка получения квитанции: " + response.status);
        }
      } catch (error) {
        alert("Ошибка получения квитанции: " + error.message);
      }
    }
  
    clearCreateForm() {
      document.getElementById("newPaymentContractId").value = "";
      document.getElementById("newPaymentAmount").value = "";
      document.getElementById("newPaymentDate").value = "";
      document.getElementById("newPaymentMethod").value = "";
      document.getElementById("newPaymentStatus").value = "unpaid";
    }
  }
  
  // Создаем экземпляр модуля
  const paymentsModule = new PaymentsModule();
  
  // Глобальные функции для обратной совместимости
  function getPayments() {
    paymentsModule.loadAll();
  }
  
  function createPayment() {
    paymentsModule.create();
  }
  
  function markPaymentPaid(paymentId) {
    paymentsModule.updateStatus(paymentId, "paid");
  }
  
  function markPaymentUnpaid(paymentId) {
    paymentsModule.updateStatus(paymentId, "unpaid");
  }
  
  function getReceipt(paymentId) {
    paymentsModule.getReceipt(paymentId);
  }