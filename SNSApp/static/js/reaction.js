const forms = document.querySelectorAll('.reaction')

forms.forEach(function(form) {
    addEventlistener('submit', async function(event){
        event.preventDefault()

        const formData = new FormData(form)
        formData.append = ('{{ reaction_kind.reaction }}', '{{ reaction_kind.count }}')
        fetch('/posts_list/<int:post_id>/reaction', {
            method : 'POST',
            body: formData
        })
    })
});