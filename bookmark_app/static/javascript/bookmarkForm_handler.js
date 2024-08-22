
const bookmarkForm = document.querySelector('#bookmarkForm')

bookmarkForm.addEventListener('submit', (event) => {
    console.log(event)
    event.preventDefault()

    fetch(bookmarkForm.action, {
        method: 'POST',
        body: new FormData(bookmarkForm),
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