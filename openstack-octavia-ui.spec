%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-ddt
BuildRequires:  python3-pbr
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  openstack-macros

BuildRequires:  python3-selenium

Requires:       openstack-dashboard
Requires:       python3-pbr >= 2.0.0
Requires:       python3-babel >= 2.3.4
Requires:       python3-openstacksdk >= 0.53.0
Requires:       python3-barbicanclient >= 4.5.2
Requires:       python3-keystoneclient >= 1:3.22.0

%description
Octavia Dashboard is an extension for OpenStack Dashboard that provides a UI
for Octavia.

%if 0%{?with_doc}
# Documentation package
%package -n python3-%{openstack_name}-doc
Summary:        Documentation for OpenStack Octavia Dashboard for Horizon
%{?python_provide:%python_provide python3-%{openstack_name}-doc}

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  openstack-dashboard
BuildRequires:  python3-barbicanclient
BuildRequires:  python3-sphinxcontrib-rsvgconverter

%description -n python3-%{openstack_name}-doc
Documentation for Octavia Dashboard
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# Build html documentation
export PYTHONPATH="%{_datadir}/openstack-dashboard:%{python3_sitearch}:%{python3_sitelib}:%{buildroot}%{python3_sitelib}"
sphinx-build -b html doc/source doc/build/html
# Remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Move config to horizon
install -p -D -m 644 octavia_dashboard/enabled/_1482_project_load_balancer_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py

%check
%if 0%{?with_test}
%{__python3} manage.py test
%endif

%files
%doc README.rst
%license LICENSE
%{python3_sitelib}/octavia_dashboard
%{python3_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py*

%if 0%{?with_doc}
%files -n python3-%{openstack_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
