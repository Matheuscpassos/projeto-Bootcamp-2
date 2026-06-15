// ============================================================================
// Gerenciador de Remédios — Lógica da Aplicação
// ============================================================================

// ── Referências DOM ─────────────────────────────────────────────────────────
const form = document.getElementById('remedioForm');
const inputNome = document.getElementById('nome');
const inputDosagem = document.getElementById('dosagem');
const inputHorarios = document.getElementById('horarios');
const inputCep = document.getElementById('cep');
const listContainer = document.getElementById('listContainer');
const countLabel = document.getElementById('countLabel');
const statusBar = document.getElementById('statusBar');
const themeToggle = document.getElementById('themeToggle');

// ── Estado local ────────────────────────────────────────────────────────────
let remedios = [];

// ══════════════════════════════════════════════════════════════════════════════
// VALIDAÇÕES (portadas do Python)
// ══════════════════════════════════════════════════════════════════════════════

/**
 * Valida o nome do remédio.
 * @returns {{ok: boolean, erro: string}}
 */
function validarNome(nome) {
  nome = nome.trim();
  if (!nome) {
    return { ok: false, erro: 'O nome não pode estar vazio.' };
  }
  if (/\d/.test(nome)) {
    return { ok: false, erro: 'O nome não pode conter números.' };
  }
  const duplicado = remedios.some(
    (r) => r.nome.toLowerCase() === nome.toLowerCase()
  );
  if (duplicado) {
    return { ok: false, erro: `"${nome}" já está cadastrado.` };
  }
  return { ok: true, erro: '' };
}

/**
 * Valida e formata a dosagem.
 * @returns {{ok: boolean, resultado: string}}
 */
function formatarDosagem(doseStr) {
  doseStr = doseStr.trim();
  if (!/^\d+$/.test(doseStr)) {
    return { ok: false, resultado: 'Digite apenas números inteiros para a dosagem.' };
  }
  const dose = parseInt(doseStr, 10);
  if (dose <= 0) {
    return { ok: false, resultado: 'A dosagem deve ser maior que zero.' };
  }
  if (dose >= 1000) {
    return { ok: true, resultado: `${(dose / 1000).toFixed(1)} g` };
  }
  return { ok: true, resultado: `${dose} mg` };
}

/**
 * Valida um horário no formato HH:MM (24h).
 */
function validarHorario(hora) {
  hora = hora.trim();
  if (!/^\d{2}:\d{2}$/.test(hora)) return false;
  const [h, m] = hora.split(':').map(Number);
  return h >= 0 && h <= 23 && m >= 0 && m <= 59;
}

/**
 * Valida o CEP (8 dígitos).
 */
function validarCEP(cep) {
  const limpo = cep.replace(/\D/g, '');
  return limpo.length === 8;
}

// ══════════════════════════════════════════════════════════════════════════════
// INTEGRAÇÃO VIACEP
// ══════════════════════════════════════════════════════════════════════════════

/**
 * Busca endereço pelo CEP via API ViaCEP.
 * @returns {Promise<{ok: boolean, resultado: string}>}
 */
async function buscarEnderecoCEP(cep) {
  const limpo = cep.replace(/\D/g, '');

  if (!validarCEP(cep)) {
    return { ok: false, resultado: 'CEP deve conter 8 dígitos.' };
  }

  try {
    const resp = await fetch(`https://viacep.com.br/ws/${limpo}/json/`, {
      signal: AbortSignal.timeout(5000),
    });

    if (!resp.ok) {
      return { ok: false, resultado: 'Erro ao conectar à API ViaCEP. Verifique sua conexão.' };
    }

    const dados = await resp.json();

    if (dados.erro) {
      return { ok: false, resultado: 'CEP não encontrado.' };
    }

    const logradouro = dados.logradouro || '';
    const bairro = dados.bairro || '';
    const cidade = dados.localidade || '';
    const uf = dados.uf || '';

    const partes = [logradouro, bairro].filter(Boolean).join(', ');
    const cidadeUf = cidade && uf ? `${cidade}/${uf}` : cidade || uf;

    let endereco;
    if (partes && cidadeUf) {
      endereco = `${partes} - ${cidadeUf}`;
    } else {
      endereco = partes || cidadeUf || 'Endereço não disponível';
    }

    return { ok: true, resultado: endereco };
  } catch {
    return { ok: false, resultado: 'Erro ao conectar à API ViaCEP. Verifique sua conexão.' };
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// UI — RENDERIZAÇÃO
// ══════════════════════════════════════════════════════════════════════════════

/**
 * Renderiza a lista de remédios no DOM.
 */
function renderRemedios() {
  const total = remedios.length;
  countLabel.textContent = `${total} remédio${total !== 1 ? 's' : ''}`;

  if (total === 0) {
    listContainer.innerHTML = `
      <div class="empty-state">
        Nenhum remédio cadastrado.<br />
        Use o formulário ao lado para adicionar.
      </div>`;
    return;
  }

  listContainer.innerHTML = remedios
    .map(
      (r) => `
    <div class="card">
      <div class="card-top">
        <span class="card-name">💊  ${escapeHTML(r.nome)}</span>
        <span class="card-dose">${escapeHTML(r.dosagem)}</span>
      </div>
      <div class="card-pills">
        ${r.horarios.map((h) => `<span class="pill">🕐 ${escapeHTML(h)}</span>`).join('')}
      </div>
      ${
        r.endereco && r.endereco !== '—'
          ? `<div class="card-address">📍 ${escapeHTML(r.endereco)}</div>`
          : ''
      }
      <div class="card-footer">
        <button class="btn-delete" onclick="handleDelete('${r.id}', '${escapeHTML(r.nome)}', '${escapeHTML(r.dosagem)}')">🗑  Excluir</button>
      </div>
    </div>`
    )
    .join('');
}

/**
 * Escapa HTML para prevenir XSS.
 */
function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ══════════════════════════════════════════════════════════════════════════════
// STATUS BAR
// ══════════════════════════════════════════════════════════════════════════════

function showStatus(msg, type = 'info') {
  statusBar.textContent = msg;
  statusBar.className = 'status-bar';
  if (type === 'error') statusBar.classList.add('error');
  if (type === 'success') statusBar.classList.add('success');
}

// ══════════════════════════════════════════════════════════════════════════════
// HANDLERS
// ══════════════════════════════════════════════════════════════════════════════

/**
 * Adiciona um remédio (submit do formulário).
 */
async function handleSubmit(e) {
  e.preventDefault();

  const nome = inputNome.value.trim();
  const doseStr = inputDosagem.value.trim();
  const horasStr = inputHorarios.value.trim();
  const cep = inputCep.value.trim();

  // Validar nome
  const nomeResult = validarNome(nome);
  if (!nomeResult.ok) {
    showStatus(`Erro: ${nomeResult.erro}`, 'error');
    return;
  }

  // Validar dosagem
  const doseResult = formatarDosagem(doseStr);
  if (!doseResult.ok) {
    showStatus(`Erro: ${doseResult.resultado}`, 'error');
    return;
  }

  // Validar horários
  const listaHoras = horasStr
    .split(',')
    .map((h) => h.trim())
    .filter(Boolean);

  if (listaHoras.length === 0) {
    showStatus('Erro: informe ao menos um horário.', 'error');
    return;
  }

  const invalidos = listaHoras.filter((h) => !validarHorario(h));
  if (invalidos.length > 0) {
    showStatus(
      `Erro: horário(s) inválido(s): ${invalidos.join(', ')}. Use o formato HH:MM (24h).`,
      'error'
    );
    return;
  }

  // Buscar CEP (opcional)
  let endereco = '—';
  if (cep) {
    showStatus('Consultando endereço na API ViaCEP...');
    const cepResult = await buscarEnderecoCEP(cep);
    if (!cepResult.ok) {
      showStatus(`Erro: ${cepResult.resultado}`, 'error');
      return;
    }
    endereco = cepResult.resultado;
  }

  // Salvar no Supabase
  showStatus('Salvando...');
  const { data, error } = await addRemedio({
    nome,
    dosagem: doseResult.resultado,
    horarios: listaHoras,
    endereco,
  });

  if (error) {
    showStatus(`Erro ao salvar: ${error.message}`, 'error');
    return;
  }

  // Atualizar estado local
  remedios.push(data);
  renderRemedios();

  // Limpar formulário
  form.reset();
  showStatus(`"${nome}" adicionado com sucesso.`, 'success');
}

/**
 * Exclui um remédio com confirmação via confirm().
 */
async function handleDelete(id, nome, dosagem) {
  const confirmar = confirm(`Deseja excluir "${nome}" (${dosagem})?`);
  if (!confirmar) return;

  showStatus('Excluindo...');
  const { error } = await deleteRemedio(id);

  if (error) {
    showStatus(`Erro ao excluir: ${error.message}`, 'error');
    return;
  }

  remedios = remedios.filter((r) => r.id !== id);
  renderRemedios();
  showStatus(`"${nome}" excluído com sucesso.`, 'success');
}

// ══════════════════════════════════════════════════════════════════════════════
// TEMA CLARO / ESCURO
// ══════════════════════════════════════════════════════════════════════════════

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';

  if (next === 'light') {
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  themeToggle.textContent = next === 'dark' ? '☀️' : '🌙';
  localStorage.setItem('theme', next);
}

function applyStoredTheme() {
  const stored = localStorage.getItem('theme') || 'dark';
  if (stored === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
    themeToggle.textContent = '☀️';
  } else {
    document.documentElement.removeAttribute('data-theme');
    themeToggle.textContent = '🌙';
  }
}

// ══════════════════════════════════════════════════════════════════════════════
// INICIALIZAÇÃO
// ══════════════════════════════════════════════════════════════════════════════

async function init() {
  applyStoredTheme();

  showStatus('Carregando remédios...');
  const { data, error } = await fetchRemedios();

  if (error) {
    showStatus(`Erro ao carregar: ${error.message}`, 'error');
    return;
  }

  remedios = data;
  renderRemedios();
  showStatus('Pronto.');
}

// Event listeners
form.addEventListener('submit', handleSubmit);
themeToggle.addEventListener('click', toggleTheme);

// Iniciar
init();
