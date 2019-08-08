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
RUN echo -e '[cc7-cernonly]\nname=CC7-CERNOnly\nbaseurl=http://linuxsoft.cern.ch/cern/centos/7/cernonly/x86_64' > /etc/yum.repos.d/cc7-cernonly.repo \
    && yum install libxslt-devel libxml2-devel

RUN yum install libaio

RUN yum update -y && yum upgrade -y
# install basic tools for downloading, extracting & managing files
RUN yum install wget git gcc openssl-devel bzip2-devel -y
# check for any upgrades
RUN yum upgrade -y && yum clean all -y
# download & extract Python3.4.0 files, since CentOS only ships with 2.7.5
#RUN cd /usr/src && wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tar.xz && tar xvf Python-3.6.5.tar.xz
#RUN cd /usr/src/Python-3.6.5 && ./configure --enable-optimizations && make altinstall
# validate correct version install
#RUN echo $PATH
#RUN python 
# upgrade to latest Pip for Python3.4.0
RUN pip3 install --upgrade pip
# validate correct version install
#RUN pip3 -V
# install packages for pytimber application
RUN pip3 install lxml zeep

# Make sure the final image runs as unprivileged user
USER 1001