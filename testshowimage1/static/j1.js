const bigImage = document.querySelector('#big-image');
const positionMessage = document.querySelector('#position');
const error1Message = document.querySelector('#error1');
const error2Message = document.querySelector('#error2');
const imageStatus = document.querySelectorAll('.image-status');
const navContainer = document.querySelector('#nav-container');
const okStatus = document.querySelector('#ok');
const errorStatus = document.querySelector('#error');
const smallImageContainer = document.querySelector("#small-image-container");




async function getMessages(imageUrl) {
    let arr = String(imageUrl).split('/');
    let status = arr[arr.length - 2];
    let hash = arr[arr.length - 1];
    let url = `/api/result-reports/${status}/${hash}`;
    let response = await fetch(url);
    let message = await response.json();
    return message;
}


function relpaceMessage(message) {
    positionMessage.textContent = message.position;
    error1Message.textContent = message.error1;
    error2Message.textContent = message.error2;
}


function removeOldImageElements() {
    let imageElements = document.querySelectorAll(".small-image");
    for (var i = 0; i < imageElements.length; i++) {
        imageElements[i].parentNode.removeChild(imageElements[i]);
    }
}


async function renderImages(imageUrls) {
    removeOldImageElements();
    for (let i = 0; i < imageUrls.length; i++) {
        let newImageNode = document.createElement("img");
        newImageNode.setAttribute("class", "small-image");
        newImageNode.setAttribute("src", imageUrls[i]);
        newImageNode.setAttribute("height", "200px");
        newImageNode.setAttribute("alt", "small-image");

        smallImageContainer.appendChild(newImageNode);

        newImageNode.addEventListener("click", 
        async () => {
            let smallImageUrl = newImageNode.src;
            let message = await getMessages(smallImageUrl)
            bigImage.src = smallImageUrl;
            relpaceMessage(message);
        });

    }
}


function replaceImagesWithUrls(newUrls) {
    smallImages.forEach(
        (oldImage, index) => {
            let newUrl = newUrls[index];
            oldImage.src = newUrl;
        }
    );
}


function removeNavElement() {
    let navElement = document.querySelectorAll('.nav');
    for (var i = 0; i < navElement.length; i++) {
        navElement[i].parentNode.removeChild(navElement[i]);
    }
}

async function renderNav(status) {
    let response = await fetch('/api/num-pages');
    let items = await response.json();
    let num_pages = items[status];
    removeNavElement();

    for (let i=1; i <= Number(num_pages); i++) {
        let newNavNode = document.createElement("div");
        newNavNode.setAttribute('class', 'nav');
        let divText = document.createTextNode(i);
        newNavNode.appendChild(divText);
        navContainer.appendChild(newNavNode);

        newNavNode.addEventListener('click', 
            async () => {
                let statusNode = document.querySelector(".image-status.active");
                let text = statusNode.textContent;
                let page = newNavNode.textContent;
                let url = `/api/result/page-hashs/${text}?page=${page}`;
                let response = await fetch(url);
                let newImageUrls = await response.json();
                await renderImages(newImageUrls);
            });
    }
}


imageStatus.forEach(
    (statusBtn) => {
        statusBtn.addEventListener('click', 
        async () => {
            let spanNode = statusBtn.getElementsByTagName('span')[0];
            let text = spanNode.textContent;
            if (text == 'error') {
                errorStatus.className = "image-status active";
                okStatus.className = "image-status";
            }
            else {
                okStatus.className = "image-status active";
                errorStatus.className = "image-status";
            }

            await renderNav(text);
            let url = `/api/result/page-hashs/${text}`;
            let response = await fetch(url);
            let newImageUrls = await response.json();
            await renderImages(newImageUrls);
        });
    }
);


function initImgElements() {
    let smallImages = document.querySelectorAll('.small-image');
    smallImages.forEach(
        (smallImage) => {
            smallImage.addEventListener('click', 
            async () => {
                let smallImageUrl = smallImage.src;
                let message = await getMessages(smallImageUrl)
                bigImage.src = smallImageUrl;
                relpaceMessage(message);
            });
        }
    );
}


function initNavElements() {
    let navElements = document.querySelectorAll('.nav');
    navElements.forEach((navElement) => {
        navElement.addEventListener('click', async () => {
            let statusNode = document.querySelector(".image-status.active");
            let text = statusNode.textContent;
            let page = navElement.textContent;
            let url = `/api/result/page-hashs/${text}?page=${page}`;
            let response = await fetch(url);
            let newImageUrls = await response.json();
            await renderImages(newImageUrls);
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    // 初始化页面时注册分页导航栏的点击事件
    initNavElements();
    initImgElements();
});
