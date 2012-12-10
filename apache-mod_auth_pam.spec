#Module-Specific definitions
%define mod_name mod_auth_pam
%define mod_conf A48_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary: 	Pam authorisation for Apache
Name: 		apache-%{mod_name}
Version: 	1.1.1
Release: 	11
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

%{_bindir}/apxs -c %{mod_name}.c -o %{mod_name}.la -lpam
%{_bindir}/apxs -c mod_auth_sys_group.c -o mod_auth_sys_group.la -lpam

%install

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

%files
%doc INSTALL README doc/configure.html doc/faq.html doc/install.html shadow.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pam.d/httpd
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_*.so


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-11mdv2012.0
+ Revision: 772571
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-10
+ Revision: 678267
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-9mdv2011.0
+ Revision: 587925
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-8mdv2010.1
+ Revision: 516051
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-7mdv2010.0
+ Revision: 406542
- rebuild

* Thu Dec 20 2007 Olivier Blin <blino@mandriva.org> 1.1.1-6mdv2009.1
+ Revision: 135820
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-6mdv2008.0
+ Revision: 82524
- rebuild

* Mon Jul 23 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-5mdv2008.0
+ Revision: 54701
- bump release

* Mon Jul 23 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-4mdv2008.0
+ Revision: 54700
- fix #27623


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-3mdv2007.1
+ Revision: 140616
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-2mdv2007.0
+ Revision: 79328
- Import apache-mod_auth_pam

* Mon Jul 24 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1.1.1-2mdv2007.0
- Fix for new PAM

* Mon Jan 30 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-1mdk
- built for apache-2.2.0

* Fri Jan 20 2006 Nicolas Lécureuil <neoclust@mandriva.org> 1:1.1.1-2mdk
- Add BuildRequires

* Thu Jan 19 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.1.1-1mdk
- fix versioning and deps

* Tue Jun 07 2005 Oden Eriksson <oeriksson@mandriva.com> 1.3.33_1.1.1-1mdk
- renamed to apache1-mod_auth_pam and reworked it quite a bit

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.1-10mdk
- spec file cleanups, remove the ADVX-build stuff

* Sun Nov 21 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.1-9mdk
- built for apache 1.3.33

* Fri Jun 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.1.1-8mdk
- built for apache 1.3.31

