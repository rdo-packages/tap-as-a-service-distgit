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

Name:           python-%{plugin}
Version:        XXX
Release:        XXX
Summary:        Neutron Tap as a Service
License:        ASL 2.0
URL:            https://git.openstack.org/cgit/openstack/%{plugin}
Source0:        http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python-oslotest
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testresources
BuildRequires:  python-testtools
BuildRequires:  python2-devel
BuildRequires:  systemd-units
BuildRequires:  python-os-testr
BuildRequires:  python-neutron
BuildRequires:  python-neutron-tests
BuildRequires:  python-neutron-lib
BuildRequires:  python-neutronclient
BuildRequires:  python-neutronclient-tests
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-utils

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

Requires:       python-%{plugin} = %{version}-%{release}
Requires:       python-subunit >= 0.0.18
Requires:       python-oslotest >= 1.10.0
Requires:       python-testrepository >= 0.0.18
Requires:       python-testresources >= 0.2.4
Requires:       python-testscenarios >= 0.4
Requires:       python-testtools >= 1.4.0
Requires:       python-os-testr
Requires:       python-neutron
Requires:       python-neutron-tests
Requires:       python-neutron-lib
Requires:       python-neutronclient
Requires:       python-neutronclient-tests
Requires:       python-oslotest
Requires:       python-oslo-i18n
Requires:       python-oslo-config
Requires:       python-oslo-utils

%description tests
Tap-as-a-Service set of tests

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git
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
install -d -m 755 %{buildroot}/%{_sysconfdir}/neutron/conf.d/common
ln -s %{_sysconfdir}/neutron/taas_plugin.ini %{buildroot}/%{_sysconfdir}/neutron/conf.d/common/taas_plugin.ini

%check
%{__python2} setup.py testr

%files -n python2-%{plugin}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/tap_as_a_service-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas_plugin.ini
%{_sysconfdir}/neutron/conf.d/common/taas_plugin.ini
%exclude %{python2_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{plugin}-doc
%license LICENSE
%doc README.rst
%endif

%files -n python-%{plugin}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%changelog
