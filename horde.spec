%define peardir /usr/share/pear
%define xmldir  /var/lib/pear

Summary: PEAR: Horde Application Framework
Name: horde
Version: 5.2.7
Release: 1%{?dist}
License: LGPL-2
Group: Development/Libraries
Source0: http://pear.horde.org/get/horde-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)
URL: http://pear.horde.org/package/horde
BuildRequires:       php-pear(PEAR) >= 1.4.7
BuildRequires: php-channel(pear.horde.org)
Requires: Horde_Role >= 1.0.0
Requires: Horde_Alarm >= 2.0.0
Requires: Horde_Alarm < 3.0.0alpha1
Requires: Horde_Argv >= 2.0.0
Requires: Horde_Argv < 3.0.0alpha1
Requires: Horde_Auth >= 2.0.0
Requires: Horde_Auth < 3.0.0alpha1
Requires: Horde_Autoloader >= 2.0.0
Requires: Horde_Autoloader < 3.0.0alpha1
Requires: Horde_Browser >= 2.0.0
Requires: Horde_Browser < 3.0.0alpha1
Requires: Horde_Core >= 2.0.0
Requires: Horde_Core < 3.0.0alpha1
Requires: Horde_Date >= 2.0.0
Requires: Horde_Date < 3.0.0alpha1
Requires: Horde_Exception >= 2.0.0
Requires: Horde_Exception < 3.0.0alpha1
Requires: Horde_Form >= 2.0.0
Requires: Horde_Form < 3.0.0alpha1
Requires: Horde_Group >= 2.0.0
Requires: Horde_Group < 3.0.0alpha1
Requires: Horde_Http >= 2.0.0
Requires: Horde_Http < 3.0.0alpha1
Requires: Horde_Image >= 2.0.0
Requires: Horde_Image < 3.0.0alpha1
Requires: Horde_LoginTasks >= 2.0.0
Requires: Horde_LoginTasks < 3.0.0alpha1
Requires: Horde_Mail >= 2.0.0
Requires: Horde_Mail < 3.0.0alpha1
Requires: Horde_Mime >= 2.0.0
Requires: Horde_Mime < 3.0.0alpha1
Requires: Horde_Nls >= 2.0.0
Requires: Horde_Nls < 3.0.0alpha1
Requires: Horde_Perms >= 2.0.0
Requires: Horde_Perms < 3.0.0alpha1
Requires: Horde_Prefs >= 2.0.0
Requires: Horde_Prefs < 3.0.0alpha1
Requires: Horde_Rpc >= 2.0.0
Requires: Horde_Rpc < 3.0.0alpha1
Requires: Horde_Serialize >= 2.0.0
Requires: Horde_Serialize < 3.0.0alpha1
Requires: Horde_Support >= 2.0.0
Requires: Horde_Support < 3.0.0alpha1
Requires: Horde_Text_Diff >= 2.0.0
Requires: Horde_Text_Diff < 3.0.0alpha1
Requires: Horde_Token >= 2.0.0
Requires: Horde_Token < 3.0.0alpha1
Requires: Horde_Text_Filter >= 2.0.0
Requires: Horde_Text_Filter < 3.0.0alpha1
Requires: Horde_Tree >= 2.0.0
Requires: Horde_Tree < 3.0.0alpha1
Requires: Horde_Url >= 2.0.0
Requires: Horde_Url < 3.0.0alpha1
Requires: Horde_Util >= 2.0.0
Requires: Horde_Util < 3.0.0alpha1
Requires: Horde_View >= 2.0.0
Requires: Horde_View < 3.0.0alpha1
Requires: Horde_Vfs >= 2.0.0
Requires: Horde_Vfs < 3.0.0alpha1
Requires: php-pear(PEAR) >= 1.7.0
Requires: php-channel(pear.horde.org)
Obsoletes: horde <= 4   
BuildArch: noarch

Provides:       %{name} = %{version}

%description
The Horde Application Framework is a flexible, modular, general-purpose web
application framework written in PHP. It provides an extensive array of
components that are targeted at the common problems and tasks involved in
developing modern web applications. It is the basis for a large number of
production-level web applications, notably the Horde Groupware suites. For
more information on Horde or the Horde Groupware suites, visit
http://www.horde.org.

%prep
%setup -c -T
pear -v -c pearrc \
        -d php_dir=%{peardir} \
        -d doc_dir=%{pear_docdir} \
        -d bin_dir=%{_bindir} \
        -d data_dir=%{peardir}/data \
        -d test_dir=%{peardir}/tests \
        -d ext_dir=%{_libdir} \
        -d horde_dir=%{pear_hordedir} \
        -s

%build

%install
rm -rf %{buildroot}
pear -c pearrc install --nodeps --packagingroot %{buildroot} %{SOURCE0}
        
# Clean up unnecessary files
rm pearrc
rm %{buildroot}/%{peardir}/.filemap
rm %{buildroot}/%{peardir}/.lock
rm -rf %{buildroot}/%{peardir}/.registry
rm -rf %{buildroot}%{peardir}/.channels
rm %{buildroot}%{peardir}/.depdb
rm %{buildroot}%{peardir}/.depdblock


#mv %{buildroot}/docs .

# Install XML package description
mkdir -p %{buildroot}%{xmldir}
tar -xzf %{SOURCE0} package.xml
cp -p package.xml %{buildroot}%{xmldir}/horde.xml

%clean
rm -rf %{buildroot}

%post
pear install --nodeps --soft --force --register-only %{xmldir}/horde.xml >/dev/null || :

%postun
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only pear.horde.org/horde >/dev/null || :
fi

%files
%defattr(-,root,root)
%{peardir}/*
#%attr(750,root,%{apachegroup}) %{pear_hordedir}/config

#%doc docs/horde/*
%doc %{pear_hordedir}
%{xmldir}/horde.xml
%{_bindir}/horde-active-sessions
%{_bindir}/horde-alarms
%{_bindir}/horde-check-logger
%{_bindir}/horde-clear-cache
%{_bindir}/horde-crond
%{_bindir}/horde-db-migrate
%{_bindir}/horde-import-squirrelmail-prefs
%{_bindir}/horde-memcache-stats
%{_bindir}/horde-run-task
%{_bindir}/horde-set-perms
%{_bindir}/horde-themes
%{_bindir}/horde-translation
%{_bindir}/horde-sessions-gc
%{_bindir}/horde-queue-run-tasks
%{_bindir}/horde-remove-user-data
%{_bindir}/horde-pref-remove
%{_bindir}/horde-sql-shell
%{_bindir}/horde-import-openxchange-prefs

%changelog
* Sat Aug 1 2015 John H. Bennett III <bennettj@johnbennettservices.com> - 5.2.7-1
- Updated to 5.2.7

* Thu Jun 18 2015 John H. Bennett III <bennettj@johnbennettservices.com> - 5.2.6-1
- Updated to 5.2.6

* Sat May 2 2015 John H. Bennett III <bennettj@johnbennettservices.com> - 5.2.5-1
- Updated to 5.2.5

* Tue Feb 10 2015 John H. Bennett III <bennettj@johnbennettservices.com> - 5.2.4-1
- Updated to 5.2.4

* Thu Dec 4 2014 John H. Bennett III <bennettj@johnbennettservices.com> - 5.2.3-1
- Updated to 5.2.3

* Wed Oct 29 2014 John H. Bennett III <bennettj@johnbennettservices.com> - 5.2.2-1
- Updated to 5.2.2

* Mon Aug 4 2014 John H. Bennett III <bennettj@johnbennettservices.com> - 5.2.1-1
- Updated to 5.2.1

* Tue Jul 8 2014 John H. Bennett III <bennettj@johnbennettservices.com> - 5.2.0-1
- Updated to 5.2.0

* Fri Mar 7 2014 John H. Bennett III <bennettj@johnbennettservices.com> - 5.1.6-1
- Updated to 5.1.6

* Wed Oct 30 2013 John H. Bennett III <bennettj@johnbennettservices.com> - 5.1.5-1
- Updated to 5.1.5

* Tue Sep 3 2013 John H. Bennett III <bennettj@johnbennettservices.com> - 5.1.4-1
- Updated to 5.1.4

* Mon Jun 3 2013 John H. Bennett III <bennettj@johnbennettservices.com> - 5.0.5-1
- Initial release for SME Server
- Original build from pear make-rpm-spec
