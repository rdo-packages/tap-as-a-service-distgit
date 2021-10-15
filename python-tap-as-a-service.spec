%global plugin tap-as-a-service
%global module neutron_taas
%global servicename neutron-taas
# oslosphinx do not work with sphinx > 2.0
%global with_doc 0
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

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

BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-oslotest
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-subunit
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testresources
BuildRequires:  python3-testtools
BuildRequires:  python3-devel
BuildRequires:  python3-stestr
BuildRequires:  python3-neutron
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-neutron-lib
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-neutronclient
BuildRequires:  python3-neutronclient-tests
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-utils
# Some unit tests do "which vim"
BuildRequires:  vim

%description
%{common_desc}

%package -n     python3-%{plugin}
Summary:        An extension to the OpenStack network service (Neutron) for port mirroring
%{?python_provide:%python_provide python3-%{plugin}}

Requires:       python3-pbr >= 5.5.0
Requires:       python3-babel >= 2.8.0
Requires:       python3-neutron-lib >= 2.11.0
Requires:       python3-oslo-db >= 4.27.0
Requires:       python3-oslo-config >= 2:5.1.0
Requires:       python3-oslo-concurrency >= 3.25.0
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-messaging >= 5.29.0
Requires:       python3-oslo-service >= 1.24.0
Requires:       openstack-neutron-common
Requires:       python3-oslo-i18n
Requires:       python3-oslo-utils

%description -n python3-%{plugin}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:        Tap-as-a-service documentation

BuildRequires:  python3-sphinx
BuildRequires:  python3-oslo-sphinx

%description doc
Documentation for Tap-as-a-service
%endif

%package -n python3-%{plugin}-tests
Summary:        Tap-as-a-Service Tests
%{?python_provide:%python_provide python3-%{plugin}-tests}

Requires:       python3-%{plugin} = %{version}-%{release}
Requires:       python3-subunit >= 0.0.18
Requires:       python3-oslotest >= 1.10.0
Requires:       python3-testresources >= 0.2.4
Requires:       python3-testscenarios >= 0.4
Requires:       python3-testtools >= 1.4.0
Requires:       python3-stestr
Requires:       python3-neutron-tests
Requires:       python3-neutronclient
Requires:       python3-neutronclient-tests
Requires:       python3-oslotest

%description -n python3-%{plugin}-tests
Tap-as-a-Service set of tests

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git
# remove requirements
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{plugin}.egg-info

%build
%{py3_build}
%if 0%{?with_doc}
# generate html docs
%{__python3} setup.py build_sphinx -b html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

install -d -m 755 %{buildroot}/%{_sysconfdir}/neutron/
cp etc/*.ini %{buildroot}/%{_sysconfdir}/neutron/

# Make sure neutron-server loads new configuration file
install -d -m 755 %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/taas_plugin.ini %{buildroot}/%{_datadir}/neutron/server/taas_plugin.ini

install -d -m 755 %{buildroot}/%{_sysconfdir}/neutron/rootwrap.d
mv %{buildroot}%{_prefix}/etc/neutron/rootwrap.d/taas-i40e-sysfs.filters %{buildroot}/%{_sysconfdir}/neutron/rootwrap.d/taas-i40e-sysfs.filters

%check
export PYTHON=%{__python3}
stestr-3 run

%files -n python3-%{plugin}
%license LICENSE
%doc README.rst
%{_bindir}/i40e_sysfs_command
%{python3_sitelib}/%{module}
%{python3_sitelib}/tap_as_a_service-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas_plugin.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/rootwrap.d/taas-i40e-sysfs.filters
%{_datadir}/neutron/server/taas_plugin.ini
%exclude %{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{plugin}-doc
%license LICENSE
%doc README.rst doc/build/html
%endif

%files -n python3-%{plugin}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests

%changelog
