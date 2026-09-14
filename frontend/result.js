/* =========================================
   GET SAVED DATA
========================================= */

const savedPhoto =
    localStorage.getItem("ruvanyaPhoto");

const savedStyle =
    localStorage.getItem("ruvanyaStyle");


/* =========================================
   CHECK PHOTO
========================================= */

if (!savedPhoto) {

    alert(
        "Please upload your photo first."
    );

    window.location.href =
        "upload.html";

}


/* =========================================
   SHOW PHOTO
========================================= */

else {

    const resultPhoto =
        document.getElementById(
            "resultPhoto"
        );

    resultPhoto.src =
        savedPhoto;

}


/* =========================================
   CHECK STYLE
========================================= */

if (!savedStyle) {

    alert(
        "Please select your style first."
    );

    window.location.href =
        "style.html";

}


/* =========================================
   SHOW STYLE
========================================= */

else {

    const style =
        JSON.parse(savedStyle);


    document.getElementById(
        "occasion"
    ).textContent =
        style.occasion;


    document.getElementById(
        "outfit"
    ).textContent =
        style.outfit;


    document.getElementById(
        "hairstyle"
    ).textContent =
        style.hairstyle;


    document.getElementById(
        "makeup"
    ).textContent =
        style.makeup;


    document.getElementById(
        "footwear"
    ).textContent =
        style.footwear;


    document.getElementById(
        "styleName"
    ).textContent =
        `${style.outfit} ${style.occasion} Look`;


    document.getElementById(
        "styleDescription"
    ).textContent =
        `A ${style.outfit.toLowerCase()} look for ${style.occasion.toLowerCase()}, paired with ${style.hairstyle.toLowerCase()}, ${style.makeup.toLowerCase()} makeup and ${style.footwear.toLowerCase()}.`;

}


/* =========================================
   TRY ANOTHER LOOK
========================================= */

function tryAgain() {

    window.location.href =
        "style.html";

}


/* =========================================
   START OVER
========================================= */

function startOver() {

    localStorage.removeItem(
        "ruvanyaPhoto"
    );

    localStorage.removeItem(
        "ruvanyaStyle"
    );

    window.location.href =
        "index.html";

}


/* =========================================
   HOME
========================================= */

function goHome() {

    window.location.href =
        "index.html";

}
