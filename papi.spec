Summary:	-
Summary(pl.UTF-8):	-
Name:		papi
Version:	1.0
%define	subver	beta
Release:	0.%{subver}.1
License:	GPL/LGPL/MIT/CDDL(?)
Group:		Libraries
Source0:	http://downloads.sourceforge.net/openprinting/%{name}-%{version}_%{subver}.tar.bz2
# Source0-md5:	7e6f769de88d581fdb78a538d97e6373
Patch0:		%{name}-glibc.patch
URL:		http://openprinting.sourceforge.net/
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel >= 1:1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl.UTF-8

%package devel
Summary:	Header files for libpapi library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libpapi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libpapi library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libpapi.

%package static
Summary:	Static libpapi library
Summary(pl.UTF-8):	Statyczna biblioteka libpapi
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libpapi library.

%description static -l pl.UTF-8
Statyczna biblioteka libpapi.

%prep
%setup -q -n %{name}-%{version}_%{subver}
%patch0 -p1

%build
# if ac/am/lt/* rebuilding is necessary, do it in this order and add
# appropriate BuildRequires
#%{__libtoolize}
#%{__aclocal}
#%{__autoconf}
#%{__autoheader}
#%{__automake}
CPPFLAGS=$(apr-1-config --includes)
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
#install -d $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%doc devel-doc/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/foo
%{_aclocaldir}/*.m4
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
