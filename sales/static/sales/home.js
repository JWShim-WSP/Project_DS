console.log('Hello world, this is JW.')

const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')
const modalBody = document.getElementById('modal-body')
const reportForm = document.getElementById('report-form')
const reportName = document.getElementById('id_name') // you should find out the name 'id_name' of the element through the console
const reportRemarks = document.getElementById('id_remarks') // also, the same for 'id_remarks' created by html itself as 'id_name'
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertBox = document.getElementById('alert-box')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
       ${msg}
    </div>
    `
}
if (img) {
    reportBtn.classList.remove('not-visible')
}

reportBtn.addEventListener('click', () => {
    // to fit the image into the modal window using Boostrap class attribute 'width 100% of modal-body'
    img.setAttribute('class', 'w-100')
    // use 'prepend' instead of 'append' to put the image on top
    modalBody.prepend(img)

    reportForm.addEventListener('submit', e=>{ // e means 'event' and want to continue with Ajax code
        e.preventDefault()
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrf)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)

        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function(response){
                handleAlerts('success', 'report created successfully')
                reportForm.reset()
            },
            error: function(error){
                handleAlerts('danger', '...something went wrong!')
            },
            processData: false,
            contentType: false,
        })
    })
})