
const modalButton = document.getElementById('modalButton')
const modal = document.getElementById('modal')
const modalChild = document.getElementById('modalChild')

const genreModal = document.getElementById('genreModal')
const countryModal = document.getElementById('countryModal')
const homeModal = document.getElementById('homeModal')

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
        const div = document.createElement('div')
        div.innerHTML = `<a href="../search/${searchTerm}/${item}">${item}</a>`
        modalChild.appendChild(div)
    })
}

function handleClickOutside(event) {
    if (!modal.contains(event.target) && !modalButton.contains(event.target) && !modalChild.contains(event.target)) {
        modal.classList.remove('show-modal')
        modalChild.classList.remove('show-modal')
    }
}
