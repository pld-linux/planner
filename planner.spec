#
# TODO:
# - check things in %{_share}/mime
# - separate python and dotnet subpackage
#
# Conditional build:
%bcond_without	pgsql	# without PostgreSQL storage module
%bcond_with	sharp	# without dotnet bindings
#
Summary:	A project management program that can help build plans, and track the progress
Summary(pl):	System zarz±dzania projektem pomocny przy planowaniu i ¶ledzeniu postêpu
Summary(pt_BR):	Planner é um programa para gerenciamento de projetos
Name:		planner
Version:	0.12
Release:	2
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	6d6cb645f87833ba0370847ed62d9400
Patch0:		%{name}-po-fix.patch
Patch1:		%{name}-locale_names.patch
URL:		http://www.imendio.com/projects/planner/
BuildRequires:	XFree86-devel
BuildRequires:	bzip2-devel
%{?with_sharp:BuildRequires:	gtk-sharp-devel}
BuildRequires:	intltool
BuildRequires:	libgda-devel >= 1.0
BuildRequires:	libgnomeprintui-devel >= 2.2.1.1
BuildRequires:	libgnomeui-devel >= 2.0.5
BuildRequires:	libgsf-devel >= 1.4.0
BuildRequires:	libxslt-devel >= 1.0
#BuildRequires:	libXi-devel
%if %{with pgsql}
BuildRequires:	postgresql-devel
%endif
BuildRequires:	python-devel
BuildRequires:	python-pygtk-devel
BuildRequires:	scrollkeeper
Obsoletes:	libmrproject
Obsoletes:	mrproject
Obsoletes:	python-libmrproject
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#define		_noautoreqdep	libplanner-1.so.0

%description
A project management program that can help build project plans, and
track the progress of a project.

%description -l pl
Program wspomagaj±cy zarz±dzanie projektami, tworzenie planów i
¶ledzenie postêpu w wykonaniu projektu.

%description -l pt_BR
Planner é um gerenciador de projetos baseado no GNOME.

%package devel
Summary:	Header files for planner library
Summary(pl):	Pliki nag³ówkowe biblioteki planner
Group:		Development/Libraries
Requires:	%{name} = %{version}
Obsoletes:	libmrproject-devel
Obsoletes:	libmrproject-static

%description devel
Header files for planner library.

%description devel -l pl
Pliki nag³ówkowe biblioteki planner.

%package storage-pgsql
Summary:	PostgreSQL storage module for Planner
Summary(pl):	Modu³ przechowywania danych w bazie PostgreSQL dla Plannera
Group:		Libraries
Requires:	%{name} = %{version}
Obsoletes:	libmrproject-storage-pgsql
Obsoletes:	mrproject-storage-pgsql

%description storage-pgsql
PostgreSQL storage module for Planner application.

%description storage-pgsql -l pl
Modu³ przechowywania danych w bazie PostgreSQL dla Plannera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

mv -f po/{no,nb}.po

%build
%configure \
	--enable-database \
	%{?with_sharp:--enable-dotnet} \
	--enable-gtk-doc \
	--enable-python \
	--enable-python-plugin \
	--enable-timetable
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	HTML_DIR=%{_gtkdocdir} \
	sqldocdir=%{_docdir}/%{name}-%{version} \
	sampledir=%{_examplesdir}/%{name}-%{version} \
	omf_dest_dir=%{_omf_dest_dir}

# useless - modules loaded through gmodule
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*/*.la

rm -f $RPM_BUILD_ROOT%{py_sitedir}/gtk-2.0/*.la

# move provided docs to proper dir
#mv $RPM_BUILD_ROOT%{_docdir}/%{name}/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
#rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

#mv $RPM_BUILD_ROOT%{_datadir}/gtk-doc/* $RPM_BUILD_ROOT%{_gtkdocdir}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libplanner*.so.*.*

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/file-modules
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/storage-modules
%dir %{_libdir}/%{name}/views

%attr(755,root,root) %{_libdir}/%{name}/file-modules/*.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%if %{with pgsql}
%exclude %{_libdir}/%{name}/storage-modules/*sql.so
%endif
%attr(755,root,root) %{_libdir}/%{name}/storage-modules/*.so
%attr(755,root,root) %{_libdir}/%{name}/views/*.so

%attr(755,root,root) %{py_sitedir}/gtk-2.0/planner.so

%{_datadir}/application-registry/*
%{_desktopdir}/*
%{_datadir}/mime-info/*
# check these:
%{_datadir}/mime/application/*.xml
%{_datadir}/mime/packages/*.xml
#
%{_datadir}/%{name}
%dir %{_pixmapsdir}/%{name}
%{_pixmapsdir}/*.png
%{_pixmapsdir}/*/*.png
%{_omf_dest_dir}/*
%{_examplesdir}/%{name}-%{version}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libplanner*.la
%attr(755,root,root) %{_libdir}/libplanner*.so
%{_includedir}/planner-1.0
%{_pkgconfigdir}/*.pc
%{_gtkdocdir}/libplanner

%if %{with pgsql}
%files storage-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/storage-modules/*sql.so
%endif
