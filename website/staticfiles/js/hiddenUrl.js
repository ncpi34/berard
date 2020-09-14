// to insert path in hidden form
        let btn_send = document.querySelectorAll('.btn_send');
        let hidd_url = document.querySelectorAll('.hidden_url');
        if (btn_send && hidd_url) {
          for (const button of btn_send) {
            button.addEventListener('click', (event)=> {
                hidd_url.forEach(val => {
                    val.value=window.location.href;
                    // val.value=window.location.pathname;
                })
            })
  
          }

        }