import nested_admin


class BaseAdmin(nested_admin.NestedModelAdmin):

    exclude = ['deleted_at']

    def get_queryset(self, request):
        try:
            return self.model.objects_with_deleted.all()
        except AttributeError:
            return super().get_queryset(request)


class BaseTabularInline(nested_admin.NestedTabularInline):

    exclude = ['deleted_at']
    extra = 0

    def get_queryset(self, request):
        try:
            return self.model.objects_with_deleted.all()
        except AttributeError:
            return super().get_queryset(request)


class BaseStackedInline(nested_admin.NestedStackedInline):

    exclude = ['deleted_at']
    extra = 0

    def get_queryset(self, request):
        try:
            return self.model.objects_with_deleted.all()
        except AttributeError:
            return super().get_queryset(request)
