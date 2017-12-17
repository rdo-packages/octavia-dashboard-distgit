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
BuildRequires:  python-django-nose >= 1.2
BuildRequires:  python-nose-exclude >= 0.3.0
BuildRequires:  python-oslo-sphinx >= 4.7.0
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  python-selenium >= 2.50.1
BuildRequires:  python-openstackdocstheme >= 1.17.0
BuildRequires:  python-python-subunit >= 1.0.0
BuildRequires:  python-sphinx >= 1.6.2
BuildRequires:  python-oslotest >= 1.10.0
BuildRequires:  openstack-macros

Requires:       python-pbr >= 2.0.0
Requires:       python-babel >= 2.3.4
Requires:       python-openstacksdk >= 0.9.19
Requires:       python-oslo-log >= 3.30.0
Requires:       python-barbicanclient >= 4.0.0
Requires:       python-keystoneclient >= 3.8.0
Requires:       python-six >= 1.10.0

%description
Octavia Dashboard is an extension for OpenStack Dashboard that provides a UI
for Octavia.

# Documentation package
%package -n python-%{openstack_name}-doc
Summary:        Documentation for OpenStack Octavia Dashboard for Horizon

%description -n python-%{openstack_name}-doc
Documentation for Octavia Dashboard

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
%py_req_cleanup

%build
%{__python2} setup.py build

# Build html documentation
python setup.py build_sphinx -b html
# Remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Move config to horizon
install -p -D -m 640 octavia_dashboard/enabled/_1482_project_load_balancer_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py

%check
PYTHONPATH=/usr/share/openstack-dashboard/ ./run_tests.sh -N -P ||:

%files
%doc README.rst
%license LICENSE
%{python2_sitelib}/octavia_dashboard
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py*

%files doc
%doc doc/build/html
%license LICENSE

%changelog
