from django.shortcuts import render
import openai, os, requests
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from .models import Image, GeneralQuestion, TranslationQuestion
from .forms import GeneralQuestionForm, TranslationQuestionForm, ImageRequestForm
from django.core import serializers
from django.http import JsonResponse
from sales.utils import generate_code

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", None)

def chatbot_general(request):
    if request.user.profile.language == "Korean":
        instruction = "질문을 입력하세요. (영어로 질문하는 것이 가장 좋습니다.)"
    else:
        instruction = "Write your question in any language for an answer."

    form = GeneralQuestionForm(None)

    context = {
        "instruction": instruction,
        "form": form,
    }
    return render(request, 'tools/openai_general.html', context)

def chatbot_translation(request):
    if request.user.profile.language == "Korean":
        instruction = "번역하고 싶은 문장을 입력하세요."
    else:
        instruction = "Write a statement in any language to translate."

    form = TranslationQuestionForm(None)

    context = {
        "instruction": instruction,
        "form": form,
    }
    return render(request, 'tools/openai_translation.html', context)

def generate_image_from_txt(request):
    if request.user.profile.language == "Korean":
        instruction = "만들어 내고자 하는 이미지를 잘 표현해 보세요."
    else:
        instruction = "Describe what you want as an image to be created."

    form = ImageRequestForm(None)

    context = {
        "instruction": instruction,
        "form": form,
    }
    return render(request, 'tools/openai_image.html', context)

def get_response_for_general(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if api_key is not None and request.method == 'POST':
            openai.api_key = api_key
            user_input = request.POST.get('prompt')
            prompt = user_input
            #prompt = f"translate this text to Spanish: {user_input}"
            #prompt = f"if the question is related to weather - answer it: {user_input}, else say: Can't answer this."

            response = openai.Completion.create(
                engine = 'text-davinci-003',
                prompt = prompt,
                max_tokens = 1024,
                #stop = "."
                #Hello World. How are you? -> 'How are you?' will be ignored
                temperature = 0.5
            )
            chatbot_response = response["choices"][0]["text"]
            obj = GeneralQuestion(None)
            obj.prompt = user_input
            obj.ai_response = chatbot_response
            obj.save()
            return JsonResponse({'data': chatbot_response, 'general_prompt': user_input})
    return JsonResponse({})

def get_response_for_translation(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if api_key is not None and request.method == 'POST':
            openai.api_key = api_key
            user_input = request.POST.get('prompt')
            to_language = request.POST.get('to_language')
            to_other_language = request.POST.get('to_other_language')
            if to_language == "":
                if to_other_language == "":
                    return JsonResponse({})
                else:
                    language = to_other_language
            else:
                language = to_language

            print(type(language))
            #prompt = user_input
            prompt = f"translate to {language}: {user_input}"
            print(prompt)
            #prompt = f"if the question is related to weather - answer it: {user_input}, else say: Can't answer this."

            response = openai.Completion.create(
                engine = 'text-davinci-003',
                prompt = prompt,
                max_tokens = 512,
                #stop = "."
                #Hello World. How are you? -> 'How are you?' will be ignored
                temperature = 0.5
            )
            chatbot_response = response["choices"][0]["text"]
            obj = TranslationQuestion(None)
            obj.prompt = user_input
            obj.ai_response = chatbot_response
            obj.to_language = to_language
            obj.to_other_language = to_other_language
            obj.save()
            return JsonResponse({'data': chatbot_response, 'translation_prompt': user_input})
    return JsonResponse({})

def get_response_for_image(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if api_key is not None and request.method == 'POST':
            openai.api_key = api_key
            user_input = request.POST.get('prompt')
            response = openai.Image.create(
                prompt = user_input,
                size = '512x512' # 512x512 1024x1024
            )
            img_url = response["data"][0]["url"]

            response = requests.get(img_url)
            img_file = ContentFile(response.content)

            count = generate_code()
            fname = f"ai-{count}.jpg"
            obj = Image(prompt=user_input)
            obj.ai_image.save(fname, img_file)
            obj.save()
            image_url = obj.ai_image.url
            image_prompt = obj.prompt
            return JsonResponse({'image_url': image_url, 'image_prompt': image_prompt})
    return JsonResponse({})

    #data = serializers.serialize('json', objects)
    #return JsonResponse({'data':data})


# Create your views here.
def tools_main_view(request):
    return render(request, 'tools/main.html')
