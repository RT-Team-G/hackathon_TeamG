const forms = document.querySelectorAll('.reaction')

forms.forEach(function(form) {
    addEventlistener(
        'submit', async function(event){
            event.preventDefault();

            const formData = new FormData(form);
            formData.append('reaction_id', event.submitter.value);
            const response =
            await fetch(
                form.action, {
                method : 'POST',
                body: formData
                }
            )
            const data = await response.json();
            console.log(data)
        }
    )
});