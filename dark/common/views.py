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
