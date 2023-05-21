// :author: 高天驰
// :copyright: © 2023 高天驰 <6159984@gmail.com>

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
                let nextNodeSrc = nextNode.querySelector("img").src;                return {
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
    () => {
        let bigImageSrc = bigImage.src;
        let items = findSmallImageContainerNode(bigImageSrc);
        bigImage.src = items.nextNodeSrc;
        items.targetNode.parentElement.removeChild(items.targetNode);
    }
)
