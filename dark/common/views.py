from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from dark.models.tournament import Tournament, TournamentRound
from dark.models.tournament.team import TeamBot


class UserAuthenticationDependentContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(UserAuthenticationDependentContextMixin, self).get_context_data(**kwargs)
        context.update(
            self.get_authenticated_context_data(**kwargs) if self.request.user.is_authenticated else
            self.get_not_authenticated_context_data(**kwargs)
        )
        return context

    def get_authenticated_context_data(self, **kwargs):
        return {}

    def get_not_authenticated_context_data(self, **kwargs):
        return {}


class ForeignKeysMixin(object):
    url_kwargs = []
    url_kwarg_fields = []

    def form_valid(self, form):
        url_kwarg_raw_values = [self.kwargs.get(url_kwarg) for url_kwarg in self.url_kwargs]
        for field_name, raw_value in zip(self.url_kwarg_fields, url_kwarg_raw_values):
            field = getattr(form.instance.__class__, field_name).field
            value = field.related_model.objects.get(id=raw_value)
            setattr(form.instance, field_name, value)
        return super(ForeignKeysMixin, self).form_valid(form)


class FieldQuerySetMixin(object):
    def get_queryset_for_field(self, field_name, queryset):
        return queryset

    def get_form(self, form_class=None):
        form = super(FieldQuerySetMixin, self).get_form(form_class)
        for field_name, value in form.fields.items():
            form.fields[field_name].queryset = self.get_queryset_for_field(field_name, value.queryset)
        return form


class TournamentEditableMixin(object):
    def dispatch(self, request, *args, **kwargs):
        tournament = get_object_or_404(Tournament, id=self.kwargs['tournament'])
        now = timezone.now()

        if tournament.start_date < now or tournament.end_date < now:
            messages.error(request, 'Tournament is no longer editable!')
            return redirect(reverse('tournament:info', kwargs={'tournament': self.kwargs['tournament']}))
        else:
            return super().dispatch(request, *args, **kwargs)


class RoundAddableMixin(object):
    def dispatch(self, request, *args, **kwargs):
        tournament = get_object_or_404(Tournament, id=self.kwargs['tournament'])
        now = timezone.now()

        if now < tournament.end_date:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'Tournament is no longer editable!')
            return redirect(reverse('tournament:info', kwargs={'tournament': self.kwargs['tournament']}))


class RoundEditableMixin(object):
    def dispatch(self, request, *args, **kwargs):
        now = timezone.now()

        if 'tround' in kwargs:
            tround = get_object_or_404(TournamentRound, id=self.kwargs['tround'])
        else:
            bot = get_object_or_404(TeamBot, id=self.kwargs['bot'])
            tround = bot.tround

        if tround.start_date < now < tround.end_date:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, 'Round is no longer editable!')
            return redirect(reverse('tournament:team:info',
                                    kwargs={'tournament': self.kwargs['tournament'], 'team': self.kwargs['team']}))
