
const modalButton = document.querySelector('#modalButton')
const modal = document.querySelector('#modal')
const modalChild = document.querySelector('#modalChild')

const genreModal = document.querySelector('#genreModal')
const countryModal = document.querySelector('#countryModal')
const homeModal = document.querySelector('#homeModal')

var genres, countries, hidden=true, childHidden=true

document.addEventListener('DOMContentLoaded', searchTermFetch)

document.addEventListener('click', handleClickOutside);

modalButton.addEventListener('click', () => {
    hidden===true?modal.classList.add('show-modal'):modal.classList.remove('show-modal')
    childHidden==false?modalChild.classList.remove('show-modal'):void 0
    hidden = !hidden
})

genreModal.addEventListener('mouseover', () => {
    modalChild.classList.add('show-modal')
    populateModalChild(genres, 'genre')
    childHidden = false
})

countryModal.addEventListener('mouseover', () => {
    modalChild.classList.add('show-modal')
    populateModalChild(countries, 'country')
    childHidden = false
})

function searchTermFetch() {
    fetch('/searchTerms/').then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        genres = data.genres
        countries = data.countries
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function populateModalChild(items, searchTerm) {
    modalChild.innerHTML = ''
    items.forEach(item => {
        const a = document.createElement('a')
        a.href = `${window.location.origin}/search/${searchTerm}/${item}`
        a.innerText = `${item}`
        modalChild.appendChild(a)
    })
}

function handleClickOutside(event) {
    if (!modal.contains(event.target) && !modalButton.contains(event.target) && !modalChild.contains(event.target)) {
        modal.classList.remove('show-modal')
        modalChild.classList.remove('show-modal')
    }
}
