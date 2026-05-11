document.addEventListener('DOMContentLoaded', function () {

    // =========================
    // MOBİL MENÜ
    // =========================

    const menuBtn = document.querySelector('.menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (menuBtn && navLinks) {

        menuBtn.addEventListener('click', function () {

            navLinks.classList.toggle('mobile-active');

        });

    }

    // =========================
    // GALERİ SLIDER
    // =========================

    const track = document.querySelector('.slider-track');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    if (track && prevBtn && nextBtn) {

        const slides = Array.from(track.children);

        let currentIndex = 0;

        function updateSlider() {

            const slideWidth = slides[0].getBoundingClientRect().width;

            track.style.transform =
                `translateX(-${currentIndex * slideWidth}px)`;
        }

        nextBtn.addEventListener('click', () => {

            if (currentIndex < slides.length - 1) {
                currentIndex++;
            } else {
                currentIndex = 0;
            }

            updateSlider();
        });

        prevBtn.addEventListener('click', () => {

            if (currentIndex > 0) {
                currentIndex--;
            } else {
                currentIndex = slides.length - 1;
            }

            updateSlider();
        });

        window.addEventListener('resize', updateSlider);
    }

});