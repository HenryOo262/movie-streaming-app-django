const genresCell = document.querySelector('#genres-cell')
const countriesCell = document.querySelector('#countries-cell')
const genresButton = document.querySelector('#genres-button')
const countriesButton = document.querySelector('#countries-button')

var showGenres = false
var showCountries = false

document.addEventListener('DOMContentLoaded', () => {
    genresCell.classList.add('hidden')
    countriesCell.classList.add('hidden')
})

genresButton.addEventListener('click', (event) => {
    event.preventDefault()
    showGenres = !showGenres
    cellOperation(genresCell, showGenres, genresButton, 'Genres')
})

countriesButton.addEventListener('click', (event) => {
    event.preventDefault()
    showCountries = !showCountries
    cellOperation(countriesCell, showCountries, countriesButton, 'Countries')
})

function cellOperation(cell, flag, button, string) {
    if(flag) {
        cell.classList.remove('hidden')
        button.textContent = `Hide ${string}`
    } else {
        cell.classList.add('hidden')
        button.textContent = `Show ${string}`
    }
}