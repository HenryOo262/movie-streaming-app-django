
const createForm = document.querySelector('#createForm')
const editForm = document.querySelector('#editForm')

createForm.addEventListener('submit', (event) => {
    event.preventDefault()
    fetch(createForm.action, {
        method: 'POST',
        body: new FormData(createForm),
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

editForm.addEventListener('submit', (event) => {
    event.preventDefault()
    fetch(editForm.action, {
        method: 'POST',
        body: new FormData(editForm),
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