%global milestone .0rc1
%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate xvfbwrapper
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global pypi_name octavia-dashboard
%global openstack_name octavia-ui

# tests are disabled by default
%bcond_with tests

Name:           openstack-%{openstack_name}
Version:        12.0.0
Release:        0.1%{?milestone}%{?dist}
Summary:        OpenStack Octavia Dashboard for Horizon

License:        Apache-2.0
URL:            https://storyboard.openstack.org/#!/project/909
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
#
# patches_base=12.0.0.0rc1
#

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
BuildRequires:  pyproject-rpm-macros
BuildRequires:  openstack-macros

Requires:       openstack-dashboard

%description
Octavia Dashboard is an extension for OpenStack Dashboard that provides a UI
for Octavia.

%if 0%{?with_doc}
# Documentation package
%package -n python3-%{openstack_name}-doc
Summary:        Documentation for OpenStack Octavia Dashboard for Horizon

BuildRequires:  openstack-dashboard
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

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
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
# Build html documentation
export PYTHONPATH="%{_datadir}/openstack-dashboard:%{python3_sitearch}:%{python3_sitelib}:%{buildroot}%{python3_sitelib}"
%tox -e docs
# Remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

# Move config to horizon
install -p -D -m 644 octavia_dashboard/enabled/_1482_project_load_balancer_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py

%check
%if 0%{?with_test}
%tox -e %{default_toxenv}
%endif

%files
%doc README.rst
%license LICENSE
%{python3_sitelib}/octavia_dashboard
%{python3_sitelib}/*.dist-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1482_project_load_balancer_panel.py*

%if 0%{?with_doc}
%files -n python3-%{openstack_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Sep 15 2023 RDO <dev@lists.rdoproject.org> 12.0.0-0.1.0rc1
- Update to 12.0.0.0rc1

