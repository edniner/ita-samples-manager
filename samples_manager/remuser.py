from django.contrib.auth.middleware import RemoteUserMiddleware    

# customising the RemoteUserMiddleware to get the HTTP header that openshift adds
class ProxyRemoteUserMiddleware(RemoteUserMiddleware):
    header = 'HTTP_X_REMOTE_USER'
    def process_request(self,request):
        print(request)
        if hasattr(request, 'user') and request.user.is_authenticated() \
         and request.user.get_username() == request.META["HTTP_X_REMOTE_USER"]:
                username =  request.META["HTTP_X_REMOTE_USER"]
                if username is not None:
                    request.user.username = username
                firstname = request.META["HTTP_X_REMOTE_FIRST_NAME"]
                if firstname is not None:
                    request.user.first_name = firstname
                lastname = request.META["HTTP_X_REMOTE_LAST_NAME"]
                if lastname is not None:
                    request.user.last_name = lastname
                email =  request.META["HTTP_X_REMOTE_EMAIL"]
                if email is not None:
                    request.user.email = email
                request.user.save()
