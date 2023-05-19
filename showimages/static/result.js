const reportContainer = document.getElementById("message-container");
const smallImageContainer = document.getElementById("small-images-container");
const navContainer = document.getElementById("page-nav");
const bigImageContainer = document.getElementById("big-image-container");



function getFeature() {
    let feature = document.querySelector("#feature-nav div.btn.active span").textContent;

    return feature
}


async function getItems(feature, page) {
    let url = `api/page-urls/${feature}?page=${page}`;
    let response = await fetch(url);
    let items = await response.json();
    return items
}


async function getReportFromImageUrl(imageUrl) {
    let imageName = imageUrl.split("/").pop();
    let url = `api/get-report/${imageName}`;

    let response = await fetch(url);
    let items = await response.json();

    return items
}


function createImageItem(url) {
    const smallImageItem = document.createElement("div");
    const smallImage = document.createElement("img");

    smallImageItem.setAttribute("class", "small-image-container");
    smallImage.setAttribute("class", "small-image");
    smallImage.setAttribute("alt", "small image");
    smallImage.setAttribute("src", url);

    smallImageItem.appendChild(smallImage);

    return smallImageItem
}


function renderReport(report) {
    reportContainer.innerHTML = "";

    for (const [key, value] of Object.entries(report)) {
        const reportItemKey = document.createElement("span");
        const reportItemValue = document.createElement("span");

        reportItemKey.textContent = key + ": ";
        reportItemValue.textContent = value;

        const reportItem = document.createElement("div");
        reportItem.appendChild(reportItemKey);
        reportItem.appendChild(reportItemValue);

        reportContainer.appendChild(reportItem);
    }

}


function createNavItem(page) {
    const newNavItemContainer = document.createElement("div");
    const newNavItem = document.createElement("span");

    if (page == 1) {
        newNavItemContainer.setAttribute("class", "btn active");
    } else {
        newNavItemContainer.setAttribute("class", "btn");
    }

    newNavItemContainer.setAttribute("data-page", page);

    newNavItem.textContent = page;
    newNavItemContainer.appendChild(newNavItem);

    return newNavItemContainer
}


function renderNavItems(numPages) {
    navContainer.innerHTML = "";
    for (let i = 1; i <= numPages; i++) {
        let newNavItem = createNavItem(i);
        navEventRegister(newNavItem);
        navContainer.appendChild(newNavItem);
    }
}


async function smallImageEventRegister(smallImageNode) {
    smallImageNode.addEventListener(
        "click",
        async () => {
            let imageUrl = smallImageNode.querySelector("img").src;
            let bigImage = bigImageContainer.querySelector("img");
            bigImage.src = imageUrl;
            let report = await getReportFromImageUrl(imageUrl);
            renderReport(report);
        }
    );
}


function updateNavActive(currentNavItem) {
    const navElements = document.querySelectorAll("#page-nav div");
    navElements.forEach(
        (navElement) => {
            navElement.setAttribute("class", "btn");
        }
    );
    currentNavItem.setAttribute("class", "btn active");
}

function updateFeatureActive(currentFeatureItem) {
    let featureItems = document.querySelectorAll("#feature-nav div");
    featureItems.forEach(
        (featureItem) => {
            featureItem.setAttribute("class", "btn");
        }
    );
    currentFeatureItem.setAttribute("class", "btn active");
}


function initFeatureEvent() {
    let featureItems = document.querySelectorAll("#feature-nav div");
    featureItems.forEach(
        (featureItem) => {
            featureItem.addEventListener(
                "click",
                async () => {
                    smallImageContainer.innerHTML = "";
                    updateFeatureActive(featureItem);
                    let feature = featureItem.querySelector("span").textContent;
                    let items = await getItems(feature, page=1);
                    let imageItems = items.image_items;
                    let numPages = items.num_pages;
                    renderNavItems(numPages);
                    
                    for (let i = 0; i < imageItems.length; i++) {
                        let imageUrl = imageItems[i]["image_url"];
                        let newImageNode = createImageItem(imageUrl);
                        await smallImageEventRegister(newImageNode);
                        smallImageContainer.appendChild(newImageNode);
                    }
                }
            );
        }
    );
}



function initSmallImageEvent() {
    let smallImageItems = document.querySelectorAll(".small-image-container");
    smallImageItems.forEach(
        async (smallImageItem) => {
            await smallImageEventRegister(smallImageItem);
        }
    );
}


function navEventRegister(navItem) {
    navItem.addEventListener(
        "click",
        async () => {
            updateNavActive(navItem);
            
            let feature = getFeature();
            let page = navItem.querySelector("span").textContent;
            let items = await getItems(feature, page);
            let imageItems = items.image_items;
            smallImageContainer.innerHTML = "";
            for (let i = 0; i < imageItems.length; i++) {
                let imageUrl = imageItems[i]["image_url"];
                let newImageNode = createImageItem(imageUrl);
                await smallImageEventRegister(newImageNode);
                smallImageContainer.appendChild(newImageNode);
            }
        }
    );
}


function initNavEvent() {
    let navItems = document.querySelectorAll("#page-nav div");
    navItems.forEach(
        (navItem) => {
            navEventRegister(navItem);
        }
    );
}


document.addEventListener("DOMContentLoaded", () => {
    initSmallImageEvent();
    initNavEvent();
    initFeatureEvent();
});