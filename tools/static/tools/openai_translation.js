console.log('Hello world, this is OpenAI for translation request.')

const openaiForm = document.getElementById('openai-form')
const openaiPrompt = document.getElementById('id_prompt') // you should find out the name 'id_name' of the element through the console
const openaiLanguage = document.getElementById('id_to_language') // also, the same for 'id_remarks' created by html itself as 'id_name'
const openaiOtherLanguage = document.getElementById('id_to_other_language') // also, the same for 'id_remarks' created by html itself as 'id_name'const openaiOtherLanguage = document.getElementById('div_id_to_other_language') // also, the same for 'id_remarks' created by html itself as 'id_name'
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const spinner = document.getElementById('spinner-box')
const aiTranslationlPrompt = document.getElementById('ai-translation-prompt')
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
    console.log(openaiForm)
    formData.append('to_language', openaiLanguage.value);
    formData.append('to_other_language', openaiOtherLanguage.value);
    spinner.classList.remove('not-visible')

    $.ajax({
        type: 'POST',
        url: '/tools/openai/get-translation/',
        data: formData,
        success: function(response){
            if (response.data != null) {
                const translation_prompt = response.translation_prompt
                aiTranslationlPrompt.innerHTML = `${translation_prompt}<br />`
                const data = response.data.replace(/\r\n/g, '&#13;&#10;')
                aiResponse.innerHTML = `<textarea rows=8 style="width:99%; white-space:pre-wrap">${data}</textarea><br>`
                openaiForm.reset()
            }
            spinner.classList.add('not-visible')
        },
        error: function(error){
            handleAlerts('danger', '...something went wrong!')
        },
        processData: false,
        contentType: false,
    })
})
