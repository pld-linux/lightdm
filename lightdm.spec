Summary:	A lightweight display manager
Summary(hu.UTF-8):	Egy könnyűsúlyú bejelentkezéskezelő
Name:		lightdm
Version:	1.1.1
Release:	2
License:	GPL v3
Group:		X11/Applications
Source0:	https://launchpad.net/lightdm/trunk/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	e42e1ac0b07b3591de44ff7b6daa6c7a
Source1:	%{name}.pamd
Patch2:		upstart-path.patch
URL:		http://www.freedesktop.org/wiki/Software/LightDM
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
BuildRequires:	gtk+2-devel >= 2:2.24
BuildRequires:	gtk-doc
BuildRequires:	gtk-webkit-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	libxklavier-devel
BuildRequires:	pam-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	vala
Requires:	lightdm-greeter
Provides:	group(xdm)
Provides:	user(xdm)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# TODO: fix this
#Unresolved symbols found in: liblightdm-qt-2.so.0.0.0
#        QPixmap::~QPixmap()
#        QPixmap::operator QVariant() const
#        QPixmap::QPixmap(QString const&, char const*, QFlags<Qt::ImageConversionFlag>)
%define		skip_post_check_so	liblightdm-qt-2.so.0.0.0

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

%package libs
Summary:	lightdm libraries
Group:		Libraries
Conflicts:	lightdm < 1.1.1-2

%description libs
lightdm libraries.

%package static
Summary:	Static library for lightdm development
Group:		Development/Libraries

%description static
Static library for lightdm development.

%package devel
Summary:	Header files for lightdm development
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

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
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	upstart >= 0.6

%description upstart
Upstart job for lightdm.

%description upstart -l hu.UTF-8
Upstart támogatás lightdm-hez.

%prep
%setup -q
%patch2 -p1

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
	--disable-tests \
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
	$RPM_BUILD_ROOT%{_datadir}/xgreeters \
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

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

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
%doc AUTHORS ChangeLog NEWS README TODO
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/keys.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/users.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lightdm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.lightdm
# XXX: move /etc/apparmor.d to filesystem package or make apparmor subpackage here
%dir /etc/apparmor.d
/etc/apparmor.d/lightdm-guest-session
/etc/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%attr(755,root,root) %{_bindir}/dm-tool
%attr(755,root,root) %{_sbindir}/lightdm
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/gdmflexiserver
%attr(755,root,root) %{_libdir}/%{name}/lightdm-guest-session-wrapper
%attr(755,root,root) %{_libdir}/%{name}/lightdm-set-defaults
%{_libdir}/girepository-1.0/LightDM-1.typelib
%dir %{_datadir}/xgreeters
%{_mandir}/man1/lightdm*
%attr(750,root,xdm) /var/log/lightdm
%attr(750,xdm,xdm) /home/services/xdm

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblightdm-gobject-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-gobject-1.so.0
%attr(755,root,root) %{_libdir}/liblightdm-qt-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-qt-2.so.0

%files static
%defattr(644,root,root,755)
%{_libdir}/liblightdm-gobject-1.a
%{_libdir}/liblightdm-qt-2.a

%files devel
%defattr(644,root,root,755)
%{_libdir}/liblightdm-gobject-1.la
%attr(755,root,root) %{_libdir}/liblightdm-gobject-1.so
%{_libdir}/liblightdm-qt-2.la
%attr(755,root,root) %{_libdir}/liblightdm-qt-2.so
%{_includedir}/lightdm-gobject-1
%{_includedir}/lightdm-qt-2
%{_pkgconfigdir}/liblightdm-gobject-1.pc
%{_pkgconfigdir}/liblightdm-qt-2.pc
%{_datadir}/gir-1.0/LightDM-1.gir
%{_datadir}/vala/vapi/liblightdm-gobject-1.vapi

%files apidocs
%defattr(644,root,root,755)
%{_datadir}/gtk-doc/html/lightdm-gobject-1

%files upstart
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/init/%{name}.conf
