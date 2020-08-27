document.addEventListener('DOMContentLoaded', function() {
             //floating
             const elemsBtns = document.querySelectorAll('.modal');
             const floatingBtn = M.FloatingActionButton.init(elemsBtns, {
                 direction: 'left',
                 hoverEnabled: false
             });

            // onclick event
            document.querySelectorAll(".pic_button").forEach(box =>
            box.addEventListener("click", () =>{
                let modal = document.getElementById("test");
                modal.src= box.id;
                console.log(box.id);

                const elemsModal = document.querySelectorAll('.modal');
                const instance = M.Modal.init(elemsModal, {dismissible: true, preventScrolling: true})

                //When click on img, you save it on localStorage.
                localStorage.setItem('scrollPosition',window.scrollY);


            }
            ))
        });