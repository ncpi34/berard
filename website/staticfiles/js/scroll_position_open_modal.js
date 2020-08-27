modal_buttons = document.querySelectorAll('.pic_button')

modal_buttons.forEach(button => {
    button.addEventListener("click", () => {
        let scrollLeft = window.pageXOffset || document.documentElement.scrollLeft,
            scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        localStorage.setItem('scrollTop', scrollTop.toString());
    })
})

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