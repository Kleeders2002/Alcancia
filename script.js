document.addEventListener('DOMContentLoaded', () => {
  const goal = 1200;
  const deadline = new Date(2026, 11, 31); // 31 dic 2026
  const API_URL = 'http://localhost:8000'; // Cambiar al deploy en producción

  // Elementos DOM
  const totalSpan = document.getElementById('totalSaved');
  const remainingSpan = document.getElementById('remaining');
  const progressPercentSpan = document.getElementById('progressPercent');
  const progressBar = document.getElementById('progressBar');
  const piggyFill = document.getElementById('piggyFill');
  const logContainer = document.getElementById('logContainer');
  const daysLeftP = document.getElementById('daysLeft');
  const depositBtn = document.getElementById('depositBtn');
  const personSelect = document.getElementById('personSelect');
  const amountInput = document.getElementById('amountInput');
  const formMessage = document.getElementById('formMessage');

  // Calcular días restantes
  function updateDaysLeft() {
    const today = new Date();
    const diffTime = deadline - today;
    const days = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    daysLeftP.textContent = `⏳ ${days > 0 ? days : 0} días para la meta`;
  }
  updateDaysLeft();

  // Cargar datos desde el servidor FastAPI
  async function fetchDeposits() {
    try {
      const response = await fetch(`${API_URL}/api/deposits`);
      if (!response.ok) throw new Error('Error al obtener datos');
      const deposits = await response.json();
      updateUI(deposits);
    } catch (error) {
      console.error(error);
      formMessage.textContent = 'No se pudo cargar el historial.';
    }
  }

  // Actualizar interfaz con lista de depósitos
  function updateUI(deposits) {
    // Calcular total
    const total = deposits.reduce((sum, d) => sum + parseFloat(d.amount), 0);
    const remaining = Math.max(goal - total, 0);
    const percent = Math.min((total / goal) * 100, 100);

    totalSpan.textContent = `$${total.toFixed(2)}`;
    remainingSpan.textContent = `$${remaining.toFixed(2)}`;
    progressPercentSpan.textContent = `${percent.toFixed(1)}%`;
    progressBar.style.width = `${percent}%`;
    piggyFill.style.height = `${percent}%`;

    // Renderizar log
    if (deposits.length === 0) {
      logContainer.innerHTML = '<p class="empty-log">✨ Aún no hay depósitos. ¡Empiecen a ahorrar!</p>';
      return;
    }

    // Ordenar por fecha descendente (más reciente primero)
    const sorted = [...deposits].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    let html = '';
    sorted.forEach(dep => {
      const date = new Date(dep.timestamp);
      const formattedDate = `${date.toLocaleDateString('es-ES')} ${date.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}`;
      html += `
        <div class="log-entry">
          <span class="person"><i class="fas fa-user-circle"></i> ${dep.person}</span>
          <span class="amount">$${parseFloat(dep.amount).toFixed(2)}</span>
          <span class="date">${formattedDate}</span>
        </div>
      `;
    });
    logContainer.innerHTML = html;
  }

  // Enviar nuevo depósito al servidor FastAPI
  async function addDeposit(person, amount) {
    const formData = new FormData();
    formData.append('person', person);
    formData.append('amount', amount);

    try {
      const response = await fetch(`${API_URL}/api/deposits`, {
        method: 'POST',
        body: formData
      });
      const result = await response.json();
      if (result.success) {
        formMessage.textContent = '✅ ¡Depósito registrado!';
        formMessage.style.color = '#1f7a3d';
        amountInput.value = '';
        fetchDeposits(); // refrescar
      } else {
        formMessage.textContent = `❌ ${result.message}`;
        formMessage.style.color = '#b13e3e';
      }
    } catch (error) {
      formMessage.textContent = '❌ Error de conexión.';
      formMessage.style.color = '#b13e3e';
    }
  }

  // Validar y enviar
  depositBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const person = personSelect.value;
    const amount = parseFloat(amountInput.value);
    if (isNaN(amount) || amount <= 0) {
      formMessage.textContent = '⚠️ Ingresa un monto válido mayor a 0.';
      formMessage.style.color = '#b13e3e';
      return;
    }
    if (amount > 100000) {
      formMessage.textContent = '😅 Monto demasiado alto, verifica.';
      return;
    }
    formMessage.textContent = '';
    addDeposit(person, amount);
  });

  // Carga inicial
  fetchDeposits();
});