const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

// Устанавливаем начальную тему
if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-theme');
    themeToggle.checked = true;
}

// Слушаем изменения переключателя
themeToggle.addEventListener('change', () => {
    body.classList.toggle('dark-theme');

    // Сохраняем выбранную тему в localStorage
    if (body.classList.contains('dark-theme')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});
