#Module-Specific definitions
%define mod_name mod_auth_pam
%define mod_conf A48_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary: 	Pam authorisation for Apache
Name: 		apache-%{mod_name}
Version: 	1.1.1
Release: 	%mkrel 9
License: 	LGPL
Group: 		System/Servers
URL: 		http://pam.sourceforge.net/mod_auth_pam/
Source0:	http://pam.sourceforge.net/mod_auth_pam/dist/%{mod_name}-2.0-%{version}.tar.bz2
Source1:	http://pam.sourceforge.net/mod_auth_pam/shadow.html
Source2:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:  pam-devel
BuildRoot: 	%{_tmppath}/%{name}-root

%description
The PAM authentication module implements Basic authentication on 
top of the Pluggable Authentication Module library. Thereby it 
supports standard unix passwd, shadow, NIS, SMB auth and radius 
authentication transparently and easily interchangeable, wherever 
the HTTP protocol allows it.

%prep

%setup -q -n %{mod_name}

cp %{SOURCE1} .
cp %{SOURCE2} %{mod_conf}

chmod 644 INSTALL README doc/configure.html doc/faq.html doc/install.html

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%{_sbindir}/apxs -c %{mod_name}.c -o %{mod_name}.la -lpam
%{_sbindir}/apxs -c mod_auth_sys_group.c -o mod_auth_sys_group.la -lpam

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_sysconfdir}/pam.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

cat > %{buildroot}%{_sysconfdir}/pam.d/httpd << EOF
#%PAM-1.0
auth       include      system-auth
account    include      system-auth
EOF

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL README doc/configure.html doc/faq.html doc/install.html shadow.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/httpd
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_*.so
