// UPDATE USER
 const getUpdateUserForm = async (url) => {
       let req = await fetch(url)
       let rsp = await req.text();

        return rsp
    }

const closeModal = (modal, alerte) => {
        setTimeout( () => {
            // full js
            // get the key under which the modal's methods are stored.
            let jQueryObj = Object.keys(modal).filter((key) => (key.toString().indexOf('jQuery') !== -1) && modal[key].hasOwnProperty('bs.modal'));
            // ... and close the modal!
            if(modal[jQueryObj]) {
                modal[jQueryObj]['bs.modal'].hide();
                alerte.style.display = 'none'
            }

        }, 2000)
    }
    const getResult = (xhr) => {
        const alerte = document.querySelector('#update_user_alert')
        const modal = document.querySelector('#updateProfileModal')

        xhr.onreadystatechange = async () => {
            if (xhr.status === 200) {
                alerte.style.display = 'block'
                alerte.className ='alert alert-success'
                alerte.innerHTML = xhr.response
                modal.scrollTo(0, 0);
                closeModal(modal, alerte)

            } else {
                alerte.style.display = 'block'
                alerte.classList.add('alert-danger')
                alerte.innerHTML = xhr.response
                modal.scrollTo(0, 0);
            }
        }

    }

    //Check forms
    const CheckForms = () => {
        let email = document.getElementById("id_email");
        let last_name = document.getElementById("id_last_name");
        let first_name = document.getElementById("id_first_name");
        let errors = document.getElementById("update_user_errors")
          if (!email.checkValidity() && last_name.checkValidity() && first_name.checkValidity()) {
              return true
          }
          errors.innerHTML = ""
    }
     // Fetch request to Update User
    const UpdateUser = async (button) => {

        let check = await CheckForms();

        if(!check){
            const Form = document.getElementById("update_user_form");
        let form = await new FormData()

        for (let i=0; i<Form.length; i++){
            if(Form[i].name.length !==0 && Form[i].name !== 'csrfmiddlewaretoken'){
                await form.append(Form[i].name, Form[i].value)
            }

        }
            let xhr = new XMLHttpRequest();
            await xhr.open("POST", button.dataset.url);
            await xhr.setRequestHeader("X-CSRFToken", Form[0].value)
            await xhr.send(form);
            await getResult(xhr, Form);
        }
    }


// LOGIN !!!
    const getLoginForm = async (butt) => {
       let req = await fetch(butt)
       let rsp = await req.text();

        return rsp
    }

    const closeModalLogin = (modal, login_alert, url_redirect) => {
        setTimeout( () => {
            // full js
            // get the key under which the modal's methods are stored.
            let jQueryObj = Object.keys(modal).filter((key) => (key.toString().indexOf('jQuery') !== -1) && modal[key].hasOwnProperty('bs.modal'));
            if(modal[jQueryObj]) {
                // ... and close the modal!
                modal[jQueryObj]['bs.modal'].hide();
                login_alert.style.display = 'none'
            }
            window.location.href = url_redirect


        }, 2000)
    }
    const getResultLogin = (xhr) => {
        const login_alert = document.querySelector('#login_alert')
        const modal = document.querySelector('#loginModal')

        xhr.onreadystatechange = async () => {
            if (xhr.status === 200) {
                let response = xhr.response.split(',')
                login_alert.style.display = 'block'
                login_alert.className = 'alert alert-success'
                login_alert.innerHTML = response[0]
                modal.scrollTo(0, 0);

                closeModalLogin(modal, login_alert, response[1])

            } else {
                login_alert.style.display = 'block'
                login_alert.classList.add('alert-danger')
                login_alert.innerHTML = xhr.response
                modal.scrollTo(0, 0);
                setTimeout(()=> {
                    login_alert.style.display ='none'
                }, 3000)
            }
        }

    }

    //Check forms
    const CheckFormsLogin = () => {
        let username = document.getElementById("id_username");

          if (!username.checkValidity()) {
              return true
          }

    }
     // Fetch request to Update User
    const Login = async (button) => {

        let check = await CheckFormsLogin();

        if(!check){
            const Form = document.getElementById("login_form");
            let form = await new FormData()
            for (let i=0; i<Form.length; i++){
                if(Form[i].name.length !==0 && Form[i].name !== 'csrfmiddlewaretoken'){
                    await form.append(Form[i].name, Form[i].value)
                }

            }
            let xhr = new XMLHttpRequest();
            await xhr.open("POST", button.dataset.url);
            await xhr.setRequestHeader("X-CSRFToken", Form[0].value)
            await xhr.send(form);
            await getResultLogin(xhr, Form);
        }
    }


// FORGOT PASSWORD !!!

const getForgotPasswordForm = async (butt) => {
       let req = await fetch(butt)
       let rsp = await req.text();

        return rsp
    }

const closeModalForgotPassword = (modal, forgot_pass_alert) => {
        setTimeout( () => {
            // full js
            // get the key under which the modal's methods are stored.
            let jQueryObj = Object.keys(modal).filter((key) => (key.toString().indexOf('jQuery') !== -1) && modal[key].hasOwnProperty('bs.modal'));
            // ... and close the modal!
            if(modal[jQueryObj]) {
                modal[jQueryObj]['bs.modal'].hide();
                forgot_pass_alert.style.display = 'none'
            }

        }, 2000)
    }
    const getResultForgotPassword = (xhr) => {
        const forgot_pass_alert = document.querySelector('#forgot_pass_alert')
        const modal = document.querySelector('#forgotPassModal')

        xhr.onreadystatechange = async () => {
            if (xhr.status === 200) {
                forgot_pass_alert.style.display = 'block'
                forgot_pass_alert.className = 'alert alert-success'
                forgot_pass_alert.innerHTML = xhr.response
                modal.scrollTo(0, 0);

                closeModalForgotPassword(modal, forgot_pass_alert)

            } else {
                forgot_pass_alert.style.display = 'block'
                forgot_pass_alert.classList.add('alert-danger')
                forgot_pass_alert.innerHTML = xhr.response
                modal.scrollTo(0, 0);
            }
        }

    }

    //Check forms
    const CheckFormsForgotPassword = () => {
        let email = document.getElementById("forgot_pass_email");

          if (!email.checkValidity()) {
              return true
          }

    }
     // Fetch request to Update User
    const ForgotPassword = async (button) => {

        let check = await CheckFormsForgotPassword();

        if(!check){
            const Form = document.getElementById("forgot_password_form");
            let form = await new FormData()
            for (let i=0; i<Form.length; i++){
                if(Form[i].name.length !==0 && Form[i].name !== 'csrfmiddlewaretoken'){
                    await form.append(Form[i].name, Form[i].value)
                }

            }
            let xhr = new XMLHttpRequest();
            await xhr.open("POST", button.dataset.url);
            await xhr.setRequestHeader("X-CSRFToken", Form[0].value)
            await xhr.send(form);
            await getResultForgotPassword(xhr, Form);
        }
    }
