document.addEventListener('DOMContentLoaded', () => {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const mobileNavOverlay = document.querySelector('.mobile-nav-overlay');
    const mobileNavClose = document.querySelector('.mobile-nav-close');
    const cityNavLinks = document.querySelectorAll('.city-nav a');

    // 确保汉堡菜单按钮内有正确的元素
    if (mobileNavToggle && !mobileNavToggle.querySelector('.hamburger')) {
        const hamburger = document.createElement('div');
        hamburger.classList.add('hamburger');
        mobileNavToggle.appendChild(hamburger);
    }

    // 切换移动端导航
    function toggleMobileNav() {
        if (mobileNavToggle && mobileNavOverlay) {
            mobileNavToggle.classList.toggle('active');
            mobileNavOverlay.classList.toggle('active');
            
            // 禁止/恢复背景滚动
            document.body.style.overflow = mobileNavOverlay.classList.contains('active') 
                ? 'hidden' 
                : 'auto';
        }
    }

    // 关闭移动端导航
    function closeMobileNav() {
        if (mobileNavToggle && mobileNavOverlay) {
            mobileNavToggle.classList.remove('active');
            mobileNavOverlay.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    }

    // 点击汉堡菜单按钮
    if (mobileNavToggle) {
        mobileNavToggle.addEventListener('click', toggleMobileNav);
    }

    // 点击关闭按钮
    if (mobileNavClose) {
        mobileNavClose.addEventListener('click', closeMobileNav);
    }

    // 点击遮罩层关闭导航
    if (mobileNavOverlay) {
        mobileNavOverlay.addEventListener('click', (event) => {
            if (event.target === mobileNavOverlay) {
                closeMobileNav();
            }
        });
    }

    // 点击导航链接后关闭导航
    cityNavLinks.forEach(link => {
        link.addEventListener('click', closeMobileNav);
    });

    // 平滑滚动到锚点
    cityNavLinks.forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});
