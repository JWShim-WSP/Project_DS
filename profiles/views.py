from django.shortcuts import render
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import ListView, DetailView, FormView
from .forms import FormatForm
from profiles.resources import MemberResource
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if form.is_valid():
        form.save()
        confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'profiles/main.html', context)

@staff_member_required
def MemberList(request):
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
        response['Content-Disposition'] = f"attachement; filename=membership.{format}"
        return response
    else:
        p = Paginator(Profile.objects.order_by('user__is_staff'), 10)
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
def MemberDetails(request, pk):
    obj = Profile.objects.get(pk=pk)
    return render(request, 'myadmin/member_detail.html', {'object': obj})

"""
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
        response['Content-Disposition'] = f"attachement; filename=membership.{format}"
        return response

class MemberDetails(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'myadmin/member_detail.html'
"""