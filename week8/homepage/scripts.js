document.addEventListener('DOMContentLoaded',function(){
    document.getElementById('main-title').addEventListener('click', function(){
        this.textContent = 'Everything We Know';
    })

    const poster = document.getElementById("poster");
    poster.addEventListener("mouseover", () => {
        poster.style.transform = "scale(1.1)";
        poster.style.transition = "0.3s";
    });
        poster.addEventListener("mouseout", () => {
        poster.style.transform = "scale(1)";
    });
})

