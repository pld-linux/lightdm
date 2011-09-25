Summary:	A lightweight display manager
Summary(hu.UTF-8):	Egy könnyűsúlyú bejelentkezéskezelő
Name:		lightdm
Version:	0.9.8
Release:	1
License:	GPL v3
Group:		X11/Applications
Source0:	http://people.ubuntu.com/~robert-ancell/lightdm/releases/%{name}-%{version}.tar.gz
# Source0-md5:	4ca45e83e317b27ea14fe85e05eef0d3
Source1:	%{name}.pamd
Patch0:		%{name}-qt4.patch
Patch1:		%{name}-disable_tests.patch
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
Requires:	lightdm-greeter
Provides:	group(xdm)
Provides:	user(xdm)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package greeter-gtk
Summary:	GTK greeter for lightdm
Group:		Themes
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	lightdm-greeter

%description greeter-gtk
GTK greeter for lightdm.

%package greeter-qt
Summary:	QT greeter for lightdm
Group:		Themes
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	lightdm-greeter

%description greeter-qt
QT greeter for lightdm.

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
%patch0 -p1
%patch1 -p1

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
	--disable-silent-rules \
	--enable-liblightdm-qt \
	--enable-gtk-doc \
	--with-greeter-user=xdm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{pam.d,security,init,dbus-1/system.d} \
	$RPM_BUILD_ROOT/home/services/xdm \
	$RPM_BUILD_ROOT/var/log/lightdm
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/lightdm
touch $RPM_BUILD_ROOT/etc/security/blacklist.lightdm
cp -p data/init/%{name}.conf $RPM_BUILD_ROOT/etc/init

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{lb,wae}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 55 -r -f xdm
%useradd -u 55 -r -d /home/services/xdm -s /bin/false -c "X Display Manager" -g xdm xdm

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post upstart
%upstart_post lightdm

%postun upstart
%upstart_postun lightdm

if [ "$1" = "0" ]; then
	%userremove xdm
	%groupremove xdm
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/keys.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/users.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lightdm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.lightdm
/etc/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%attr(755,root,root) %{_bindir}/dm-tool
%attr(755,root,root) %{_sbindir}/lightdm
%attr(755,root,root) %{_libdir}/liblightdm-gobject-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-gobject-1.so.0
%attr(755,root,root) %{_libdir}/liblightdm-qt-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-qt-1.so.0
%attr(755,root,root) %{_libdir}/lightdm-set-defaults
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/gdmflexiserver
%{_libdir}/girepository-1.0/LightDM-1.typelib
%dir %{_datadir}/xgreeters
%{_mandir}/man1/lightdm*
%attr(750,root,xdm) /var/log/lightdm
%attr(750,xdm,xdm) /home/services/xdm

%files greeter-gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lightdm-gtk-greeter
%{_datadir}/lightdm-gtk-greeter
%{_datadir}/xgreeters/lightdm-gtk-greeter.desktop
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}-gtk-greeter.conf

%files greeter-qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/lightdm-qt-greeter
%{_datadir}/xgreeters/lightdm-qt-greeter.desktop

%files static
%defattr(644,root,root,755)
%{_libdir}/liblightdm-gobject-1.a
%{_libdir}/liblightdm-qt-1.a

%files devel
%defattr(644,root,root,755)
%{_libdir}/liblightdm-gobject-1.la
%attr(755,root,root) %{_libdir}/liblightdm-gobject-1.so
%{_libdir}/liblightdm-qt-1.la
%attr(755,root,root) %{_libdir}/liblightdm-qt-1.so
%{_includedir}/lightdm-gobject-1
%{_includedir}/lightdm-qt-1
%{_pkgconfigdir}/liblightdm-gobject-1.pc
%{_pkgconfigdir}/liblightdm-qt-1.pc
%{_datadir}/gir-1.0/LightDM-1.gir
%{_datadir}/vala/vapi/liblightdm-gobject-1.vapi

%files apidocs
%defattr(644,root,root,755)
%{_datadir}/gtk-doc/html/lightdm-gobject-1

%files upstart
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/init/%{name}.conf
