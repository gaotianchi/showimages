/* :author: 高天驰
:copyright: © 2023 高天驰 <6159984@gmail.com> */


const fileSub = document.getElementById("fileSub");
const fileSelect = document.getElementById("file-source-button");
const btns = document.querySelectorAll(".btn");
fileList = document.getElementById("fileList");
tBody = document.getElementsByTagName("tbody")[0];
fileElem = document.getElementById("fileElem");
moreFilesBtnContainer = document.getElementById("file-source-more-button-background");
seleElement = document.getElementById("file-source-button-background");
moreFilesBtn = document.getElementById("more-file-source-button");
uploadFile = document.getElementById("upload-file");
const statusContainer = document.getElementById("status-container");
const upload = document.querySelector(".upload > span:nth-child(2)");
const processed = document.querySelector(".processed  > span:nth-child(2)");
const resultLink = document.querySelector("#status > div.processed > span:nth-child(1) > a");


resultLink.addEventListener(
    "click",
    () => {
        const num = document.querySelector("#status > div.processed > span:nth-child(2)").textContent;
        if (Number(num) == 0) {
            alert("还没有上传任何图片！");
        }
    }
)


btns.forEach(
    (btn) => {
        btn.addEventListener("mouseenter",
            function () {
                btn.style.cursor = 'grab';
            });
    }
);


fileSelect.addEventListener(
    "click",
    (e) => {
        if (fileElem) {
            fileElem.click();
        }
        e.preventDefault();
    },
    false
);

moreFilesBtn.addEventListener(
    "click",
    (e) => {
        if (fileElem) {
            fileElem.click();
        }
        e.preventDefault();
    },
    false
);

uploadFile.addEventListener(
    "click",
    (e) => {
        if (fileSub) {
            fileSub.click();
        }
        e.preventDefault();
    },
    false
);


function updateToUploadFileCount() {
    upload.innerHTML = "";
    let count = fileElem.files.length;
    upload.textContent = count;
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


document.addEventListener("DOMContentLoaded",
    async () => {
        await updateHadProcessedFileCount();
    }
);


fileElem.addEventListener("change", showImages, false);


function showImages() {
    for (let i = 0; i < this.files.length; i++) {
        const tr = document.createElement('tr');
        const td1 = document.createElement('td');
        const td2 = document.createElement('td');
        const td3 = document.createElement('td');

        const img = document.createElement("img");
        const info = document.createElement("span");
        const undoButton = document.createElement('button');

        img.src = URL.createObjectURL(this.files[i]);
        img.height = 60;
        img.onload = () => {
            URL.revokeObjectURL(img.src);
            seleElement.setAttribute("style", "display: none;");
            fileList.setAttribute("class", "none");
            moreFilesBtnContainer.setAttribute("class", "none");
        };

        info.innerHTML = `${this.files[i].name}:${this.files[i].size} bytes`;

        undoButton.textContent = '撤销';
        undoButton.setAttribute('data-name', this.files[i].name);

        undoButton.addEventListener("click", function () {
            const name = this.getAttribute('data-name');
            removeFileFromArray(name);
            tr.parentElement.removeChild(tr);
            updateToUploadFileCount();
        });

        td1.appendChild(img);
        td2.appendChild(info);
        td3.appendChild(undoButton);

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);

        tBody.appendChild(tr);
    }
    updateToUploadFileCount();
}


function removeFileFromArray(name) {
    for (let i = 0; i < fileElem.files.length; i++) {
        let file = fileElem.files[i];
        console.log(fileElem.files);
        console.log(file);
        if (name == file["name"]) {
            const newFiles = Array.from(fileElem.files);
            index = getIndexFromElement(newFiles, file);
            console.log(index);
            newFiles.splice(index, 1);
            const dataTransfer = new DataTransfer();
            newFiles.forEach(function (file) {
                dataTransfer.items.add(file);
                console.log(file);
            });
            fileElem.files = dataTransfer.files;
            console.log(fileElem.files);
        }
    }
}


function getIndexFromElement(array, element) {
    return Array.prototype.indexOf.call(array, element);
}