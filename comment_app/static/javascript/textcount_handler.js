
/* Handles Text Count and Comment Edit */

const max = 280

const comment = document.querySelector('#id_commentText')
const editModal = document.querySelector('#editModal')
const edit = document.querySelector('#id_editText')
const commentId = document.querySelector('#id_commentId')
const counter1 = document.querySelector('#counter1')
const counter2 = document.querySelector('#counter2')

document.addEventListener('DOMContentLoaded', () => {
    comment.value = ''
    edit.value = ''

    counter1.textContent = String(comment.value.length) + '/' + 280
    counter2.textContent = String(edit.value.length) + '/' + 280
    checkCounter(comment, counter1)
    checkCounter(edit, counter2)

    editModal.classList.add('hidden')
})

comment.addEventListener('input', () => {
    checkCounter(comment, counter1)
})

edit.addEventListener('input', () => {
    checkCounter(edit, counter2)
})

function checkCounter(input, counter) {
    counter.textContent = String(input.value.length) + '/' + 280

    if(input.value.length > 280) {
        counter.style.color = 'red'
    } else if(input.value.length === 280) {
        counter.style.color = 'yellow'
    } else {
        counter.style.color = 'white'
    }
}

function callEditText(inputText) {
    // Remove Linebreaks
    // inputText = inputText.replace(/(\r\n|\n|\r)/gm, "");
    edit.value = inputText

    // Set The Word Counter of Modal
    checkCounter(edit, counter2)

    // Create The Overlay That Will Prevent Clicks Outside Modal
    var overlay = document.createElement('div');
    overlay.className = 'editModalOverlay';
    overlay.id = 'editModalOverlay';

    // Insert As The First Child Of Body
    document.body.insertBefore(overlay, document.body.firstChild);

    // Show Modal
    editModal.classList.remove('hidden')
}

function uncallEditText() {
    // Remove Overlay
    document.querySelector('#editModalOverlay').remove()

    // Hide Modal
    editModal.classList.add('hidden')
}

function setCommentId(inputCommentId) { 
    // Add CommentID To Form Field
    commentId.value = parseInt(inputCommentId)
}