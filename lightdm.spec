Summary:	A lightweight display manager
Summary(hu.UTF-8):	Egy könnyűsúlyú bejelentkezéskezelő
Name:		lightdm
Version:	0.2.2
Release:	0.1
License:	GPL v3
Group:		X11/Applications
Source0:	http://launchpad.net/lightdm/trunk/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	143cd786a28e93ed2728b0b4afe7068d
URL:		https://launchpad.net/lightdm
BuildRequires:	QtDBus-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-webkit-devel
BuildRequires:	intltool
BuildRequires:	libxklavier-devel
BuildRequires:	pam-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	perl-base
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
Summary(hu.UTF-8):	Alap témák a ligthdm-hez
Group:		Themes

%description themes-core
Core themes for lightdm.

%description themes-core -l hu.UTF-8
Alap témák a ligthdm-hez.


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
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-theme-dir=%{_datadir}/%{name}/themes
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post upstart
%upstart_post lightdm

%postun upstart
%upstart_postun lightdm

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%{_libdir}/liblightdm-gobject-0.so.0.0.0
%{_libdir}/liblightdm-qt-0.so.0.0.0
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/themes
%{_libdir}/girepository-1.0/LightDM-0.typelib
%{_mandir}/man1/lightdm*
/etc/dbus-1/system.d/org.lightdm.LightDisplayManager.conf
%{_sysconfdir}/%{name}.conf

%files themes-core
%defattr(644,root,root,755)
%{_datadir}/%{name}/themes/gnome
%{_libdir}/ldm-gtk-greeter
%{_datadir}/%{name}/themes/webkit
%{_libdir}/ldm-webkit-greeter

%files static
%defattr(644,root,root,755)
%{_libdir}/liblightdm-gobject-0.a
%{_libdir}/liblightdm-qt-0.a

%files devel
%defattr(644,root,root,755)
%{_libdir}/liblightdm-gobject-0.la
%{_libdir}/liblightdm-qt-0.la
%{_includedir}/lightdm-gobject-0
%{_includedir}/lightdm-qt-0
%{_pkgconfigdir}/liblightdm-gobject-0.pc
%{_pkgconfigdir}/liblightdm-qt-0.pc
%{_datadir}/gir-1.0/LightDM-0.gir

%files apidocs
%defattr(644,root,root,755)
%{_datadir}/gtk-doc/html/lightdm-gobject-0

%files upstart
%defattr(644,root,root,755)
%{_sysconfdir}/init/%{name}.conf
