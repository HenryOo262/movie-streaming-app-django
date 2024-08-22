
/*

const deleteForms = document.querySelectorAll('.deleteForm')

deleteForms.forEach(deleteForm => {
    console.log('ok')
    deleteForm.addEventListener('submit', (event) => {
        event.preventDefault()
        console.log('deleted')
    
        fetch(deleteForm.action, {
            method: 'DELETE',
            body: new FormData(deleteForm),
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        }).then(response => {
            if(response.ok) {
                window.location.reload()
            } else {
                window.location.reload()
            }
        }).catch(error => {
            alert('An unexpected error has occured. Please try again.')
        })
    })
})

*/