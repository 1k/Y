document.addEventListener('DOMContentLoaded', function() {
    const backToTopButton = document.getElementById('back-to-top');
    const mobileNavToggle = document.getElementById('mobile-nav-toggle');
    const mobileNavClose = document.getElementById('mobile-nav-close');
    const mobileNavOverlay = document.getElementById('mobile-nav-overlay');

    // 显示/隐藏返回顶部按钮
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    // 点击返回顶部
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // 移动端导航栏切换
    mobileNavToggle.addEventListener('click', function() {
        mobileNavOverlay.classList.add('show');
    });

    mobileNavClose.addEventListener('click', function() {
        mobileNavOverlay.classList.remove('show');
    });

    // 点击导航链接关闭遮罩层
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-overlay .city-nav a');
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileNavOverlay.classList.remove('show');
        });
    });
});
