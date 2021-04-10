from django.shortcuts import render, redirect

def start_page(request):
    return render(request, 'common/start_page.html')
