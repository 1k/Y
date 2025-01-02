document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const cityNav = document.querySelector('.city-nav');

    // 移动端导航切换
    navToggle.addEventListener('click', () => {
        cityNav.classList.toggle('show');
        navToggle.setAttribute('aria-expanded', 
            navToggle.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
        );
    });

    // 点击导航链接后关闭移动端菜单
    const navLinks = document.querySelectorAll('.city-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            cityNav.classList.remove('show');
            navToggle.setAttribute('aria-expanded', 'false');
        });
    });

    // 平滑滚动到锚点
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
