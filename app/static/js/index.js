// In‑place filtering & highlight (no dropdown)
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('file-search');
    const listItems = document.querySelectorAll('.file-list li');
  
    if (!input) return;
  
    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      listItems.forEach(li => {
        const name = li.textContent.toLowerCase();
        li.style.display = name.includes(q) ? '' : 'none';
      });
    });
  });
  