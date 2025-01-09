from django.shortcuts import redirect

class AdminPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/administration/') or request.path.startswith('/dashboard/') or request.path.startswith('/admin/'):
            if not request.user.is_authenticated or (not request.user.is_superuser and not request.user.is_staff):
                return redirect('/')
        return None
