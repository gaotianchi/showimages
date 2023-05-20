const messages = document.getElementsByClassName('flash-message');


function initFlash() {
    Array.from(messages).forEach(function(message) {
      
        setTimeout(function() {
          message.parentElement.removeChild(message);
        }, 5000);
      });
}


document.addEventListener("DOMContentLoaded", () => {
    initFlash();
})
