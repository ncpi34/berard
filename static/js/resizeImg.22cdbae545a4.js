document.addEventListener('DOMContentLoaded', () => {
    let img = document.querySelectorAll('.img_modal')
      if(img) {
        img.forEach(i => {
          let ratio = i.clientHeight /i.clientWidth
          if (ratio > 2) {
            i.style.width = '12%';
          }  else {
            i.style.width = '35%';
          }
        })
      }
})