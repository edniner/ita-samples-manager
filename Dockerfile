# A FROM line must be present but is ignored. It will be overridden by the --image-stream parameter in the buildConfig
FROM centos/python-34-centos7
# Temporarily switch to root user to install packages
USER root
# Install whatever is necessary. For brevity we use --nogpgcheck, don't do this in real applications!
RUN echo -e '[cc7-cernonly]\nname=CC7-CERNOnly\nbaseurl=http://linuxsoft.cern.ch/cern/centos/7/cernonly/x86_64' > /etc/yum.repos.d/cc7-cernonly.repo \
    && yum install --assumeyes --nogpgcheck oracle-instantclient12.2-basic-12.2.0.1.0-1.x86_64
RUN echo -e '[cc7-cernonly]\nname=CC7-CERNOnly\nbaseurl=http://linuxsoft.cern.ch/cern/centos/7/cernonly/x86_64' > /etc/yum.repos.d/cc7-cernonly.repo \
    && yum install --assumeyes --nogpgcheck oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64
RUN echo -e '[cc7-cernonly]\nname=CC7-CERNOnly\nbaseurl=http://linuxsoft.cern.ch/cern/centos/7/cernonly/x86_64' > /etc/yum.repos.d/cc7-cernonly.repo \
    && yum install --assumeyes --nogpgcheck oracle-instantclient12.2-sqlplus-12.2.0.1.0-1.x86_64
# Make sure the final image runs as unprivileged user
USER 1001