console.log('Hello world, this is OpenAI for general question.')

const openaiForm = document.getElementById('openai-form')
const openaiPrompt = document.getElementById('id_prompt') // you should find out the name 'id_name' of the element through the console
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const spinner = document.getElementById('spinner-box')
const aiGeneralPrompt = document.getElementById('ai-general-prompt')
const aiResponse = document.getElementById('ai-response')
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
        url: '/tools/openai/get-general/',
        data: formData,
        success: function(response){
            const general_prompt = response.general_prompt
            aiGeneralPrompt.innerHTML = `${general_prompt}<br />`
            const data = response.data.replace(/\r\n/g, '&#13;&#10;')
            aiResponse.innerHTML = `<textarea rows=8 style="width:99%; white-space:pre-wrap">${data}</textarea><br>`
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
