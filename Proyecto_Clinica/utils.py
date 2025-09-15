from django.shortcuts import redirect

def login_required_session(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("autenticado"):
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper
