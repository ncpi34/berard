document.addEventListener("DOMContentLoaded", function(event) {
            var scrollpos = localStorage.getItem('scrollpos');
            if (scrollpos) window.scrollTo(0, scrollpos);
        });

        window.onbeforeunload = function(e) {
            localStorage.setItem('scrollpos', window.scrollY);
        };



// define container
var redips = {};

// append scroll parameter to URL or return scroll value
redips.scroll = function (url) {
    let scroll, q;
    // DOM compliant
    if (document.body && document.body.scrollTop) {
        scroll = document.body.scrollTop;
    }
    // old - Netscape compliant
    else if (typeof (window.pageYOffset) === 'number') {
        scroll = window.pageYOffset;
    }
    // very very old - IE6 standards compliant mode
    else if (document.documentElement && document.documentElement.scrollTop) {
        scroll = document.documentElement.scrollTop;
    }
    // when vertical scroll bar is on the top
    else {
        scroll = 0;
    }
    // if input parameter does not exist then return scroll value
    if (url === undefined) {
        return scroll;
    }
    // else append scroll parameter to URL
    else {
        // set "?" or "&" before scroll parameter
        q = url.indexOf('?') === -1 ? '?' : '&';
        // load page with scroll position parameter
        window.location.href = url + q + 'scroll=' + scroll;
    }
};

// set scroll position if URL contains scroll=nnn parameter
redips.setScrollOnLoad = function () {
    // get query string parameter with "?"
    let search = window.location.search,
        matches;
    // if query string exists
    if (search) {
        // find scroll parameter in query string
        matches = /scroll=(\d+)/.exec(search);
        // jump to scroll position if scroll parameter exists
        if (matches) {
            window.scrollTo(0, matches[1]);
        }
    }
};

// add onload event listener
if (window.addEventListener) {
    window.addEventListener('load', redips.setScrollOnLoad, false);
}
else if (window.attachEvent) {
    window.attachEvent('onload', redips.setScrollOnLoad);
}