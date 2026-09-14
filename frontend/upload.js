const photoInput =
    document.getElementById("photoInput");

const uploadArea =
    document.getElementById("uploadArea");

const previewArea =
    document.getElementById("previewArea");

const previewImage =
    document.getElementById("previewImage");


/* =========================================
   OPEN FILE PICKER
========================================= */

function openFilePicker() {
    photoInput.click();
}


/* =========================================
   SELECT PHOTO
========================================= */

photoInput.addEventListener(
    "change",
    function () {

        const file =
            photoInput.files[0];

        if (!file) {
            return;
        }


        if (!file.type.startsWith("image/")) {

            alert(
                "Please select an image file."
            );

            return;
        }


        const reader =
            new FileReader();


        reader.onload =
            function (event) {

                const imageData =
                    event.target.result;


                /* SAVE PHOTO */

                localStorage.setItem(
                    "ruvanyaPhoto",
                    imageData
                );


                /* SHOW PHOTO */

                previewImage.src =
                    imageData;


                uploadArea.style.display =
                    "none";


                previewArea.classList.add(
                    "active"
                );

            };


        reader.readAsDataURL(file);

    }
);


/* =========================================
   CONTINUE
========================================= */

function continueToStyle() {

    const photo =
        localStorage.getItem(
            "ruvanyaPhoto"
        );


    if (!photo) {

        alert(
            "Please upload your photo first."
        );

        return;
    }


    window.location.href =
        "style.html";
}


/* =========================================
   HOME
========================================= */

function goHome() {

    window.location.href =
        "index.html";
}
