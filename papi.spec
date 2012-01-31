# TODO: config file for mod_ipp
Summary:	Free Standards Group Open Printing API and applications implementation
Summary(pl.UTF-8):	Implementacja API i aplikacji Free Standards Group Open Printing
Name:		papi
Version:	1.0
%define	subver	beta
Release:	0.%{subver}.1
License:	CDDL, MIT (libpapi-cups), LGPL v2+ (NSS for printers)
Group:		Applications/Printing
Source0:	http://downloads.sourceforge.net/openprinting/%{name}-%{version}_%{subver}.tar.bz2
# Source0-md5:	7e6f769de88d581fdb78a538d97e6373
Patch0:		%{name}-glibc.patch
Patch1:		%{name}-apache2.patch
Patch2:		%{name}-install.patch
URL:		http://openprinting.sourceforge.net/
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel >= 1:1.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cups-devel
BuildRequires:	libmagic-devel
BuildRequires:	libtool
Requires:	%{name}-libs = %{version}-%{release}
Provides:	printingclient
Provides:	printingdaemon
Obsoletes:	printingclient
Obsoletes:	printingdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/papi

%description
The Free Standards Group Open Printing API provides a standards based
interface for applications to interact with print services. This
implementation contains support for servers with LPD (RFC 1179) and/or
IPP (RFC 2910/2911) protocol interfaces and name service storage of
configuration data. There are also implementations of many common BSD
and SysV printing commands.

%description -l pl.UTF-8
Free Standards Group Open Printing API to oparty na standardach
interfejs pozwalający aplikacjom współpracować z usługami drukowania.
Ta implementacja zawiera obsługę serwerów obsługujących protokoły LPD
(RFC 1179) i/lub IPP (RFC 2910/2911) oraz przechowywanie danych
konfiguracyjnych z obsługą NSS. Zapewnia także implementację wielu
często używanych poleceń BSD i SysV obsługujących drukowanie.

%package -n apache-mod_ipp
Summary:	IPP (Internet Printing Protocol) module for Apache
Summary(pl.UTF-8):	Moduł IPP (Internet Printing Protocol) dla Apache'a
Group:		Networking/Daemons/HTTP
Requires:	%{name}-libs = %{version}-%{release}
Requires:	apache-base >= 2
Provides:	apache(mod_ipp) = %{version}-%{release}

%description -n apache-mod_ipp
IPP (Internet Printing Protocol) module for Apache.

%description -n apache-mod_ipp -l pl.UTF-8
Moduł IPP (Internet Printing Protocol) dla Apache'a.

%package libs
Summary:	Free Standards Group Open Printing API libraries
Summary(pl.UTF-8):	Biblioteki Free Standards Group Open Printing API
Group:		Libraries

%description libs
Free Standards Group Open Printing API libraries.

%description libs -l pl.UTF-8
Biblioteki Free Standards Group Open Printing API.

%package devel
Summary:	Header files for Free Standards Group Open Printing API libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Free Standards Group Open Printing API
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Free Standards Group Open Printing API libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Free Standards Group Open Printing API.

%package static
Summary:	Static Free Standards Group Open Printing API libraries
Summary(pl.UTF-8):	Statyczne Biblioteki Free Standards Group Open Printing API
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Free Standards Group Open Printing API libraries.

%description static -l pl.UTF-8
Statyczne Biblioteki Free Standards Group Open Printing API.

%prep
%setup -q -n %{name}-%{version}_%{subver}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CPPFLAGS="$(apr-1-config --cppflags) $(apu-1-config --includes)"
# debug.h and http.h are too common, use include subdir
%configure \
	--with-apache=%{_prefix} \
	--includedir=%{_includedir}/papi \
	--enable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# modules dlopened by psm-*.so
%{__rm} $RPM_BUILD_ROOT%{_libexecdir}/psm-*.{la,a}

# apache module
install -d $RPM_BUILD_ROOT%{_libdir}/apache
mv $RPM_BUILD_ROOT%{_libdir}/mod_ipp.so $RPM_BUILD_ROOT%{_libdir}/apache
%{__rm} $RPM_BUILD_ROOT%{_libdir}/mod_ipp.{la,a}

# keep only source form of examples, move to standard place
install -d $RPM_BUILD_ROOT%{_examplesdir}
mv $RPM_BUILD_ROOT%{_datadir}/examples/src $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/examples

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cancel
%attr(755,root,root) %{_bindir}/lp
%attr(755,root,root) %{_bindir}/lpq
%attr(755,root,root) %{_bindir}/lpr
%attr(755,root,root) %{_bindir}/lprm
%attr(755,root,root) %{_bindir}/lpstat
%attr(755,root,root) %{_sbindir}/accept
%attr(755,root,root) %{_sbindir}/disable
%attr(755,root,root) %{_sbindir}/enable
%attr(755,root,root) %{_sbindir}/in.lpd
%attr(755,root,root) %{_sbindir}/lpc
%attr(755,root,root) %{_sbindir}/lpmove
%attr(755,root,root) %{_sbindir}/reject
%attr(2755,root,lp) %{_libdir}/papi/lpd-port
%attr(755,root,root) %{_libdir}/papi/psm-ipp.so
%attr(755,root,root) %{_libdir}/papi/psm-lpd.so
%{_mandir}/man1/accept.1m*
%{_mandir}/man1/cancel.1*
%{_mandir}/man1/disable.1*
%{_mandir}/man1/enable.1*
%{_mandir}/man1/lp.1*
%{_mandir}/man1/lpc.1b*
%{_mandir}/man1/lpmove.1m*
%{_mandir}/man1/lpq.1b*
%{_mandir}/man1/lpr.1b*
%{_mandir}/man1/lprm.1b*
%{_mandir}/man1/lpstat.1*
%{_mandir}/man1/reject.1m*
%{_mandir}/man5/psm-ipp.5*

%files -n apache-mod_ipp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apache/mod_ipp.so

%files libs
%defattr(644,root,root,755)
%doc ChangeLog README TODO
%attr(755,root,root) %{_libdir}/libipp-core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libipp-core.so.0
%attr(755,root,root) %{_libdir}/libipp-listener.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libipp-listener.so.0
%attr(755,root,root) %{_libdir}/libpapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpapi.so.0
%attr(755,root,root) %{_libdir}/libpapi-common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpapi-common.so.0
%dir %{_libdir}/papi

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libipp-core.so
%attr(755,root,root) %{_libdir}/libipp-listener.so
%attr(755,root,root) %{_libdir}/libpapi.so
%attr(755,root,root) %{_libdir}/libpapi-common.so
%{_libdir}/libipp-core.la
%{_libdir}/libipp-listener.la
%{_libdir}/libpapi.la
%{_libdir}/libpapi-common.la
%{_includedir}/papi
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libipp-core.a
%{_libdir}/libipp-listener.a
%{_libdir}/libpapi.a
%{_libdir}/libpapi-common.a
