document.addEventListener('DOMContentLoaded', function () {

    const clickable = document.querySelectorAll('.halaqa_link')
    clickable.forEach(element => {
        element.addEventListener('click', function () {
            window.location.href = `halaqaat/${element.id}`
        });
    })

})