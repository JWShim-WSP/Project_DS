from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def Calculator(request):
    return render(request, 'calculator/calculator.html')

def SubmitQuery(request):
    query = request.GET["query"]
    try: 
        answer = eval(query)
        if (type(answer) == int):
            answer = '{:,}'.format(answer)
        elif (type(answer) != str):
            answer = '{:,.4f}'.format(answer)
        error = False
    except:
        answer = ""
        error = True

    return render(request, "calculator/calculator.html", {
            "query": query,
            "answer": answer,
            "error": error,
        })

    