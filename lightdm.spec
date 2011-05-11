Summary:	A lightweight display manager
Summary(hu.UTF-8):	Egy könnyűsúlyú bejelentkezéskezelő
Name:		lightdm
Version:	0.3.3
Release:	0.1
License:	GPL v3
Group:		X11/Applications
Source0:	http://people.ubuntu.com/~robert-ancell/lightdm/releases/%{name}-%{version}.tar.gz
# Source0-md5:	13f33b7693e58ba99f47ff5e7f7cbfb2
Source1:	%{name}.pamd
URL:		https://launchpad.net/lightdm
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	autoconf
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	gtk-webkit-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libxklavier-devel
BuildRequires:	pam-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	vala
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         skip_post_check_so	liblightdm-qt-0.so.0.0.0

%description
An X display manager that:
 - Has a lightweight codebase
 - Is standards compliant (PAM, ConsoleKit, etc)
 - Has a well defined interface between the server and user interface
 - Fully themeable (easiest with the webkit interface)
 - Cross-desktop (greeters can be written in any toolkit)

%description -l hu.UTF-8
Egy X bejelentkezéskezelő, amely:
 - pehelysúlyú kóddal rendelkezik
 - követi a standardokat (PAM, ConsoleKit, stb.)
 - jól-definiált felület a szerver és a felhasználói felület között
 - teljesen témázható (a legkönnyebb a webkit felülettel)
 - desktop-független (üdvözlők bármilyen eszközkészlettel írhatók)

%package themes-core
Summary:	Core themes for lightdm
Summary(hu.UTF-8):	Alap témák a lightdm-hez
Group:		Themes

%description themes-core
Core themes for lightdm.

%description themes-core -l hu.UTF-8
Alap témák a lightdm-hez.

%package static
Summary:	Static library for lightdm development
Group:		Development/Libraries

%description static
Static library for lightdm development.

%package devel
Summary:	Header files for lightdm development
Group:		Development/Libraries

%description devel
Header files for lightdm development.

%package apidocs
Summary:	lightdm API documentation
Group:		Documentation

%description apidocs
lightdm API documentation.

%package upstart
Summary:	Upstart job for lightdm
Summary(hu.UTF-8):	Upstart támogatás lightdm-hez
Group:		Daemons

%description upstart
Upstart job for lightdm.

%description upstart -l hu.UTF-8
Upstart támogatás lightdm-hez.

%prep
%setup -q

%build
install -d m4
%{__gtkdocize}
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--with-theme-dir=%{_datadir}/%{name}/themes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{pam.d,security} \
	$RPM_BUILD_ROOT/var/log/lightdm
install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/lightdm
touch $RPM_BUILD_ROOT/etc/security/blacklist.lightdm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post upstart
%upstart_post lightdm

%postun upstart
%upstart_postun lightdm

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/liblightdm-gobject-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-gobject-0.so.0
%attr(755,root,root) %{_libdir}/liblightdm-qt-0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-qt-0.so.0
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/themes
%{_libdir}/girepository-1.0/LightDM-0.typelib
%{_mandir}/man1/lightdm*
/etc/dbus-1/system.d/org.lightdm.LightDisplayManager.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lightdm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.lightdm
%attr(750,root,root) /var/log/lightdm

%files themes-core
%defattr(644,root,root,755)
%{_datadir}/%{name}/themes/example-gtk-gnome
%{_datadir}/%{name}/themes/example-python-gtk-gnome
%{_datadir}/%{name}/themes/example-qt-kde
%{_datadir}/%{name}/themes/example-vala-gtk-gnome
%attr(755,root,root) %{_libdir}/lightdm-example-gtk-greeter
%attr(755,root,root) %{_libdir}/lightdm-example-python-gtk-greeter
%attr(755,root,root) %{_libdir}/lightdm-example-qt-greeter
%attr(755,root,root) %{_libdir}/lightdm-example-vala-gtk-greeter
%{_datadir}/lightdm-example-gtk-greeter/greeter.ui
# %attr(755,root,root) %{_libdir}/ldm-webkit-greeter

%files static
%defattr(644,root,root,755)
%{_libdir}/liblightdm-gobject-0.a
%{_libdir}/liblightdm-qt-0.a

%files devel
%defattr(644,root,root,755)
%{_libdir}/liblightdm-gobject-0.la
%attr(755,root,root) %{_libdir}/liblightdm-gobject-0.so
%{_libdir}/liblightdm-qt-0.la
%attr(755,root,root) %{_libdir}/liblightdm-qt-0.so
%{_includedir}/lightdm-gobject-0
%{_includedir}/lightdm-qt-0
%{_pkgconfigdir}/liblightdm-gobject-0.pc
%{_pkgconfigdir}/liblightdm-qt-0.pc
%{_datadir}/gir-1.0/LightDM-0.gir
%{_datadir}/vala/vapi/liblightdm-gobject-0.vapi

%files apidocs
%defattr(644,root,root,755)
%{_datadir}/gtk-doc/html/lightdm-gobject-0

%files upstart
%defattr(644,root,root,755)
# missing config noreplace?
%{_sysconfdir}/init/%{name}.conf
