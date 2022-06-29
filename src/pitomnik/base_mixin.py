class BaseMixin:
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)
