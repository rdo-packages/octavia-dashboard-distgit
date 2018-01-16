%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name octavia-dashboard
%global openstack_name octavia-ui

# tests are disabled by default
%bcond_with tests

Name:           openstack-%{openstack_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Octavia Dashboard for Horizon

License:        ASL 2.0
URL:            https://storyboard.openstack.org/#!/project/909
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python-ddt
BuildRequires:  python-django-nose
BuildRequires:  python-nose-exclude
BuildRequires:  python-pbr
BuildRequires:  python-selenium
BuildRequires:  python-subunit
BuildRequires:  python-oslotest
BuildRequires:  openstack-macros

Requires:       openstack-dashboard
Requires:       python-pbr >= 2.0.0
Requires:       python-babel >= 2.3.4
Requires:       python-openstacksdk >= 0.9.19
Requires:       python-oslo-log >= 3.30.0
Requires:       python-barbicanclient >= 4.0.0
Requires:       python-keystoneclient >= 1:3.8.0
Requires:       python-six >= 1.10.0

%description
Octavia Dashboard is an extension for OpenStack Dashboard that provides a UI
for Octavia.

# Documentation package
%package -n python-%{openstack_name}-doc
Summary:        Documentation for OpenStack Octavia Dashboard for Horizon

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  openstack-dashboard
BuildRequires:  python-barbicanclient

%description -n python-%{openstack_name}-doc
Documentation for Octavia Dashboard

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup

%build
%py2_build

# Build html documentation
export PYTHONPATH="%{_datadir}/openstack-dashboard:%{python2_sitearch}:%{python2_sitelib}:%{buildroot}%{python2_sitelib}"
sphinx-build -b html doc/source doc/build/html
# Remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install

# Move config to horizon
install -p -D -m 640 octavia_dashboard/enabled/_1482_project_load_balancer_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py

%check
%if 0%{?with_test}
%{__python2} manage.py test
%endif

%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/octavia_dashboard
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py*

%files -n python-%{openstack_name}-doc
%doc doc/build/html
%license LICENSE

%changelog
