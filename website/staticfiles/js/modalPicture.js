document.addEventListener('DOMContentLoaded', () => {
    //floating
    const elemsBtns = document.querySelectorAll('.modal');
    const floatingBtn = M.FloatingActionButton.init(elemsBtns, {
        direction: 'left',
        hoverEnabled: false
    });

   // onclick event
   document.querySelectorAll(".pic_button").forEach(box =>
   box.addEventListener("click", () =>{
       let modal = document.getElementById("img-modal");
       modal.src= box.id;

       const elemsModal = document.querySelectorAll('.modal');
       const instance = M.Modal.init(elemsModal, {dismissible: true, preventScrolling: true})

       let scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
           scrollTop = window.pageYOffset || document.documentElement.scrollTop;
       localStorage.setItem('scrollTop', scrollTop.toString());
   }
   ))
});

close_modal_picture_button = document.querySelectorAll('.close_modal_picture')
close_modal_picture_button.forEach(button => {
button.addEventListener("click", () => {
let scrollpos = localStorage.getItem('scrollTop');
   if (scrollpos) {
       setTimeout( () => {
           window.scrollTo(0, scrollpos);
       }, 50)

   }  else {
       window.scrollTo(0, 0);
   }
})
})