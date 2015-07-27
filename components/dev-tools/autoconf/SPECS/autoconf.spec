#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the Performance Peak project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%include %{_sourcedir}/FSP_macros

%define pname autoconf
%{!?PROJ_DELIM:%define PROJ_DELIM %{nil}}

Summary:   A GNU tool for automatically configuring source code
Name:      %{pname}%{PROJ_DELIM}
Version:   2.69
Release:   1
License:   GPLv3+ and GFDL
Group:     fsp/dev-tools
DocDir:    %{FSP_PUB}/doc/contrib
URL:       http://www.gnu.org/software/autoconf/
Source0:   autoconf-%{version}.tar.gz
Source1:   FSP_macros
BuildRoot: %{_tmppath}/%{pname}-%{version}-%{release}-root

Requires: m4

%define debug_package %{nil}
%{!?FSP_PUB: %define FSP_PUB /opt/fsp/pub}
%define install_path %{FSP_PUB}/autotools

%description
GNU Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%setup -n autoconf-%{version}

%build
./configure --prefix=%{install_path}

%install
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install

# remove share/info/dir to avoid conflict with other package installs
rm -f $RPM_BUILD_ROOT/%{install_path}/share/info/dir

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{FSP_HOME}
%dir %{FSP_PUB}
%{FSP_PUB}/autotools
%doc THANKS
%doc NEWS
%doc ChangeLog.2
%doc ChangeLog
%doc COPYING
%doc ChangeLog.3
%doc README
%doc AUTHORS
%doc COPYINGv3
%doc ChangeLog.0
%doc ChangeLog.1
%doc TODO
%doc COPYING.EXCEPTION


%changelog
* Mon Sep 15 2014  <karl.w.schulz@intel.com> - 
- Initial build.

