document.addEventListener("readystatechange", () => { 
    let groups_url = document.querySelectorAll('.groups_url')
    
    if (groups_url) {
        groups_url.forEach(group => {
            group.addEventListener('click', () => {
                localStorage.setItem('scrollpos', "0");
            })
        })
    }
   
       
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, scrollpos);

     // onclick event
   document.querySelectorAll(".btn_send").forEach(box =>
    box.addEventListener("click", () =>{

        let scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
            scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        localStorage.setItem('scrollpos', scrollTop.toString());
    }
    ))
  

});
