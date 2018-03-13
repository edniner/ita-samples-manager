from django.contrib.auth.middleware import RemoteUserMiddleware    

# customising the RemoteUserMiddleware to get the HTTP header that openshift adds
class ProxyRemoteUserMiddleware(RemoteUserMiddleware):
    header = 'HTTP_X_REMOTE_USER'
    def process_request(self,request):
        if hasattr(request, 'user') and request.user.is_authenticated() \
         and request.user.get_username() == request.META[self.header]:
                email =  request.META[self.header]
                if email is not None:
                    request.user.email = email
                firstname = request.META.get("ADFS_FULLNAME", None)
                if firstname is not None:
                    request.user.first_name = firstname
                request.user.save()
