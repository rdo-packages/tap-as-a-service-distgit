%global plugin tap-as-a-service
%global module neutron_taas
%global servicename neutron-taas
%global with_doc 1
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
Tap-as-a-Service (TaaS) is an extension to the OpenStack network service \
(Neutron). It provides remote port mirroring capability for tenant virtual \
networks. Port mirroring involves sending a copy of packets entering and/or \
leaving one port to another port, which is usually different from the original \
destinations of the packets being mirrored.

Name:       python-%{plugin}
Version:    XXX
Release:    XXX
Summary:    Neutron Tap as a Service	
License:    ASL 2.0
URL:        https://git.openstack.org/cgit/openstack/%{plugin}
Source0:    http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz
BuildArch:  noarch

BuildRequires:  python-coverage
BuildRequires:  python-hacking
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslotest
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python2-devel
BuildRequires:  systemd-units

%description
%{common_desc}

%package -n     python2-%{plugin}
Summary:        An extension to the OpenStack network service (Neutron) for port mirroring
%{?python_provide:%python_provide python2-%{plugin}}

Requires:       python-pbr >= 1.6
Requires:       python-babel >= 2.3.4
Requires:       python-neutron-lib >= 0.0.3
Requires:       python-oslo-db >= 4.1.0
Requires:       python-oslo-config >= 2:3.9.0
Requires:       python-oslo-concurrency >= 3.5.0
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-messaging >= 4.5.0
Requires:       python-oslo-service >= 1.0.0
Requires:       python-setuptools
Requires:       openstack-neutron-common

%description -n python2-%{plugin}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:        Tap-as-a-service documentation

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description doc
Documentation for Tap-as-a-service
%endif

%package tests
Summary:        Tap-as-a-Service Tests

Requires:       python-%{plugin} = %{epoch}:%{version}-%{release}
Requires:       python-hacking >= 0.10.0
Requires:       python-coverage >= 4.0
Requires:       python-subunit >= 0.0.18
Requires:       python-sphinx >= 1.2.1
Requires:       python-oslo-sphinx >= 4.7.0
Requires:       python-oslotest >= 1.10.0
Requires:       python-testrepository >= 0.0.18
Requires:       python-testresources >= 0.2.4
Requires:       python-testscenarios >= 0.4
Requires:       python-testtools >= 1.4.0

%description tests
Tap-as-a-Service set of tests

%package -n %{servicename}-openvswitch-agent
Summary:        Neutron Taas openvswitch agent
%description -n %{servicename}-openvswitch-agent 
Agent that enables TaaS functionality

%prep
%autosetup -n %{plugin}-%{upstream_version}
# remove requirements
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{plugin}.egg-info

%build
%py2_build
%if 0%{?with_doc}
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%py2_install

install -d -m 755 %{buildroot}/%{_sysconfdir}/neutron/
cp etc/*.ini %{buildroot}/%{_sysconfdir}/neutron/

# Make sure neutron-server loads new configuration file
install -d -m 755 %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/taas_plugin.ini %{buildroot}/%{_datadir}/neutron/server/taas_plugin.ini

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{servicename}-openvswitch-agent.service

%post
%systemd_post %{servicename}-openvswitch-agent.service

%preun
%systemd_preun %{servicename}-openvswitch-agent.service

%postun
%systemd_postun_with_restart %{servicename}-openvswitch-agent.service

%files -n python2-%{plugin}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/tap_as_a_service-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas_plugin.ini
%{_datadir}/neutron/server/taas_plugin.ini
%exclude %{python2_sitelib}/%{sname}/tests
%exclude %{_unitdir}/%{servicename}-openvswitch-agent.service
%exclude %{_bindir}/neutron-taas-openvswitch-agent

%if 0%{?with_doc}
%files -n python-%{plugin}-doc
%license LICENSE
%doc README.rst
%endif

%files -n python-%{plugin}-tests
%license LICENSE
%{python2_sitelib}/%{sname}/tests

%files -n %{servicename}-openvswitch-agent
%license LICENSE
%{_unitdir}/%{servicename}-openvswitch-agent.service
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas.ini
%{_bindir}/neutron-taas-openvswitch-agent

%changelog
