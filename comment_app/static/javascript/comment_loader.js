
var page = 1  // load the second page for the first load
var user_id

const loader = document.querySelector('#loader')
const comments = document.querySelector('#comments')
const loadmore = comments.lastElementChild

try {
    user_id = parseInt(JSON.parse(document.getElementById('user_id').textContent))
} catch(Exception) {
    user_id = null
} 

loader.addEventListener('click', (event) => {
    event.preventDefault()

    fetch(`${loader.href}?page=${page}`).then(response => {
        if (!response.ok) {
            throw new Error('Network error. Cannot load more comments.');
        }
        page += 1
        return response.json()
    })
    .then(data => {
        // If no more new comments to be fetched
        if(!data.hasNext) {
            const noComment = document.createElement('p')
            if(page === 2 && data.comments.length === 0) {
            // After init load, no comments and no next
                noComment.textContent = 'Be The First One To Comment 😆 !!!' 
            } else if(page === 2 && data.comments.length !== 0) {
            // After init load, comments and no next
                noComment.textContent = 'No More Comments 😔'
            } else if (page !== 2) {
            // After normal load, no next
                noComment.textContent = 'No More Comments 😔'
            }
            loader.replaceWith(noComment)
        }

        fetch_comments = data.comments
        fetch_comments.forEach(comment => {
            commentMaker(comment)
        });
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
})

document.addEventListener('DOMContentLoaded', () => {
    // Perform init load on page load, page = 1
    loader.click()
})

function commentMaker(comment) {
    const commentDiv = document.createElement('div')
    commentDiv.id = 'comment'
    commentDiv.className = 'comment'

    const username = document.createElement('p')
    username.className = 'green'
    username.innerText = comment.userName + ' : '
    commentDiv.appendChild(username)
    
    const commentText = document.createElement('p')
    commentText.innerText = comment.commentText
    commentDiv.appendChild(commentText)

    const addedDateTime = document.createElement('p')
    addedDateTime.className = 'green'
    const localDateTime = new Date(comment.addedDateTime).toLocaleString()
    addedDateTime.innerText = localDateTime
    commentDiv.appendChild(addedDateTime)

    if(comment.userId == user_id) {
        // Delete
        const form = document.createElement('form');
        form.className = 'comment-operation deleteForm';
        form.action = `${window.location.origin}/comments/${comment.commentId}/delete/`; 
        form.method = 'POST';

        form.addEventListener('submit', (event) => {
            event.preventDefault()
        
            fetch(form.action, {
                method: 'DELETE',
                body: new FormData(form),
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

        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = document.querySelector('[name=csrfmiddlewaretoken]').value 
        form.appendChild(csrfInput);

        const deleteButton = document.createElement('button');
        deleteButton.id = 'delete';
        deleteButton.className = 'delete';
        deleteButton.onclick = function () {
            return confirm('Are you sure you want to do this?');
        };

        deleteButton.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#ffffff">
            <path d="M312-144q-29.7 0-50.85-21.15Q240-186.3 240-216v-480h-48v-72h192v-48h192v48h192v72h-48v479.57Q720-186 698.85-165T648-144H312Zm336-552H312v480h336v-480ZM384-288h72v-336h-72v336Zm120 0h72v-336h-72v336ZM312-696v480-480Z"/>
        </svg>`;
        form.appendChild(deleteButton);
        commentDiv.appendChild(form);

        // Edit
        const edit = document.createElement('a')
        edit.className = 'edit'
        edit.onclick = function () {
            callEditText(comment.commentText);
            setCommentId(comment.commentId);
        };
        edit.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#ffffff">
            <path d="M216-216h51l375-375-51-51-375 375v51Zm-72 72v-153l498-498q11-11 23.84-16 12.83-5 27-5 14.16 0 27.16 5t24 16l51 51q11 11 16 24t5 26.54q0 14.45-5.02 27.54T795-642L297-144H144Zm600-549-51-51 51 51Zm-127.95 76.95L591-642l51 51-25.95-25.05Z"/>
        </svg>`
        commentDiv.appendChild(edit)
    }

    comments.insertBefore(commentDiv, loadmore)
}