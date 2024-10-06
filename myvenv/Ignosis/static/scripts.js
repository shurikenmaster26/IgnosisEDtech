/*!
* Start Bootstrap - Landing Page v6.0.6 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

document.addEventListener("DOMContentLoaded", function() {
    let currentIndex = 0;
    const totalSlides = document.querySelectorAll('.slide').length;

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlider();
    }

    function updateSlider() {
        const translateValue = -currentIndex * 100 / totalSlides;
        document.querySelector('.slider-container').style.transform = `translateX(${translateValue}%)`;
    }

    // Automatically switch slides every 3 seconds
    setInterval(nextSlide, 3000);
});