Array.from(document.getElementsByClassName("product-image-toggler")).forEach(
    (element) => {
        element.addEventListener("click", (e) => {
            /* First hide all images */
            Array.from(document.getElementsByClassName("product-image-toggled")).forEach(element => {
                element.classList.add("d-none")
            })
            /* Then find and unhide clicked image */
            let id_of_image_to_toggle = e.target.getAttribute("toggles-image")
            let element_to_toggle = document.getElementById(id_of_image_to_toggle)
            element_to_toggle.classList.remove("d-none")
        });
    }
);
