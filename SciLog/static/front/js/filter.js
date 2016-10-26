var acc = document.getElementById("accordion");

acc.onclick = function(){
    this.nextElementSibling.classList.toggle("show");
}
