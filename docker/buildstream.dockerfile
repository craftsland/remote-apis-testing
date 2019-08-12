FROM fedora:30

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8





# install all system dependencies
RUN \
    # Install dependencies
    dnf install --assumeyes \
    # buildstream dependencies
    bubblewrap \
    fuse \
    fuse-devel \
    # python-build dependencies
    gcc \
    gcc-c++ \
    python3-devel \
    python3-pip \
    python3-setuptools \
    # utilities dependencies
    bash-completion \
    # plugin dependencies
    bzr \
    git \
    lzip \
    ostree \
    patch \
    python3-gobject \
    # external-plugins dependencies
    quilt

# Clone buildstream master for install and examples subdirectory
RUN git clone https://gitlab.com/BuildStream/buildstream.git /buildstream

# install python dependencies
RUN pip3 install \
    arpy \
    # install buildstream from master cloned earlier.
    /buildstream \
    git+https://gitlab.com/buildstream/bst-external.git@0.16.0 \
    && \
    # Cleanup afterwards
    dnf remove --assumeyes gcc gcc-c++ python3-devel && \
    dnf clean all
