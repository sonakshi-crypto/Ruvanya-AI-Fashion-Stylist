/* =========================================
   RUVANYA LOGIN / SIGN UP
========================================= */


/* GET ELEMENTS */

const signInTab =
    document.getElementById("signInTab");

const signUpTab =
    document.getElementById("signUpTab");

const signInForm =
    document.getElementById("signInForm");

const signUpForm =
    document.getElementById("signUpForm");

const formTitle =
    document.getElementById("formTitle");

const formSubtitle =
    document.getElementById("formSubtitle");

const switchToSignUp =
    document.getElementById("switchToSignUp");

const switchToSignIn =
    document.getElementById("switchToSignIn");


/* =========================================
   SHOW SIGN IN
========================================= */

function showSignIn() {

    signInTab.classList.add("active");

    signUpTab.classList.remove("active");

    signInForm.classList.add("active-form");

    signUpForm.classList.remove("active-form");

    formTitle.textContent =
        "Welcome Back";

    formSubtitle.textContent =
        "Sign in to continue your style journey.";

}


/* =========================================
   SHOW SIGN UP
========================================= */

function showSignUp() {

    signUpTab.classList.add("active");

    signInTab.classList.remove("active");

    signUpForm.classList.add("active-form");

    signInForm.classList.remove("active-form");

    formTitle.textContent =
        "Create Your Account";

    formSubtitle.textContent =
        "Start your personalized style journey.";

}


/* =========================================
   TAB EVENTS
========================================= */

signInTab.addEventListener(
    "click",
    showSignIn
);


signUpTab.addEventListener(
    "click",
    showSignUp
);


switchToSignUp.addEventListener(
    "click",
    showSignUp
);


switchToSignIn.addEventListener(
    "click",
    showSignIn
);


/* =========================================
   SIGN UP VALIDATION
========================================= */

signUpForm.addEventListener(
    "submit",
    function(event) {

        event.preventDefault();

        const password =
            document.getElementById(
                "signupPassword"
            ).value;

        const confirmPassword =
            document.getElementById(
                "signupConfirmPassword"
            ).value;


        if (password !== confirmPassword) {

            alert(
                "Passwords do not match."
            );

            return;

        }


        alert(
            "Account created successfully!"
        );

    }
);


/* =========================================
   SIGN IN
========================================= */

signInForm.addEventListener(
    "submit",
    function(event) {

        event.preventDefault();

        alert(
            "Sign in functionality will be connected to the backend next."
        );

    }
);
