/* =========================================
   RUVANYA
   WHERE STYLE MEETS YOU
========================================= */


/* =========================================
   GO TO LOGIN PAGE
========================================= */

function goToLogin() {

    window.location.href = "login.html";

}


/* =========================================
   SMOOTH SCROLL
========================================= */

function scrollToSection(sectionId) {

    const section =
        document.getElementById(sectionId);

    if (section) {

        section.scrollIntoView({
            behavior: "smooth"
        });

    }

}


/* =========================================
   MOBILE MENU
========================================= */

function toggleMenu() {

    const nav =
        document.querySelector(".nav-links");

    if (nav.classList.contains("mobile-open")) {

        nav.classList.remove("mobile-open");

        nav.style.display = "none";

    } else {

        nav.classList.add("mobile-open");

        nav.style.display = "flex";

        nav.style.position = "absolute";

        nav.style.top = "78px";

        nav.style.left = "0";

        nav.style.right = "0";

        nav.style.padding = "25px";

        nav.style.background = "#F7F3E8";

        nav.style.flexDirection = "column";

        nav.style.alignItems = "center";

        nav.style.gap = "20px";

        nav.style.borderBottom =
            "1px solid #DAD7C6";

    }

}


/* =========================================
   CLOSE MOBILE MENU AFTER CLICK
========================================= */

const navLinks =
    document.querySelectorAll(".nav-links a");

navLinks.forEach(link => {

    link.addEventListener("click", () => {

        const nav =
            document.querySelector(".nav-links");

        nav.classList.remove("mobile-open");

        if (window.innerWidth <= 950) {

            nav.style.display = "none";

        }

    });

});


/* =========================================
   ACTIVE NAVIGATION
========================================= */

const sections =
    document.querySelectorAll("section");

const navigationLinks =
    document.querySelectorAll(".nav-links a");


window.addEventListener("scroll", () => {

    let currentSection = "";

    sections.forEach(section => {

        const sectionTop =
            section.offsetTop;

        const sectionHeight =
            section.offsetHeight;

        if (
            window.scrollY >=
            sectionTop - 150
        ) {

            currentSection =
                section.getAttribute("id");

        }

    });


    navigationLinks.forEach(link => {

        link.classList.remove("active");

        if (
            link.getAttribute("href") ===
            "#" + currentSection
        ) {

            link.classList.add("active");

        }

    });

});
