# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global plugin tap-as-a-service
%global module neutron_taas
%global servicename neutron-taas
# oslosphinx do not work with sphinx > 2.0
%if %{pyver} == 3
%global with_doc 0
%else
%global with_doc 1
%endif
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

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testresources
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-neutron
BuildRequires:  python%{pyver}-neutron-tests
BuildRequires:  python%{pyver}-neutron-lib
BuildRequires:  python%{pyver}-neutron-lib-tests
BuildRequires:  python%{pyver}-neutronclient
BuildRequires:  python%{pyver}-neutronclient-tests
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-utils

%description
%{common_desc}

%package -n     python%{pyver}-%{plugin}
Summary:        An extension to the OpenStack network service (Neutron) for port mirroring
%{?python_provide:%python_provide python%{pyver}-%{plugin}}

Requires:       python%{pyver}-pbr >= 1.6
Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-neutron-lib >= 1.13.0
Requires:       python%{pyver}-oslo-db >= 4.27.0
Requires:       python%{pyver}-oslo-config >= 2:5.1.0
Requires:       python%{pyver}-oslo-concurrency >= 3.25.0
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-messaging >= 5.29.0
Requires:       python%{pyver}-oslo-service >= 1.24.0
Requires:       openstack-neutron-common
Requires:       python%{pyver}-oslo-i18n
Requires:       python%{pyver}-oslo-utils

%description -n python%{pyver}-%{plugin}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:        Tap-as-a-service documentation

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-oslo-sphinx

%description doc
Documentation for Tap-as-a-service
%endif

%package -n python%{pyver}-%{plugin}-tests
Summary:        Tap-as-a-Service Tests
%{?python_provide:%python_provide python%{pyver}-%{plugin}-tests}

Requires:       python%{pyver}-%{plugin} = %{version}-%{release}
Requires:       python%{pyver}-subunit >= 0.0.18
Requires:       python%{pyver}-oslotest >= 1.10.0
Requires:       python%{pyver}-testresources >= 0.2.4
Requires:       python%{pyver}-testscenarios >= 0.4
Requires:       python%{pyver}-testtools >= 1.4.0
Requires:       python%{pyver}-stestr
Requires:       python%{pyver}-neutron-tests
Requires:       python%{pyver}-neutronclient
Requires:       python%{pyver}-neutronclient-tests
Requires:       python%{pyver}-oslotest

%description -n python%{pyver}-%{plugin}-tests
Tap-as-a-Service set of tests

%prep
%autosetup -n %{plugin}-%{upstream_version} -S git
# remove requirements
%py_req_cleanup
# Remove bundled egg-info
rm -rf %{plugin}.egg-info

%build
%{pyver_build}
%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

install -d -m 755 %{buildroot}/%{_sysconfdir}/neutron/
cp etc/*.ini %{buildroot}/%{_sysconfdir}/neutron/

# Make sure neutron-server loads new configuration file
install -d -m 755 %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/taas_plugin.ini %{buildroot}/%{_datadir}/neutron/server/taas_plugin.ini

install -d -m 755 %{buildroot}/%{_sysconfdir}/neutron/rootwrap.d
mv %{buildroot}%{_prefix}/etc/neutron/rootwrap.d/taas-i40e-sysfs.filters %{buildroot}/%{_sysconfdir}/neutron/rootwrap.d/taas-i40e-sysfs.filters

%check
export PYTHON=%{pyver_bin}
stestr-%{pyver} run

%files -n python%{pyver}-%{plugin}
%license LICENSE
%doc README.rst
%{_bindir}/i40e_sysfs_command
%{pyver_sitelib}/%{module}
%{pyver_sitelib}/tap_as_a_service-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas_plugin.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/rootwrap.d/taas-i40e-sysfs.filters
%{_datadir}/neutron/server/taas_plugin.ini
%exclude %{pyver_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{plugin}-doc
%license LICENSE
%doc README.rst doc/build/html
%endif

%files -n python%{pyver}-%{plugin}-tests
%license LICENSE
%{pyver_sitelib}/%{module}/tests

%changelog
