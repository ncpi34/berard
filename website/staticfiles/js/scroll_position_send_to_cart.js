let btns_send_to_cart = document.querySelectorAll('.btn_send')
if (btns_send_to_cart) {
    for (btn in btns_send_to_cart) {
        btn.addEventListener('click', () => {
            localStorage.setItem('scrollpos', window.scrollY);
        })
    }
}  
document.addEventListener("DOMContentLoaded", () => { 
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, scrollpos);

     
  

});


// window.onbeforeunload = function(e) {
//     localStorage.setItem('scrollpos', window.scrollY);
// };
