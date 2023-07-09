from django.shortcuts import render
import openai, os, requests
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from .models import Image
from .forms import GeneralQuestionForm, TranslationRequestForm, ImageRequestForm

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", None)

def chatbot_general(request):
    chatbot_response = None

    if request.user.profile.language == "Korean":
        instruction = "질문을 입력하세요. (영어로 질문하는 것이 가장 좋습니다.)"
    else:
        instruction = "Write your question in any language for an answer."

    form = GeneralQuestionForm()

    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('Prompt')
        prompt = user_input
        #prompt = f"translate this text to Spanish: {user_input}"
        #prompt = f"if the question is related to weather - answer it: {user_input}, else say: Can't answer this."

        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = prompt,
            max_tokens = 256,
            #stop = "."
            #Hello World. How are you? -> 'How are you?' will be ignored
            temperature = 0.5
        )
        chatbot_response = response["choices"][0]["text"]

    context = {
        "instruction": instruction,
        "response": chatbot_response,
        "form": form,
    }
    return render(request, 'tools/openai.html', context)

def chatbot_translation(request):
    chatbot_response = None
    if request.user.profile.language == "Korean":
        instruction = "번역하고 싶은 문장을 입력하세요"
    else:
        instruction = "Write a statement in any language to translate."

    form = TranslationRequestForm()

    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('Prompt')
        language = request.POST.get('To_language')
        #prompt = user_input
        prompt = f"translate to {language}: {user_input}"
        #prompt = f"if the question is related to weather - answer it: {user_input}, else say: Can't answer this."

        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = prompt,
            max_tokens = 256,
            #stop = "."
            #Hello World. How are you? -> 'How are you?' will be ignored
            temperature = 0.5
        )
        chatbot_response = response["choices"][0]["text"]

    context = {
        "instruction": instruction,
        "response": chatbot_response,
        "form": form
    }
    return render(request, 'tools/openai.html', context)

def generate_image_from_txt(request):
    obj = None
    if request.user.profile.language == "Korean":
        instruction = "만들어 내고자 하는 이미지를 잘 표현해 보세요."
    else:
        instruction = "Describe what you want as an image to be created."

    form = ImageRequestForm()

    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('Prompt')
        response = openai.Image.create(
            prompt = user_input,
            size = '256x256' # 512x512 1024x1024
        )
        img_url = response["data"][0]["url"]

        response = requests.get(img_url)
        img_file = ContentFile(response.content)

        count = Image.objects.count() + 1
        fname = f"image-{count}.jpg"
        obj = Image(phrase=user_input)
        obj.ai_image.save(fname, img_file)
        obj.save()

    context = {
        "instruction": instruction,
        "image": obj,
        "form": form
    }
    return render(request, 'tools/openai.html', context)

# Create your views here.
def tools_main_view(request):
    return render(request, 'tools/main.html')
