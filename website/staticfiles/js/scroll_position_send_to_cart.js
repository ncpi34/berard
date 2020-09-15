document.addEventListener("DOMContentLoaded", () => { 
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, scrollpos);

     
  

});


window.onbeforeunload = function(e) {
    localStorage.setItem('scrollpos', window.scrollY);
};
