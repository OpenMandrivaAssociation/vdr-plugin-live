
%define plugin	live
%define name	vdr-plugin-%plugin
%define version	0.2.0
%define snapshot 0
%define rel	3

Summary:	VDR plugin: Live Integrated VDR Environment
Name:		%name
Version:	%version
%if %snapshot
Release:	%mkrel 1.%snapshot.%rel
%else
Release:	%mkrel %rel
%endif
Group:		Video
License:	GPLv2+
URL:		http://live.vdr-developer.org/
%if %snapshot
Source:		vdr-%plugin-%snapshot.tar.gz
%define dirname	%plugin
%else
Source:		http://live.vdr-developer.org/downloads/vdr-%plugin-%version.tar.gz
%define dirname	%plugin-%version
%endif
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0
Requires:	vdr-abi = %vdr_abi
BuildRequires:	tntnet-devel
BuildRequires:	boost-devel
BuildRequires:	openssl-devel
BuildRequires:	epgsearch-devel >= 0.9.24

%description
Live, the "Live Interactive VDR Environment", is a plugin providing
the possibility to interactively control the VDR and some of its
plugins by a web interface.

Unlike external utility programs that communicate with VDR and its
plugins by SVDRP, Live has direct access to VDR's data structures
and is thus very fast.

%prep
%setup -q -n %dirname
# epgsearch-devel
rm -rf epgsearch
sed -i 's,"epgsearch/services.h",<vdr/epgsearch/services.h>,' epgsearch.cpp timerconflict.cpp
%vdr_plugin_prep

%vdr_plugin_params_begin %plugin
# use PORT to listen for incoming connections instead of 8008
var=PORT
param="-p PORT"
# bind server only to specified IP
# multiple IPs can be separated with a space
var=BIND_IP
param=--ip=MULTIPLE_PARAMS
# use SSLPORT to listen for incoming ssl connections instead of 8443
var=SSLPORT
param="-s PORT"
# full path to a custom ssl certificate file
var=CERT
param="-c CERT"
default="%{_sysconfdir}/pki/tls/private/vdr-%plugin.pem"
# log level for tntnet (values: INFO, DEBUG,...)
var=LOGLEVEL
param="-l LOGLEVEL"
# directory for epgimages
var=EPGIMAGES
param="-e EPGIMAGES"
default="%{_vdr_epgimagesdir}"
%vdr_plugin_params_end

%build
# (01/2008) parallel build broken
%vdr_plugin_build -j1

%install
rm -rf %{buildroot}
%vdr_plugin_install

install -d -m755 %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}
touch %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}/httpd.config
touch %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}/httpd.properties

install -d -m755 %{buildroot}%{_vdr_plugin_datadir}
cp -a live %{buildroot}%{_vdr_plugin_datadir}/
for dir in %plugin/*; do
	ln -s %{_vdr_plugin_datadir}/$dir %{buildroot}%{_vdr_plugin_cfgdir}/$dir
done

%clean
rm -rf %{buildroot}

%post
%_create_ssl_certificate -g vdr -b vdr-%plugin
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc CONTRIBUTORS HISTORY README
%dir %attr(-,vdr,vdr) %{_vdr_plugin_cfgdir}/%{plugin}
%ghost %{_vdr_plugin_cfgdir}/%{plugin}/httpd.config
%ghost %{_vdr_plugin_cfgdir}/%{plugin}/httpd.properties
%{_vdr_plugin_cfgdir}/%{plugin}/css
%{_vdr_plugin_cfgdir}/%{plugin}/img
%{_vdr_plugin_cfgdir}/%{plugin}/js
%{_vdr_plugin_cfgdir}/%{plugin}/themes
%{_vdr_plugin_datadir}/%{plugin}

