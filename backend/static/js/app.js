// X5 frontend helpers: динамический prompt/placeholder/hint и счётчик символов
document.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('case_id');
  const promptBox = document.getElementById('case-prompt');
  const ta = document.getElementById('answer');
  const hintBox = document.getElementById('hint');
  const chars = document.getElementById('chars');
  const btn = document.getElementById('check-btn');

  function safeParseJSON(s) {
    try { return JSON.parse(s); } catch { return s; }
  }

  function setFromCase() {
    const opt = select?.selectedOptions?.[0];
    if (!opt) return;

    // prompt (с абзацами)
    const prompt = safeParseJSON(opt.getAttribute('data-prompt') || '') || '—';
    const html = String(prompt).replace(/\n/g, '<br>');
    if (promptBox) promptBox.innerHTML = html;

    // placeholder
    const placeholder = safeParseJSON(opt.getAttribute('data-placeholder') || '');
    if (ta) ta.placeholder = placeholder || 'Введите ваш ответ…';

    // hint
    const hint = safeParseJSON(opt.getAttribute('data-hint') || '');
    if (hintBox) hintBox.textContent = hint || '';
  }

  setFromCase();
  select?.addEventListener('change', setFromCase);

  // Счётчик символов
  if (ta && chars) {
    const limit = 6000;
    const update = () => {
      const len = ta.value.length;
      chars.textContent = `${len}/${limit}`;
      chars.style.color = len > limit * 0.9 ? '#d33' : '';
    };
    ta.addEventListener('input', update);
    update();
  }

  // Лёгкая индикация на кнопке (визуально)
  btn?.addEventListener('click', () => {
    btn.classList.add('disabled');
    btn.innerHTML = 'Проверяем…';
    setTimeout(() => {
      btn.classList.remove('disabled');
      btn.innerHTML = 'Проверить';
    }, 1200);
  });
});
