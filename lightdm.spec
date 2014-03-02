Summary:	A lightweight display manager
Summary(hu.UTF-8):	Egy könnyűsúlyú bejelentkezéskezelő
Name:		lightdm
Version:	1.7.12
Release:	6
# library/bindings are LGPLv2 or LGPLv3, the rest GPLv3+
License:	(LGPLv2 or LGPLv3) and GPLv3+
Group:		X11/Applications
Source0:	https://launchpad.net/lightdm/1.7/%{version}/+download/%{name}-%{version}.tar.xz
# Source0-md5:	73d6a917ed667a45c194df6c4f270b80
Source1:	%{name}.pamd
Source2:	%{name}-autologin.pamd
Source3:	%{name}-greeter.pamd
Source4:	%{name}.init
Patch0:		config.patch
Patch1:		upstart-path.patch
Patch2:		%{name}-nodaemon_option.patch
URL:		http://www.freedesktop.org/wiki/Software/LightDM
BuildRequires:	QtCore-devel
BuildRequires:	QtDBus-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	autoconf
BuildRequires:	dbus-glib-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.30
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk+2-devel >= 2:2.24
BuildRequires:	gtk-doc
BuildRequires:	gtk-webkit-devel
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	libgcrypt-devel
BuildRequires:	libtool
BuildRequires:	libxklavier-devel
BuildRequires:	pam-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	qt4-build
BuildRequires:	rpmbuild(macros) >= 1.689
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	/usr/bin/X
Requires:	dbus-x11
Requires:	lightdm-greeter
Requires:	xinitrc-ng >= 1.1-2
Provides:	XDM
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

%package libs-gobject
Summary:	LightDM GObject client library
Group:		Libraries
Obsoletes:	lightdm-libs < 1.7.0-0.6

%description libs-gobject
This package contains a GObject based library for LightDM clients to
use to interface with LightDM.

%package libs-gobject-devel
Summary:	Development files for %{name}-gobject
Group:		Development/Libraries
Group:		Libraries
Requires:	%{name}-libs-gobject = %{version}-%{release}

%description libs-gobject-devel
This package contains development files for a GObject based library
for LightDM clients to use to interface with LightDM.

%package libs-qt
Summary:	LightDM Qt client library
Group:		Libraries
Conflicts:	lightdm-libs < 1.7.0-0.6

%description libs-qt
This package contains a Qt based library for LightDM clients to use to
interface with LightDM.

%package libs-qt-devel
Summary:	Development files for %{name}-qt
Group:		Development/Libraries
Requires:	%{name}-libs-qt = %{version}-%{release}

%description libs-qt-devel
This package contains development files for a Qt based library for
LightDM clients to use to interface with LightDM.

%package apidocs
Summary:	lightdm API documentation
Group:		Documentation

%description apidocs
lightdm API documentation.

%package init
Summary:	Init script for Lightdm
Summary(pl.UTF-8):	Skrypt init dla Lightdm-a
Group:		X11/Applications
Requires(post,preun):	/sbin/chkconfig
Requires(post,postun):	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
Obsoletes:	lightdm-upstart < 1.7.12-6
Conflicts:	upstart < 0.6

%description init
Init script for Lightdm.

%description init -l pl.UTF-8
Skrypt init dla Lightdm-a.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--disable-tests \
	--enable-liblightdm-qt \
	--with-html-dir=%{_gtkdocdir} \
	--enable-gtk-doc \
	--with-greeter-session=lightdm-gtk-greeter \
	--with-greeter-user=xdm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{pam.d,security,init,rc.d/init.d,dbus-1/system.d} \
	$RPM_BUILD_ROOT/home/services/xdm \
	$RPM_BUILD_ROOT%{_datadir}/xgreeters \
	$RPM_BUILD_ROOT%{_datadir}/lightdm/remote-sessions \
	$RPM_BUILD_ROOT%{systemdunitdir} \
	$RPM_BUILD_ROOT/var/{log,cache}/lightdm

# initscripts
cp -p data/init/%{name}.conf $RPM_BUILD_ROOT/etc/init
install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/lightdm
ln -s /dev/null $RPM_BUILD_ROOT%{systemdunitdir}/lxdm.service

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/lightdm
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/lightdm-autologin
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/pam.d/lightdm-greeter
touch $RPM_BUILD_ROOT/etc/security/blacklist.lightdm

# We don't ship AppAmor
rm -rv $RPM_BUILD_ROOT/etc/apparmor.d

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{lb,wae}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 55 -r -f xdm
%useradd -u 55 -r -d /home/services/xdm -s /bin/false -c "X Display Manager" -g xdm xdm

%postun
if [ "$1" = "0" ]; then
	%userremove xdm
	%groupremove xdm
fi

%post	libs-gobject -p /sbin/ldconfig
%postun	libs-gobject -p /sbin/ldconfig

%post	libs-qt -p /sbin/ldconfig
%postun	libs-qt -p /sbin/ldconfig

%post init
/sbin/chkconfig --add %{name}
%service -n %{name} restart
%upstart_post %{name}
%systemd_reload

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del %{name}
	%service %{name} stop
fi

%postun init
%systemd_reload
%upstart_postun %{name}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/keys.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/users.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lightdm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lightdm-autologin
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/lightdm-greeter
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.lightdm
/etc/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%attr(755,root,root) %{_bindir}/dm-tool
%attr(755,root,root) %{_sbindir}/lightdm
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/gdmflexiserver
%attr(755,root,root) %{_libdir}/%{name}/lightdm-guest-session-wrapper
%attr(755,root,root) %{_libdir}/%{name}/lightdm-set-defaults
%{_libdir}/girepository-1.0/LightDM-1.typelib
%dir %{_datadir}/xgreeters
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/remote-sessions
%{_mandir}/man1/lightdm*
%dir %attr(710,root,root) /var/cache/lightdm
%dir %attr(710,root,root) /var/log/lightdm
%dir %attr(750,xdm,xdm) /home/services/xdm

%files libs-gobject
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblightdm-gobject-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-gobject-1.so.0

%files libs-qt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblightdm-qt-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblightdm-qt-3.so.0

%files libs-gobject-devel
%defattr(644,root,root,755)
%{_datadir}/gir-1.0/LightDM-1.gir
%{_includedir}/lightdm-gobject-1
%{_pkgconfigdir}/liblightdm-gobject-1.pc
%{_libdir}/liblightdm-gobject-1.la
%attr(755,root,root) %{_libdir}/liblightdm-gobject-1.so
# -vala
%{_datadir}/vala/vapi/liblightdm-gobject-1.vapi

%files libs-qt-devel
%defattr(644,root,root,755)
%{_libdir}/liblightdm-qt-3.la
%attr(755,root,root) %{_libdir}/liblightdm-qt-3.so
%{_includedir}/lightdm-qt-3
%{_pkgconfigdir}/liblightdm-qt-3.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/lightdm-gobject-1

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/init/%{name}.conf
%{systemdunitdir}/lxdm.service
