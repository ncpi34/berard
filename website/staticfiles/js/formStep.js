document.addEventListener("DOMContentLoaded", () => { 
    console.log('zeubiiii')
    let hidden_groups = document.querySelectorAll('.hidden_groups')
    
    // quantities form step
    let multiples = document.querySelectorAll('.product_multiples')
    let multiples_display = document.querySelectorAll('.quantity_val')
    console.log('zeubiiii')

    // Insert After
    const insertAfter = (referenceNode, newNode) => {
        referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
    }

    // Insert Before
    const insertBefore = (newNode, existingNode) => {
        existingNode.parentNode.insertBefore(newNode, existingNode);
    }
    // set Time Out
    const debounce = (callback, wait) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => { callback.apply(this, args) }, wait);
        };
      }
      
    
    if(multiples &&  multiples_display){
        for (let i=0; i< multiples.length; i++) {
            if (hidden_groups[i].value === 'BOISSONS') { // only for products with group=BOISSONS
                if(!isNaN(parseInt(multiples[i].innerHTML))) {
                    multiples_display[i].step = multiples[i].innerHTML
                    multiples_display[i].addEventListener('input', debounce(() => {
                        console.log('movement!!!')
                        let value_onchange = multiples_display[i];
                        let multiple_expected = multiples[i].innerHTML;
                        // round result
                        if (value_onchange.value % multiple_expected !== 0) {
                            let result_to_display = Math.round(value_onchange.value / multiple_expected) * multiple_expected
    
                            value_onchange.value = result_to_display 
                            // create error display
                            if(value_onchange.value == 0) {
                                let p = document.createElement('p')
                                p.innerHTML = "Veuillez ajouter un minimum de " +  multiple_expected
                                p.style.color = 'red'
                                
                                insertBefore(p, value_onchange.parentNode)
                                setTimeout( () => {
                                    p.style.display = 'none'
                                }, 3000)
                            
                                // insertAfter(value_onchange, p);
                            }
                        }
                        
                        
                    }, 400))
                }
            }     
        }
    }
  
    

});


