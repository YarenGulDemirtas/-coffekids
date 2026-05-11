document.addEventListener("DOMContentLoaded", () => {

    // ======================
    // MOBİL MENÜ
    // ======================

    const menuBtn = document.querySelector(".menu-btn");
    const navLinks = document.querySelector(".nav-links");

    if(menuBtn && navLinks){

        menuBtn.addEventListener("click", () => {

            navLinks.classList.toggle("mobile-active");

        });

    }

    // ======================
    // GALERİ SLIDER
    // ======================

    const sliderTrack = document.querySelector(".slider-track");
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");

    if(sliderTrack && prevBtn && nextBtn){

        const slides = sliderTrack.querySelectorAll("img");

        let currentSlide = 0;

        function changeSlide(){

            const slideWidth = slides[0].clientWidth;

            sliderTrack.style.transform =
            `translateX(-${currentSlide * slideWidth}px)`;

        }

        nextBtn.addEventListener("click", () => {

            currentSlide++;

            if(currentSlide >= slides.length){
                currentSlide = 0;
            }

            changeSlide();

        });

        prevBtn.addEventListener("click", () => {

            currentSlide--;

            if(currentSlide < 0){
                currentSlide = slides.length - 1;
            }

            changeSlide();

        });

        window.addEventListener("resize", changeSlide);

    }

});