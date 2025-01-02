document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const cityNav = document.querySelector('.city-nav');
    const overlay = document.createElement('div');
    overlay.classList.add('nav-overlay');
    document.body.appendChild(overlay);

    // 移动端导航切换
    navToggle.addEventListener('click', () => {
        cityNav.classList.toggle('nav-open');
        overlay.classList.toggle('nav-overlay-active');
        navToggle.setAttribute('aria-expanded', 
            navToggle.getAttribute('aria-expanded') === 'true' ? 'false' : 'true'
        );
        
        // 禁止背景滚动
        document.body.style.overflow = cityNav.classList.contains('nav-open') ? 'hidden' : 'auto';
    });

    // 点击遮罩层或导航链接关闭菜单
    [overlay, ...document.querySelectorAll('.city-nav a')].forEach(element => {
        element.addEventListener('click', () => {
            cityNav.classList.remove('nav-open');
            overlay.classList.remove('nav-overlay-active');
            navToggle.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = 'auto';
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
