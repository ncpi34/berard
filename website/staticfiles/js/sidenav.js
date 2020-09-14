   // sideNavs animation
   document.addEventListener('DOMContentLoaded', function() {
    //   NAVBAR
    let elem = document.querySelector('#nav-mobile');
    let instance = M.Sidenav.init(elem, {
        menuWidth: 300, // Default is 300
        edge: 'right', // Choose the horizontal origin
        closeOnClick: false, // Closes side-nav on <a> clicks, useful for Angular/Meteor
        draggable: true // Choose whether you can drag to open on touch screens
    });

    // SIDENAV
    let elems = document.querySelector('#sidenav-mobile');
    let instances = M.Sidenav.init(elems, {
        menuWidth: 300, // Default is 300
        edge: 'left', // Choose the horizontal origin
        closeOnClick: false, // Closes side-nav on <a> clicks, useful for Angular/Meteor
        draggable: true // Choose whether you can drag to open on touch screens
    });
    //navBar animation
    let prevScrollpos = window.pageYOffset;
    window.onscroll = function() {
    let currentScrollPos = window.pageYOffset;
    let navbar = document.getElementById("navbar")
      if (prevScrollpos > currentScrollPos) {
        navbar.style.top = "0";
      } else {
        navbar.style.top = "-60px";
      }
      prevScrollpos = currentScrollPos;
    }

    // // animation searchbar
    //  let iconclose = document.querySelector('#close_icon')
    // const searchBar = document.querySelector('#search_icon');
    // searchBar.addEventListener('click',  () => {
    //     let searchbar = document.querySelector('#search')
    //     searchbar.classList.toggle("searchbar");
    //     searchbar.focus();
    //
    //
    //    let iconsearch = document.querySelector('#search_icon')
    //     iconsearch.classList.toggle("search_icon");
    //
    //
    //     iconclose.classList.toggle("close_icon");
    //
    // })
    // iconclose.addEventListener('click', ()=> {
    //     let searchbar = document.querySelector('#search')
    //     searchbar.value = ''
    //     searchbar.classList.toggle("searchbar");
    //
    //    let iconsearch = document.querySelector('#search_icon')
    //     iconsearch.classList.toggle("search_icon");
    //
    //
    //     iconclose.classList.toggle("close_icon");
    // })
});
 const submitSearch = () => {
        if (document.querySelector('#search_form')) {
            let form = document.querySelector('#search_form')
            form.submit()
        }
    }
    const debounce = (callback, wait) => {
      let timeout;
      return (...args) => {
          clearTimeout(timeout);
          timeout = setTimeout(() => { callback.apply(this, args) }, wait);
      };
    }

    let search = document.querySelector('#search')
    if (search) {
        search.addEventListener('keyup', debounce( () => {
            // code you would like to run 1000ms after the keyup event has stopped firing
            // further keyup events reset the timer, as expected
            let form = document.querySelector('#search_form')
            form.submit()
        }, 1000))
    }

