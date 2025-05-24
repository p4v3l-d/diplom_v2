// API модуль для работы с сервером
class ApiClient {
    static async request(url, options = {}) {
      const token = getToken();
      const defaultOptions = {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          ...options.headers
        }
      };
  
      const finalOptions = { ...defaultOptions, ...options };
      
      try {
        const response = await fetch(url, finalOptions);
        return response;
      } catch (error) {
        console.error('API request failed:', error);
        throw error;
      }
    }
  
    static async get(url) {
      return this.request(url, { method: 'GET' });
    }
  
    static async post(url, data) {
      return this.request(url, {
        method: 'POST',
        body: JSON.stringify(data)
      });
    }
  
    static async patch(url, data) {
      return this.request(url, {
        method: 'PATCH',
        body: JSON.stringify(data)
      });
    }
  
    static async delete(url) {
      return this.request(url, { method: 'DELETE' });
    }
  }
  
  // Специфичные API функции
  const API = {
    // Студенты
    students: {
      getAll: () => ApiClient.get('/students/'),
      create: (data) => ApiClient.post('/students/', data),
      search: (params) => {
        const searchParams = new URLSearchParams(params);
        return ApiClient.get(`/students/search?${searchParams}`);
      }
    },
  
    // Контракты
    contracts: {
      getAll: () => ApiClient.get('/contracts/'),
      create: (data) => ApiClient.post('/contracts/', data)
    },
  
    // Платежи
    payments: {
      getAll: () => ApiClient.get('/payments/'),
      create: (data) => ApiClient.post('/payments/', data),
      updateStatus: (id, status) => ApiClient.patch(`/payments/${id}`, { status }),
      getReceipt: (id) => ApiClient.get(`/payments/${id}/receipt`)
    },
  
    // Отчёты
    reports: {
      getPaymentsByRange: (startDate, endDate) => {
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        return ApiClient.get(`/reports/payments-range?${params}`);
      },
      getPaymentsSummary: (startDate, endDate) => {
        const params = new URLSearchParams();
        if (startDate) params.append('start_date', startDate);
        if (endDate) params.append('end_date', endDate);
        return ApiClient.get(`/reports/payments-range/summary?${params}`);
      },
      getPaymentsReport: (startDate, endDate) => {
        return ApiClient.get(`/reports/payments?start_date=${startDate}&end_date=${endDate}`);
      },
      getDebtors: () => ApiClient.get('/reports/debtors'),
      getSummary: () => ApiClient.get('/reports/summary')
    }
  };