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
        });

        td1.appendChild(img);
        td2.appendChild(info);
        td3.appendChild(undoButton);

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);

        tBody.appendChild(tr);
    }
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