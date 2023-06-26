%global plugin tap-as-a-service
%global module neutron_taas
%global servicename neutron-taas
# oslosphinx do not work with sphinx > 2.0
%global with_doc 0
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order isort astroid pylint

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
License:        Apache-2.0
URL:            https://git.openstack.org/cgit/openstack/%{plugin}
Source0:        http://tarballs.openstack.org/%{plugin}/%{plugin}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
# Some unit tests do "which vim"
BuildRequires:  vim

%description
%{common_desc}

%package -n     python3-%{plugin}
Summary:        An extension to the OpenStack network service (Neutron) for port mirroring

Requires:       openstack-neutron-common
%description -n python3-%{plugin}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:        Tap-as-a-service documentation

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
# Remove bundled egg-info
rm -rf %{plugin}.egg-info

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel
%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

install -d -m 755 %{buildroot}/%{_sysconfdir}/neutron/
cp etc/*.ini %{buildroot}/%{_sysconfdir}/neutron/

# Make sure neutron-server loads new configuration file
install -d -m 755 %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/neutron/taas_plugin.ini %{buildroot}/%{_datadir}/neutron/server/taas_plugin.ini

install -d -m 755 %{buildroot}/%{_sysconfdir}/neutron/rootwrap.d
mv %{buildroot}%{_prefix}/etc/neutron/rootwrap.d/taas-i40e-sysfs.filters %{buildroot}/%{_sysconfdir}/neutron/rootwrap.d/taas-i40e-sysfs.filters

%check
export PYTHON=%{__python3}
%tox -e %{default_toxenv}

%files -n python3-%{plugin}
%license LICENSE
%doc README.rst
%{_bindir}/i40e_sysfs_command
%{python3_sitelib}/%{module}
%{python3_sitelib}/tap_as_a_service-*.dist-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/taas_plugin.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/rootwrap.d/taas-i40e-sysfs.filters
%{_datadir}/neutron/server/taas_plugin.ini
%exclude %{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{plugin}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python3-%{plugin}-tests
%license LICENSE
%{python3_sitelib}/%{module}/tests

%changelog
