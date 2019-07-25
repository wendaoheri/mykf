FROM centos:7


# RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && yum makecache

RUN yum install -y epel-release && \
    yum install -y python && \
    yum install -y python-setuptools && \
    yum install -y wget && \
    yum install -y unzip && \
    yum install -y python-pip

ADD pip.conf /root/.pip/pip.conf