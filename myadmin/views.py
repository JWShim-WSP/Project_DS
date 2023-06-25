from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, FormView
from profiles.models import Profile
from .forms import MemberForm, NewMemberForm
from profiles.forms import FormatForm
from profiles.resources import MemberResource
from django.core.paginator import Paginator

# Create your views here.

@staff_member_required
def member_list_view(request):
    if (request.method == 'POST'):
        dataset = MemberResource().export()
        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstmember.{format}"
        return response
    else:
        p = Paginator(User.objects.order_by('-date_joined'), 10)
        try:
            object_list = p.get_page(request.GET.get("page"))
        except:
            object_list = p.get_page(1)
        
        form_class = FormatForm()
            
        context = {
            'object_list': object_list,
            'form': form_class,
        }
        return render(request, 'myadmin/member_list.html', context)

@staff_member_required
def member_detail_view(request, pk):
    profile = User.objects.get(pk=pk)
    form = MemberForm(request.POST or None, instance=profile)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponseRedirect(reverse('myadmin:memberlist'))

    context = {
        'profile': profile,
        'form': form,
        'confirm': False,
    }
    return render(request, 'myadmin/member_detail.html', context)

@staff_member_required
def member_add_view(request):
    form = NewMemberForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:memberlist'))

    context = {
        'profile': None,
        'form': form,
        'confirm': False,
    }
    return render(request, 'myadmin/member_detail.html', context)

@staff_member_required
def member_delete_view(request, pk):
    member = User.objects.get(pk=pk)

    if request.method == 'POST':
        member.delete()
        return HttpResponseRedirect(reverse('myadmin:memberlist'))
    else:
        context = {
            'profile': member,
        }
        return render(request, 'myadmin/member_confirm_delete.html', context)

# Create your CBV views here. ==> security reason to go to FBV above
class MemberList(LoginRequiredMixin, ListView, FormView):
    model = Profile
    template_name = 'myadmin/member_list.html'

    # this is needed for 'post' of file to export
    form_class = FormatForm

    def get_queryset(self, *args, **kwargs):
        p = Paginator(Profile.objects.order_by('user__is_staff'), 10)
        try:
            return p.get_page(self.request.GET.get("page"))
        except:
            return p.get_page(1)

    def post(self, request, **kwargs):
        #qs = self.get_queryset() # you can select data through get_queryset()
        #dataset = UserMembershipResource().export(qs)
        dataset = MemberResource().export()

        format = request.POST.get('format')
        if format == 'xls':
            dataset_format = dataset.xls
        elif format == 'csv':
            dataset_format = dataset.csv
        else:
            dataset_format = dataset.json
        
        response = HttpResponse(dataset_format, content_type=f"text/{format}")
        response['Content-Disposition'] = f"attachement; filename=bstcustomer.{format}"
        return response

class MemberDetails(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'myadmin/member_detail.html'
