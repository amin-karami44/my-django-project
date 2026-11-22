document.addEventListener("DOMContentLoaded", function () {
    const navToggle = document.querySelector(".nav-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (!navToggle || !navLinks) {
        return;
    }

    navToggle.addEventListener("click", function () {
        const isOpen = navLinks.classList.toggle("is-open");

        navToggle.setAttribute("aria-expanded", isOpen);
        navToggle.setAttribute(
            "aria-label",
            isOpen ? "بستن منو" : "باز کردن منو"
        );
    });
});