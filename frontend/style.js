const selections = {
    occasion: "",
    outfit: "",
    hairstyle: "",
    makeup: "",
    footwear: ""
};

const optionCards = document.querySelectorAll(".option-card");

optionCards.forEach(card => {

    card.addEventListener("click", function () {

        const group = this.dataset.group;
        const value = this.dataset.value;

        document
            .querySelectorAll(.option-card[data-group="${group}"])
            .forEach(item => {
                item.classList.remove("selected");
            });

        this.classList.add("selected");

        selections[group] = value;

        updateMessage();
    });
});


function updateMessage() {

    const selectedCount =
        Object.values(selections)
        .filter(value => value !== "")
        .length;

    const message =
        document.getElementById("selectionMessage");

    if (selectedCount === 0) {
        message.textContent =
            "Choose your preferences above.";
    }
    else if (selectedCount < 5) {
        message.textContent =
            ${selectedCount} of 5 preferences selected.;
    }
    else {
        message.textContent =
            "Perfect! Your style is ready to be created. ✨";
    }
}


function createLook() {

    const selectedCount =
        Object.values(selections)
        .filter(value => value !== "")
        .length;

    if (selectedCount < 5) {

        alert(
            "Please select one option from each section."
        );

        return;
    }

    // SAVE STYLE
    localStorage.setItem(
        "ruvanyaStyle",
        JSON.stringify(selections)
    );

    // OPEN RESULT PAGE
    window.location.href = "./result.html";
}


function goHome() {

    window.location.href = "./index.html";

}
