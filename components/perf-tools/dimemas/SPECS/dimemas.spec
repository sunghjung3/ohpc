#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

# Build that is dependent on compiler/mpi toolchains
%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%include %{_sourcedir}/OHPC_macros

# Base package name
%define pname dimemas

Summary:	Dimemas tool
Name:		%{pname}-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Version:	5.4.2
Release:	1
License:	GNU
Group:		%{PROJ_NAME}/perf-tools
URL:		https://tools.bsc.es
Source0:	https://ftp.tools.bsc.es/dimemas/dimemas-%{version}-src.tar.bz2

BuildRequires: boost-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Requires:      boost-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
BuildRequires: bison make
%if 0%{?rhel} || 0%{?openEuler}
BuildRequires: flex-devel
BuildRequires: flex
%endif
%if 0%{?suse_version}
BuildRequires: libfl-devel
BuildRequires: flex%{PROJ_DELIM}
%endif
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
#!BuildIgnore: post-build-checks

# Default library install path
%define install_path %{OHPC_LIBS}/%{compiler_family}/%{mpi_family}/%{pname}/%version

%description
Dimemas is a performance analysis tool for message-passing
programs. It enables the user to develop and tune parallel applications on a
workstation, while providing an accurate prediction of their performance on the
parallel target machine. The Dimemas simulator reconstructs the time behavior
of a parallel application on a machine modeled by a set of performance
parameters. Thus, performance experiments can be done easily. The supported
target architecture classes include networks of workstations, single and
clustered SMPs, distributed memory parallel computers, and even heterogeneous
systems.

%prep
%setup -q -n %{pname}-%{version}


%build
%ohpc_setup_compiler
module load boost

#./bootstrap

%if 0%{?suse_version}
module load flex
export LDFLAGS="-L$FLEX_LIB"
%endif
export CFLAGS="${CFLAGS} -Wno-implicit-int"
export CFLAGS="${CFLAGS} -Wno-implicit-function-declaration"
export CXXFLAGS="${CXXFLAGS} -Wno-implicit-int"
export CXXFLAGS="${CXXFLAGS} -Wno-implicit-function-declaration"
export CXXFLAGS="${CXXFLAGS} -Wno-register"
%if "%{compiler_family}" == "arm1"
export CFLAGS="${CFLAGS} -fsimdmath"
export CXXFLAGS="${CXXFLAGS} -fsimdmath"
%endif

./configure --prefix=%{install_path} \
            --with-boost=$BOOST_DIR || cat config.log

make %{?_smp_mflags}

%install
export NO_BRP_CHECK_RPATH=true

# OpenHPC compiler designation
%ohpc_setup_compiler

make DESTDIR=$RPM_BUILD_ROOT install

# don't package static libs
rm -f $RPM_BUILD_ROOT%{install_path}/lib/*.la
rm -f $RPM_BUILD_ROOT%{install_path}/lib/*.a
rm -f $RPM_BUILD_ROOT%{install_path}/lib/dimemas/*.la

# OpenHPC module file
%{__mkdir} -p %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "This module loads the %{pname} library built with the %{compiler_family} compiler"
puts stderr "toolchain and the %{mpi_family} MPI stack."
puts stderr "\nVersion %{version}\n"

}
module-whatis "Name: %{pname} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Category: performance tool"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

set     version			    %{version}

# Require boost
depends-on boost

prepend-path    PATH                %{install_path}/bin

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_INC        %{install_path}/include

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%{__mkdir} -p $RPM_BUILD_ROOT/%{_docdir}

%files
%{OHPC_PUB}
%doc
