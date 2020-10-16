document.addEventListener('DOMContentLoaded', () => {
    let img = document.querySelectorAll('.img_modal')
      if(img) {
        img.forEach(i => {
          let ratio = i.clientHeight /i.clientWidth
          if (ratio > 2) {
            i.style.width = '15%';
          }  else {
            i.classList.add('w-50')     
          }
        })
      }
})