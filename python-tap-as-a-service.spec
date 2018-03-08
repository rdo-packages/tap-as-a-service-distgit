%global plugin tap-as-a-service
%global module neutron_taas
%global servicename neutron-taas
%global with_doc 1
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Tap-as-a-Service (TaaS) is an extension to the OpenStack network service \
(Neutron). It provides remote port mirroring capability for tenant virtual \
networks. Port mirroring involves sending a copy of packets entering and/or \
leaving one port to another port, which is usually different from the original \
destinations of the packets being mirrored.

Name:           python-%{plugin}
Version:        3.0.0
Release:        1%{?dist}
Summary:        Neutron Tap as a Service
License:        ASL 2.0
URL:            https://git.openstack.org/cgit/openstack/%{plugin}
Source0:        https://github.com/openstack/%{plugin}/archive/%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python2-oslotest
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  python2-subunit
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
BuildRequires:  python2-testresources
BuildRequires:  python2-testtools
BuildRequires:  python2-devel
BuildRequires:  python2-os-testr
BuildRequires:  python-neutron
BuildRequires:  python-neutron-tests
BuildRequires:  python-neutron-lib
BuildRequires:  python2-neutronclient
BuildRequires:  python2-neutronclient-tests
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-utils

%description
%{common_desc}

%package -n     python2-%{plugin}
Summary:        An extension to the OpenStack network service (Neutron) for port mirroring
%{?python_provide:%python_provide python2-%{plugin}}

Requires:       python2-pbr >= 1.6
Requires:       python2-babel >= 2.3.4
Requires:       python-neutron-lib >= 1.13.0
Requires:       python2-oslo-db >= 4.27.0
Requires:       python2-oslo-config >= 2:5.1.0
Requires:       python2-oslo-concurrency >= 3.25.0
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-messaging >= 5.29.0
Requires:       python2-oslo-service >= 1.24.0
Requires:       openstack-neutron-common
Requires:       python2-oslo-i18n
Requires:       python2-oslo-utils

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
Requires:       python2-subunit >= 0.0.18
Requires:       python2-oslotest >= 1.10.0
Requires:       python2-testrepository >= 0.0.18
Requires:       python2-testresources >= 0.2.4
Requires:       python2-testscenarios >= 0.4
Requires:       python2-testtools >= 1.4.0
Requires:       python2-os-testr
Requires:       python-neutron-tests
Requires:       python2-neutronclient
Requires:       python2-neutronclient-tests
Requires:       python2-oslotest

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
install -d -m 755 %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/taas_plugin.ini %{buildroot}/%{_datadir}/neutron/server/taas_plugin.ini

%check
%{__python2} setup.py testr

%files -n python2-%{plugin}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/tap_as_a_service-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas_plugin.ini
%{_datadir}/neutron/server/taas_plugin.ini
%exclude %{python2_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{plugin}-doc
%license LICENSE
%doc README.rst doc/build/html
%endif

%files -n python-%{plugin}-tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%changelog
* Thu Mar 08 2018 RDO <dev@lists.rdoproject.org> 3.0.0-1
- Update to 3.0.0

