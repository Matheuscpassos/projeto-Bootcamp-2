// ============================================================================
// Supabase Client — Gerenciador de Remédios
// ============================================================================
// CONFIGURAÇÃO: Substitua os valores abaixo pelas credenciais do seu projeto
// Supabase. Você encontra essas informações em:
//   https://app.supabase.com → seu projeto → Settings → API
// ============================================================================

const SUPABASE_URL = 'https://uftiflyoufinrarhovmd.supabase.co';       // Ex: https://xxxxx.supabase.co
const SUPABASE_ANON_KEY = 'sb_publishable_2uaBHXRO0Gw1DRSLlAq15A_t_1_n_0G'; // Ex: eyJhbGciOi...

// Inicializa o client Supabase (SDK carregado via CDN no index.html)
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// ── SQL para criar a tabela (execute no Supabase SQL Editor) ────────────────
// CREATE TABLE remedios (
//   id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   nome       TEXT NOT NULL,
//   dosagem    TEXT NOT NULL,
//   horarios   TEXT[] NOT NULL DEFAULT '{}',
//   endereco   TEXT DEFAULT '—',
//   created_at TIMESTAMPTZ DEFAULT now()
// );
//
// -- Habilitar acesso público (RLS):
// ALTER TABLE remedios ENABLE ROW LEVEL SECURITY;
// CREATE POLICY "Allow all" ON remedios FOR ALL USING (true) WITH CHECK (true);
// ────────────────────────────────────────────────────────────────────────────

/**
 * Busca todos os remédios ordenados por data de criação.
 * @returns {Promise<{data: Array, error: object|null}>}
 */
async function fetchRemedios() {
  const { data, error } = await supabase
    .from('remedios')
    .select('*')
    .order('created_at', { ascending: true });

  return { data: data || [], error };
}

/**
 * Adiciona um novo remédio.
 * @param {{nome: string, dosagem: string, horarios: string[], endereco: string}} remedio
 * @returns {Promise<{data: object|null, error: object|null}>}
 */
async function addRemedio(remedio) {
  const { data, error } = await supabase
    .from('remedios')
    .insert([remedio])
    .select()
    .single();

  return { data, error };
}

/**
 * Exclui um remédio pelo ID.
 * @param {string} id — UUID do remédio
 * @returns {Promise<{error: object|null}>}
 */
async function deleteRemedio(id) {
  const { error } = await supabase
    .from('remedios')
    .delete()
    .eq('id', id);

  return { error };
}

/**
 * Verifica se já existe um remédio com o mesmo nome (case-insensitive).
 * @param {string} nome
 * @returns {Promise<boolean>}
 */
async function checkDuplicateName(nome) {
  const { data } = await supabase
    .from('remedios')
    .select('id')
    .ilike('nome', nome);

  return data && data.length > 0;

// ============================================================================
// Supabase Client — Gerenciador de Remédios
// ============================================================================
// CONFIGURAÇÃO: Substitua os valores abaixo pelas credenciais do seu projeto
// Supabase. Você encontra essas informações em:
//   https://app.supabase.com → seu projeto → Settings → API
// ============================================================================

const SUPABASE_URL = 'https://uftiflyoufinrarhovmd.supabase.co';       // Ex: https://xxxxx.supabase.co
const SUPABASE_ANON_KEY = 'sb_publishable_2uaBHXRO0Gw1DRSLlAq15A_t_1_n_0G'; // Ex: eyJhbGciOi...

// Inicializa o client Supabase (SDK carregado via CDN no index.html)
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// ── SQL para criar a tabela (execute no Supabase SQL Editor) ────────────────
// CREATE TABLE remedios (
//   id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
//   nome       TEXT NOT NULL,
//   dosagem    TEXT NOT NULL,
//   horarios   TEXT[] NOT NULL DEFAULT '{}',
//   endereco   TEXT DEFAULT '—',
//   created_at TIMESTAMPTZ DEFAULT now()
// );
//
// -- Habilitar acesso público (RLS):
// ALTER TABLE remedios ENABLE ROW LEVEL SECURITY;
// CREATE POLICY "Allow all" ON remedios FOR ALL USING (true) WITH CHECK (true);
// ────────────────────────────────────────────────────────────────────────────

/**
 * Busca todos os remédios ordenados por data de criação.
 * @returns {Promise<{data: Array, error: object|null}>}
 */
async function fetchRemedios() {
  const { data, error } = await supabase
    .from('remedios')
    .select('*')
    .order('created_at', { ascending: true });

  return { data: data || [], error };
}

/**
 * Adiciona um novo remédio.
 * @param {{nome: string, dosagem: string, horarios: string[], endereco: string}} remedio
 * @returns {Promise<{data: object|null, error: object|null}>}
 */
async function addRemedio(remedio) {
  const { data, error } = await supabase
    .from('remedios')
    .insert([remedio])
    .select()
    .single();

  return { data, error };
}

/**
 * Exclui um remédio pelo ID.
 * @param {string} id — UUID do remédio
 * @returns {Promise<{error: object|null}>}
 */
async function deleteRemedio(id) {
  const { error } = await supabase
    .from('remedios')
    .delete()
    .eq('id', id);

  return { error };
}

/**
 * Verifica se já existe um remédio com o mesmo nome (case-insensitive).
 * @param {string} nome
 * @returns {Promise<boolean>}
 */
async function checkDuplicateName(nome) {
  const { data } = await supabase
    .from('remedios')
    .select('id')
    .ilike('nome', nome);

  return data && data.length > 0;
  }
  
}