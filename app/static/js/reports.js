//============================
//        REPORTS
//============================

async function getPaymentsByDateRange() {
    const startDate = document.getElementById("reportStartDate").value;
    const endDate = document.getElementById("reportEndDate").value;
    let url = "/reports/payments-range";
    const params = [];
    if (startDate) params.push(`start_date=${startDate}`);
    if (endDate) params.push(`end_date=${endDate}`);
    if (params.length > 0) {
      url += "?" + params.join("&");
    }
    const resp = await fetch(url, { headers: { "Authorization": `Bearer ${token}` } });
    if (resp.ok) {
      const payments = await resp.json();
      renderPayments(payments, "paymentsRangeList");
    } else {
      alert("Ошибка: " + resp.status);
    }
  }
  
  async function getPaymentsByDateRangeSummary() {
    const startDate = document.getElementById("reportStartDate").value;
    const endDate = document.getElementById("reportEndDate").value;
    let url = "/reports/payments-range/summary";
    const params = [];
    if (startDate) params.push(`start_date=${startDate}`);
    if (endDate) params.push(`end_date=${endDate}`);
    if (params.length > 0) {
      url += "?" + params.join("&");
    }
    const resp = await fetch(url, { headers: { "Authorization": `Bearer ${token}` }});
    if (resp.ok) {
      const data = await resp.json();
      document.getElementById("paymentsRangeSummary").innerHTML = `
        <div class="alert alert-info">
          Итого за период: ${data.total_payments_sum} руб.
        </div>
      `;
    } else {
      alert("Ошибка: " + resp.status);
    }
  }
  
  async function getPaymentsReport() {
    const now = new Date();
    const endDate = now.toISOString().slice(0, 10);
    const startDateObj = new Date(now.getTime() - 30 * 24*3600*1000);
    const startDate = startDateObj.toISOString().slice(0, 10);
  
    const url = `/reports/payments?start_date=${startDate}&end_date=${endDate}`;
    const resp = await fetch(url, { headers: { "Authorization": `Bearer ${token}` }});
    if (resp.ok) {
      const data = await resp.json();
      renderPayments(data, "paymentsReport");
    } else {
      alert("Ошибка: " + resp.status);
    }
  }
  
  async function getDebtors() {
    const resp = await fetch("/reports/debtors", {
      headers: {"Authorization": `Bearer ${token}`}
    });
    if (resp.ok) {
      const data = await resp.json();
      renderDebtors(data);
    } else {
      alert("Ошибка при получении должников: " + resp.status);
    }
  }
  
  function renderDebtors(debtors) {
    const c = document.getElementById("debtorsList");
    c.innerHTML = "";
    if (!debtors.length) {
      c.textContent = "Нет должников.";
      return;
    }
    const table = document.createElement("table");
    table.className = "table table-striped";
    let thead = document.createElement("thead");
    thead.innerHTML = "<tr><th>ID студента</th><th>ФИО</th><th>Долг</th></tr>";
    table.appendChild(thead);
    let tbody = document.createElement("tbody");
    debtors.forEach(d => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${d.student_id}</td>
        <td>${d.full_name}</td>
        <td class="text-danger">${d.debt}</td>
      `;
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    c.appendChild(table);
  }
  
  async function getSummary() {
    const resp = await fetch("/reports/summary", {
      headers: {"Authorization": `Bearer ${token}`}
    });
    if (resp.ok) {
      const data = await resp.json();
      document.getElementById("summaryInfo").innerHTML = `
        <div class="alert alert-success">
          Всего платежей: ${data.total_payments}<br/>
          Сумма: ${data.total_paid_sum}
        </div>
      `;
    } else {
      alert("Ошибка сводного отчёта " + resp.status);
    }
  }