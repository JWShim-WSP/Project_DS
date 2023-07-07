from django.shortcuts import render
import openai, os, requests
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from .models import Image

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", None)

def chatbot(request):
    chatbot_response = None
    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('user_input')
        #prompt = user_input
        #prompt = f"translate this text to Spanish: {user_input}"
        prompt = f"if the question is related to weather - answer it: {user_input}, else say: Can't answer this."

        response = openai.Completion.create(
            engine = 'text-davinci-003',
            prompt = prompt,
            max_tokens = 256,
            #stop = "."
            #Hello World. How are you? -> 'How are you?' will be ignored
            temperature = 0.5
        )
        chatbot_response = response["choices"][0]["text"]

    return render(request, 'tools/chatbot.html', {"response": chatbot_response})

def generate_image_from_txt(request):
    obj = None
    if api_key is not None and request.method == 'POST':
        openai.api_key = api_key
        user_input = request.POST.get('user_input')
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

    return render(request, 'tools/chatbot.html', {'image': obj})

# Create your views here.
def tools_main_view(request):
    return render(request, 'tools/main.html')
