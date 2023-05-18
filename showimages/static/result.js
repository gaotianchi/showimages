const bigImage = document.getElementById("big-image");
const smallImgages = document.querySelectorAll(".small-image");



smallImgages.forEach(
    (smallImage) => {
        smallImage.addEventListener("click",
            () => {
                let smallImageUrl = smallImage.src;
                bigImage.src = smallImageUrl;
            });
    }
);


function createMessageContainer(json) {

    const messageContainer = document.getElementById("message-container");

    for (var key in json) {
        if (json.hasOwnProperty(key)) {
            var div = document.createElement("div");

            var keySpan = document.createElement("span");
            keySpan.textContent = key + ": ";
            div.appendChild(keySpan);

            var valueSpan = document.createElement("span");
            valueSpan.textContent = json[key];
            div.appendChild(valueSpan);

            messageContainer.appendChild(div);
        }
    }
}


function getSmallImageItem(url) {
    const smallImageItem = document.createElement("div");
    const smallImage = document.createElement("img");

    smallImageItem.setAttribute("class", "small-image-container");
    smallImage.setAttribute("class", "small-image");
    smallImage.setAttribute("alt", "small image");
    smallImage.setAttribute("src", url);

    smallImageItem.appendChild(smallImage);

    return smallImageItem
}


function createNavItems(numPages) {
    const pageNav = document.getElementById("page-nav");

    for (let i = 0; i < numPages; i++) {
        const navItem = document.createElement("div");
        navItem.setAttribute("class", "btn");

        const textItem = document.createElement("span");
        textItem.textContent = i + 1;

        navItem.appendChild(textItem);

        pageNav.appendChild(navItem)
    }
}

