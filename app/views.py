from django.shortcuts import render
from app.utils.index import menu
from django.contrib.auth.decorators import login_required


@login_required(login_url='/admin')
def report(requests):

    return render(requests, 'report.html', {'side_menu_list': menu})
