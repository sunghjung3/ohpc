#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%include %{_sourcedir}/OHPC_macros

%define pname hpc-workspace

Name:    %{pname}%{PROJ_DELIM}
Version: 1.4.0
Release: 1%{?dist}
Summary: Temporary workspace management
License: GPL
Source:  https://github.com/holgerBerger/hpc-workspace/archive/refs/tags/%{version}.tar.gz
Source1: ws.conf.template
Group:   %{PROJ_NAME}/admin
URL:     https://github.com/holgerBerger/hpc-workspace

BuildRequires: gcc-c++
BuildRequires: python3-devel
BuildRequires: boost-devel
BuildRequires: yaml-cpp-devel
BuildRequires: ncurses-devel
BuildRequires: cmake
Requires: python3
Requires: python3-pyyaml
Requires: lua5.1
Requires: boost-system
Requires: boost-filesystem
Requires: boost-regex
Requires: boost-program-options
Requires: ncurses
Requires: libcap
Requires: yaml-cpp


# Default library install path
%define install_path %{OHPC_ADMIN}/%{pname}/%{version}

%description
HPC Workspace provides tools to provision temporaty workspaces on scratch or 
working filesystems in an HPC environment.

%prep
%setup -q -n %{pname}-%{version}

%build
cmake \
  -DCMAKE_INSTALL_PREFIX=%{install_path} \
  .
make

%install
make DESTDIR=%{buildroot} install
%{__mkdir_p} %{buildroot}%{_sysconfdir}/cron.daily
%{__mkdir_p} %{buildroot}%{_localstatedir}/log/%{pname}
cp %{SOURCE1} %{buildroot}%{_sysconfdir}
%{__cat} << EOF > %{buildroot}%{_sysconfdir}/cron.daily/%{pname}
#!/bin/sh

# Daily cleanup script for %{pname}
%{install_path}/sbin/ws_expirer -c > %{_localstatedir}/log/%{pname}/expirer-`date +%y.%m.%d`
find %{_localstatedir}/log/%{pname} -type f -ctime +90 -exec rm {} \;
EOF

%{__mkdir} -p %{buildroot}/%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}
#%Module1.0#####################################################################
proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the HPC Workspace utility"
puts stderr " "
puts stderr "Version %{version}"
puts stderr " "

}

module-whatis "Name: HPC Workspace utility"
module-whatis "Version: %{version}"
module-whatis "Category: resource manager tools"
module-whatis "Description: %{Summary}"

set     version                 %{version}

prepend-path    PATH            %{install_path}/bin

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
set     ModulesVersion      "%{version}"
EOF

%files 
%config %{_sysconfdir}/ws.conf.template
%dir %{OHPC_ADMIN}
%dir %{OHPC_MODULES}
%dir %{_localstatedir}/log/%{pname}
%dir %{_sysconfdir}/cron.daily
%{OHPC_ADMIN}/%{pname}
%{OHPC_MODULES}/%{pname}
%{_sysconfdir}/cron.daily/%{pname}
%attr(4755, root, root) %{install_path}/bin/ws_allocate
%attr(4755, root, root) %{install_path}/bin/ws_release
%attr(4755, root, root) %{install_path}/bin/ws_restore


%pre
# provide specific uid/gid to ensure that it is the same across the cluster
/usr/bin/getent group hpcws >/dev/null 2>&1 || \
  /usr/sbin/groupadd -r hpcws -g 85
/usr/bin/getent passwd hpcws >/dev/null 2>&1 || \
  /usr/sbin/useradd -c "HPC Workspace manager" \
  -d %{_sysconfdir} -g hpcws -s /sbin/nologin -r hpcws -u 85
exit 0