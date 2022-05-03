Name:           mesh
Version:        0.4.0.1rc6
Release:        1%{?dist}
Summary:        IoT end-to-end encrypted IPv6 network

License:        GPLv3
URL:            https://github.com/RiV-chain
Source0:        https://codeload.github.com/RiV-chain/RiV-mesh/tar.gz/v%{version}

BuildRequires:  systemd golang >= 1.16 git
Requires(pre):  shadow-utils
Requires(post): /sbin/chkconfig, /sbin/service
Requires(preun): /sbin/chkconfig, /sbin/service
Conflicts:      mesh-develop

%description
RiV-mesh is an implementation of a fully end-to-end encrypted IPv6 network,
created in the scope to produce the Transport Layer for RiV Chain Blockchain,
also to facilitate secure conectivity between a wide spectrum of endpoint devices like IoT devices,
desktop computers or even routers.
It is lightweight, self-arranging, supported on multiple platforms and allows pretty
much any IPv6-capable application to communicate securely with other RiV-mesh nodes.
RiV-mesh does not require you to have IPv6 Internet connectivity - it also works over IPv4.

%pre
getent group mesh >/dev/null || groupadd -r mesh
exit 0

%prep
%setup -qn RiV-mesh-%{version}

%build
export PKGNAME="%{name}"
export PKGVER="%{version}"
export GOPROXY="https://proxy.golang.org,direct"
./build -t -p -l "-linkmode=external"

%install
rm -rf %{buildroot}
install -m 0755 -D mesh %{buildroot}/%{_bindir}/mesh
install -m 0755 -D meshctl %{buildroot}/%{_bindir}/meshctl
install -m 0755 -D contrib/systemd/mesh.service %{buildroot}/%{_sysconfdir}/systemd/system/mesh.service

%files
%defattr(-,root,root)
%{_bindir}/mesh
%{_bindir}/meshctl
%{_sysconfdir}/systemd/system/mesh.service

%post
/sbin/chkconfig --add mesh >/dev/null 2>/dev/null #supress notes on systemd

if [ "$1" -ge "1" ]; then
    /sbin/service mesh condrestart >/dev/null 2>&1 || :
fi
echo "-----------------------------------------------------------------------------" > /dev/stderr
echo "  To finish the installation, you need to configure the peers list and" > /dev/stderr
echo "  in the file /etc/mesh.config." > /dev/stderr
echo "  Then run 'service mesh start'." > /dev/stderr
echo "-----------------------------------------------------------------------------" > /dev/stderr

%preun
if [ $1 = 0 ] ; then
    /sbin/service mesh stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del mesh >/dev/null 2>/dev/null #supress notes on systemd
fi
exit 0

%postun
%systemd_postun_with_restart mesh.service
