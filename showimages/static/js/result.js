/* :author: 高天驰
:copyright: © 2023 高天驰 <6159984@gmail.com> */


const reportContainer = document.getElementById("message-container");
const smallImageContainer = document.getElementById("small-images-container");
const navContainer = document.getElementById("page-nav");
const bigImageContainer = document.getElementById("big-image-container");
const processed = document.querySelector(".processed  > span:nth-child(2)");
const deleteThisOneBtn = document.getElementById("delete-this-one");
const deleteAllBtn = document.getElementById("delete-all");
const bigImage = document.getElementById("big-image");


function findSmallImageContainerNode(bigImageSrc) {
    const smallImageContainers = document.querySelectorAll(".small-image-container");
    for (let i = 0; i < smallImageContainers.length; i++) {
        let smallImageContainer = smallImageContainers[i];
        let smallImageNode = smallImageContainer.querySelector("img");
        if (smallImageNode.src == bigImageSrc) {
            const targetNode = smallImageContainer;
            if (i < smallImageContainers.length - 1) {
                let nextNode = smallImageContainers[i + 1];
                let nextNodeSrc = nextNode.querySelector("img").src;
                return {
                    "targetNode": targetNode,
                    "nextNodeSrc": nextNodeSrc
                }
            }
            else if (i == smallImageContainers.length - 1 & smallImageContainers.length > 1) {
                let nextNode = smallImageContainers[i - 1];
                let nextNodeSrc = nextNode.querySelector("img").src; return {
                    "targetNode": targetNode,
                    "nextNodeSrc": nextNodeSrc
                }
            }
            else {
                let nextNodeSrc = "/static/delete-warning.png";
                return {
                    "targetNode": targetNode,
                    "nextNodeSrc": nextNodeSrc
                }
            }
        }
    }

}


deleteThisOneBtn.addEventListener(
    "click",
    async () => {
        let bigImageSrc = bigImage.src;
        let imageName = bigImageSrc.split("/").pop();
        let deleteUrl = `api/delete-this-one/${imageName}`;
        await fetch(deleteUrl);
        let items = findSmallImageContainerNode(bigImageSrc);
        bigImage.src = items.nextNodeSrc;
        let report = await getReportFromImageUrl(items.nextNodeSrc);
        renderReport(report);
        if (items.nextNodeSrc == "/static/delete-warning.png") {
            location.reload();
        }

        items.targetNode.parentElement.removeChild(items.targetNode);
    }
)


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

async function getJsonItems(url) {
    let response = await fetch(url);
    let items = await response.json();
    return items;
}


async function updateHadProcessedFileCount() {
    let url = "api/processed-images"
    let items = await getJsonItems(url);
    let count = items.length;
    processed.innerHTML = "";
    processed.textContent = count;
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


function featureItemRegister(featureItem) {
    featureItem.addEventListener(
        "click",
        async () => {
            smallImageContainer.innerHTML = "";
            updateFeatureActive(featureItem);
            let feature = featureItem.querySelector("span").textContent;
            let items = await getItems(feature, page = 1);
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



function initFeatureEvents() {
    let featureItems = document.querySelectorAll("#feature-nav div");
    featureItems.forEach(
        (featureItem) => {
            featureItemRegister(featureItem);
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


document.addEventListener("DOMContentLoaded",
    async () => {
        initSmallImageEvent();
        initNavEvent();
        initFeatureEvents();
        await updateHadProcessedFileCount();
    });