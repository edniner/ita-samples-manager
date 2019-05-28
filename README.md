This is a django project for managing all the operations and functionalities of the IRRAD facility. 
The project uses the Oracle database.
Here you can find some instructions on how to build and deploy this project on Openshift.
First you have to generate the file requirements.txt with the command: 
pip install -r requirements.txt

In these requirements there is also the cx_Oracle python package which links python with Oracle.
Since in the oracle client is not present in the standard Python images, we need to intall them.
We create a Dockerfile where we add the commands for the packages that we want to install and we add the following text:

A FROM line must be present but is ignored. It will be overridden by the --image-stream parameter in the buildConfig


FROM centos/python-34-centos7


Temporarily switch to root user to install packages
USER root



Install whatever is necessary. 
RUN echo -e '[cc7-cernonly]\nname=CC7-CERNOnly\nbaseurl=http://linuxsoft.cern.ch/cern/centos/7/cernonly/x86_64' > /etc/yum.repos.d/cc7-cernonly.repo \
    && yum install --assumeyes --nogpgcheck oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64
RUN echo -e '[cc7-cernonly]\nname=CC7-CERNOnly\nbaseurl=http://linuxsoft.cern.ch/cern/centos/7/cernonly/x86_64' > /etc/yum.repos.d/cc7-cernonly.repo \
    && yum install --assumeyes --nogpgcheck oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64
RUN echo -e '[cc7-cernonly]\nname=CC7-CERNOnly\nbaseurl=http://linuxsoft.cern.ch/cern/centos/7/cernonly/x86_64' > /etc/yum.repos.d/cc7-cernonly.repo \
    && yum install --assumeyes --nogpgcheck oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64


Make sure the final image runs as unprivileged user
USER 1001


Then we try to build the Docker image first using this command: 

oc new-build --image-stream=python:3.4 --name="<docker_image_name>" --strategy=docker https://gitlab.cern.ch/<team>/<project>.git

After this image is successful then we have to build project with the source and deploy it running this command:

 
oc new-app docker_image_name~https://gitlab.cern.ch/<team>/<project>.git

For more details see: https://cern.service-now.com/service-portal/article.do?n=KB0004913
and https://github.com/openshift/django-ex


In order to run the project with the wsgi.py and load also the static files, you need to do also some changes to the settings.py
ALLOWED_HOSTS=['*']
add 'mod_wsgi.server' in the INSTALLED_APPS
add 'whitenoise.middleware.WhiteNoiseMiddleware' in the MIDDLEWARE_CLASSES
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

Also pay attention to the configurations of the Oracle database. If you don't have the SID you can use the service name you can use the property 'NAME' to add the configurations:
DATABASES = {
  
  'default': {

        'ENGINE': 'django.db.backends.oracle',

        'NAME': 'hostname:10121/service_name',

        'USER': 'username',

        'PASSWORD': 'password',

    }

}
