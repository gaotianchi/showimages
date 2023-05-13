const smallImages = document.querySelectorAll('.small-image');
const bigImage = document.querySelector('#big-image');
const positionMessage = document.querySelector('#position');
const error1Message = document.querySelector('#error1');
const error2Message = document.querySelector('#error2');
const imageStatus = document.querySelectorAll('.image-status');
const navContainer = document.querySelector('#nav-container');
const okStatus = document.querySelector('#ok');
const errorStatus = document.querySelector('#error');




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
            replaceImagesWithUrls(newImageUrls);
        });
    }
);


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


let navElements = document.querySelectorAll('.nav');
navElements.forEach(
    (navElement) => {
        navElement.addEventListener('click', 
        async () => {
            let page = navElement.textContent;
            let url = `/api/result/page-hashs/${page}`;
        });
    }
);