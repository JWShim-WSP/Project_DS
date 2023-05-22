console.log('Hello world, this is JW.')

const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')
const Body = document.getElementById('modal-body')
const reportForm = document.getElementById('report-form')
const alertBox = document.getElementById('alert-box')

const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

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
    console.log('clicked')
    // to fit the image into the modal window
    img.setAttribute('class', 'w-100')
    // use 'prepend' instead of 'append' to put the image on top
    modalBody.prepend(img)

    reportForm.addEventListener('submit', e=>{
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
                console.log(response)
                handleAlerts('success', 'report created successfully')
                reportForm.reset()
            },
            error: function(error){
                console.log(error)
                handleAlerts('danger', '...something went wrong!')
            },
            processData: false,
            contentType: false,
        })
    })
})