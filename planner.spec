#
# Conditional build:
%bcond_without pgsql	# without PostgreSQL storage module
#
Summary:	A project management program that can help build plans, and track the progress
Summary(pl):	System zarz±dzania projektem pomocny przy planowaniu i ¶ledzeniu postêpu
Summary(pt_BR):	Planner é um programa para gerenciamento de projetos
Name:		planner
Version:	0.11
Release:	0.1
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/0.11/%{name}-%{version}.tar.gz
# Source0-md5:	ce3ee7d4d84695b0edb88a25b55fcf7f
URL:		http://www.imendio.com/projects/planner/
BuildRequires:	libgnomeprintui-devel >= 2.2.1.1
BuildRequires:	libgnomeui-devel >= 2.0.5
Obsoletes:	libmrproject
Obsoletes:	libmrproject-devel
Obsoletes:	libmrproject-static
Obsoletes:	libmrproject-storage-pgsql
Obsoletes:	mrproject
Obsoletes:	python-libmrproject
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A project management program that can help build project plans, and
track the progress of a project.

%description -l pl
Program wspomagaj±cy zarz±dzanie projektami, tworzenie planów i
¶ledzenie postêpu w wykonaniu projektu.

%description -l pt_BR
Planner é um gerenciador de projetos baseado no GNOME.

%package storage-pgsql
Summary:	PostgreSQL storage module for Planner
Summary(pl):	Modu³ przechowywania danych w bazie PostgreSQL dla Plannera
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}

%description storage-pgsql
PostgreSQL storage module for Planner application.

%description storage-pgsql -l pl
Modu³ przechowywania danych w bazie PostgreSQL dla Plannera.

%prep
%setup -q

%build
%configure \
	--enable-timetable
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	omf_dest_dir=%{_omf_dest_dir}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/file-modules
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/storage-modules
%dir %{_libdir}/%{name}/views

%attr(755,root,root) %{_libdir}/%{name}/file-modules/*.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%exclude %{_libdir}/%{name}/storage-modules/*sql.so
%attr(755,root,root) %{_libdir}/%{name}/storage-modules/*.so
%attr(755,root,root) %{_libdir}/%{name}/views/*.so

%{_libdir}/%{name}/file-modules/*.la
%{_libdir}/%{name}/plugins/*.la
%{_libdir}/%{name}/storage-modules/*.la
%exclude %{_libdir}/%{name}/storage-modules/*sql.la
%{_libdir}/%{name}/views/*.la

%{_datadir}/application-registry/*
%{_desktopdir}/*
%{_datadir}/mime-info/*
%{_datadir}/%{name}
%dir %{_pixmapsdir}/%{name}
%{_pixmapsdir}/*.png
%{_pixmapsdir}/*/*.png
%{_omf_dest_dir}/*

%if %{with pgsql}
%files storage-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/storage-modules/*sql.so
%{_libdir}/%{name}/storage-modules/*sql.la
%endif
