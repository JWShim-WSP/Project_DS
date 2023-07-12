console.log('Hello world, this is OpenAI.')

const openaiForm = document.getElementById('openai-form')
const openaiPrompt = document.getElementById('id_prompt') // you should find out the name 'id_name' of the element through the console
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const spinner = document.getElementById('spinner-box')
const aiImagePrompt = document.getElementById('ai-image-prompt')
const aiImage = document.getElementById('ai-image')
const alertBox = document.getElementById('alert-box')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
       ${msg}
    </div>
    `
}

openaiForm.addEventListener('submit', e=>{ // e means 'event' and want to continue with Ajax code
    e.preventDefault()
    const formData = new FormData()
    formData.append('csrfmiddlewaretoken', csrf)
    formData.append('prompt', openaiPrompt.value)
    spinner.classList.remove('not-visible')

    $.ajax({
        type: 'POST',
        url: '/tools/openai/get-image/',
        data: formData,
        success: function(response){
            const image_url = response.image_url
            const image_prompt = response.image_prompt
            aiImagePrompt.innerHTML = `${image_prompt}<br />`
            aiImage.innerHTML = `<img src="${image_url}" alt="${image_prompt}">`
            spinner.classList.add('not-visible')
            openaiForm.reset()
        },
        error: function(error){
            handleAlerts('danger', '...something went wrong!')
        },
        processData: false,
        contentType: false,
    })
})
