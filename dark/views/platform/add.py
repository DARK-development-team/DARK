from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse

from dark.models.platform.platform import Platform
from dark.forms.platform import AddPlatformForm


def add_platform(instance: Platform):
    # logger.info(instance.name)
    # self.update_state(state='PROGRESS', meta={'status': "Cloning platform repository..."})
    instance.save()


class AddPlatformView(CreateView):
    model = Platform
    template_name = 'dark/platform/add.html'
    form_class = AddPlatformForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(AddPlatformView, self).form_valid(form)

    def get_success_url(self):
        return reverse('platform:info', kwargs={
            'platform': self.object.id,
        })
