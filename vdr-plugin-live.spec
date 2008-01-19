
%define plugin	live
%define name	vdr-plugin-%plugin
%define version	0.1.0
%define rel	1

Summary:	VDR plugin: Live Integrated VDR Environment
Name:		%name
Version:	%version
Release:	%mkrel %rel
Group:		Video
License:	GPLv2+
URL:		http://live.vdr-developer.org/
Source:		http://live.vdr-developer.org/downloads/vdr-%plugin-%version.tar.gz
# From e-tobi repository:
Patch0:		91_timer-delete-fix.dpatch
Patch1:		92_live-0.1.0-1.5.3.dpatch
Patch2:		01_tnt-1.6.0.dpatch
# (Anssi 01/2008) Fix trivial build issues with tntnet 1.6.1:
# This patch is not enough to get it to work.
Patch3:		live-tntnet-1.6.1.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.4.7-9
Requires:	vdr-abi = %vdr_abi
BuildRequires:	tntnet-devel
BuildRequires:	boost-devel
BuildRequires:	openssl-devel
BuildRequires:	epgsearch-devel

%description
Live, the "Live Interactive VDR Environment", is a plugin providing
the possibility to interactively control the VDR and some of its
plugins by a web interface.

Unlike external utility programs that communicate with VDR and its
plugins by SVDRP, Live has direct access to VDR's data structures
and is thus very fast.

%prep
%setup -q -c
cd %plugin
%patch0 -p1
%patch1 -p1
%patch2 -p1
#patch3 -p1

# epgsearch-devel
rm -rf epgsearch
sed -i 's,"epgsearch/services.h",<vdr/epgsearch/services.h>,' epgsearch.cpp

%vdr_plugin_params_begin %plugin
# use PORT to listen for incoming connections instead of 8008
var=PORT
param="-p PORT"
# bind server only to specified IP
# multiple IPs can be separated with a space
var=BIND_IP
param=--ip=MULTIPLE_PARAMS
%vdr_plugin_params_end

%build
cd %plugin
# (01/2008) parallel build broken
%vdr_plugin_build -j1

%install
rm -rf %{buildroot}
cd %plugin
%vdr_plugin_install

install -d -m755 %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}
touch %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}/httpd.config
touch %{buildroot}%{_vdr_plugin_cfgdir}/%{plugin}/httpd.properties

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin/%plugin.vdr
%defattr(-,root,root)
%doc %plugin/CONTRIBUTORS %plugin/HISTORY %plugin/README
%dir %attr(-,vdr,vdr) %{_vdr_plugin_cfgdir}/%{plugin}
%ghost %{_vdr_plugin_cfgdir}/%{plugin}/httpd.config
%ghost %{_vdr_plugin_cfgdir}/%{plugin}/httpd.properties
