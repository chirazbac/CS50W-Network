
    document.addEventListener('DOMContentLoaded', function() {
    function editPost(postId) {

        const contentElement = document.getElementById(`content-${postId}`);
        const originalContent = contentElement.textContent;
        contentElement.innerHTML = `
                    <textarea id="textarea-${postId}" rows="2" cols="100">${originalContent}</textarea>
                    <br>
                    <button id="save-${postId}" class="btn btn-primary">Save</button>
                `;
        document.getElementById(`edit-${postId}`).style.display = "none";

        document.getElementById(`save-${postId}`).addEventListener('click', function() {
            const newContent = document.getElementById(`textarea-${postId}`).value;
            savePost(postId, newContent);
        });

    }

    function savePost(postId, newContent) {
            fetch(`/edit/${postId}`, {
            method: 'POST',
            body: JSON.stringify({
            content: newContent
        }),
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
        })
            .then(response => response.json())
            .then(data => {
            console.log(data)
            document.getElementById(`content-${postId}`).textContent = newContent;
            document.getElementById(`edit-${postId}`).style.display = "block";

        });
   }
    function likePost(postId) {
    const heartIcon = document.getElementById(`like-${postId}`);
    const liked = heartIcon.classList.contains('fas');

    if (liked) {
            fetch(`/removeLike/${postId}`)
            .then(response => response.json())
            .then(data => {
            console.log(data);
            heartIcon.classList.remove('fas');
            heartIcon.classList.add('far');
            heartIcon.style.color = 'black';
            document.getElementById(`like-count-${postId}`).innerHTML = data.likedCount; // Update like count
        })
        } else {
            fetch(`/addLike/${postId}`)
            .then(response => response.json())
            .then(data => {
            console.log(data);
            heartIcon.classList.remove('far');
            heartIcon.classList.add('fas');
            heartIcon.style.color = 'red';
            document.getElementById(`like-count-${postId}`).innerHTML = data.likedCount; // Update like count
        })
        }
    }
    document.querySelectorAll('.edit-link').forEach(function(editLink) {
    editLink.addEventListener('click', function(event) {
    const postId = this.dataset.postId;
    editPost(postId);
        });
    });

    document.querySelectorAll('.fa-heart').forEach(function(likeIcon) {
    likeIcon.addEventListener('click', function() {
    const postId = this.dataset.postId;
    likePost(postId);
        });
    });

   });


