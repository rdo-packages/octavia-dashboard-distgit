# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
# Doc build is trying to access location /usr/share/openstack-dashboard/local for
# writing 'secret_key_store.lock', LOCAL_PATH=/tmp (writable) and SECRET_KEY is set in
# /etc/openstack-dashboard/local_settings but this file is not readable during
# mockbuild as permission for this file is 0640(root:apache). Until the issue
# is cleared in python-django-horizon packages disabling doc build.
%global with_doc 0
%else
%global pyver 2
%global with_doc 1
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_sitearch %python%{pyver}_sitearch
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name octavia-dashboard
%global openstack_name octavia-ui

# tests are disabled by default
%bcond_with tests

Name:           openstack-%{openstack_name}
Version:        4.0.0
Release:        1%{?dist}
Summary:        OpenStack Octavia Dashboard for Horizon

License:        ASL 2.0
URL:            https://storyboard.openstack.org/#!/project/909
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

#

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-ddt
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  openstack-macros

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-selenium
%else
BuildRequires:  python%{pyver}-selenium
%endif

Requires:       openstack-dashboard
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-openstacksdk >= 0.24.0
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-barbicanclient >= 4.5.2
Requires:       python%{pyver}-keystoneclient >= 1:3.8.0
Requires:       python%{pyver}-six >= 1.10.0

%description
Octavia Dashboard is an extension for OpenStack Dashboard that provides a UI
for Octavia.

%if 0%{?with_doc}
# Documentation package
%package -n python%{pyver}-%{openstack_name}-doc
Summary:        Documentation for OpenStack Octavia Dashboard for Horizon
%{?python_provide:%python_provide python%{pyver}-%{openstack_name}-doc}

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinxcontrib-apidoc
BuildRequires:  openstack-dashboard
BuildRequires:  python%{pyver}-barbicanclient
BuildRequires:  python%{pyver}-sphinxcontrib-rsvgconverter

%description -n python%{pyver}-%{openstack_name}-doc
Documentation for Octavia Dashboard
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# Build html documentation
export PYTHONPATH="%{_datadir}/openstack-dashboard:%{pyver_sitearch}:%{pyver_sitelib}:%{buildroot}%{pyver_sitelib}"
sphinx-build-%{pyver} -b html doc/source doc/build/html
# Remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Move config to horizon
install -p -D -m 640 octavia_dashboard/enabled/_1482_project_load_balancer_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py

%check
%if 0%{?with_test}
%{pyver_bin} manage.py test
%endif

%files
%doc README.rst
%license LICENSE
%{pyver_sitelib}/octavia_dashboard
%{pyver_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py*

%if 0%{?with_doc}
%files -n python%{pyver}-%{openstack_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Wed Oct 16 2019 RDO <dev@lists.rdoproject.org> 4.0.0-1
- Update to 4.0.0

* Fri Oct 11 2019 RDO <dev@lists.rdoproject.org> 4.0.0-0.2.0rc1
- Update to 4.0.0.0rc2

* Mon Sep 30 2019 RDO <dev@lists.rdoproject.org> 4.0.0-0.1.0rc1
- Update to 4.0.0.0rc1

