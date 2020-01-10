%global site_name org.apache.felix.bundlerepository
%global grp_name  felix

Name:           felix-bundlerepository
Version:        1.6.6
Release:        14%{?dist}
Summary:        Bundle repository service
License:        ASL 2.0 and MIT
URL:            http://felix.apache.org/site/apache-felix-osgi-bundle-repository.html

Source0:        http://www.fightrice.com/mirrors/apache/felix/org.apache.felix.bundlerepository-%{version}-source-release.tar.gz
Patch1:         0001-Unbundle-libraries.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.sf.kxml:kxml2)
BuildRequires:  mvn(org.apache.felix:felix-parent)
BuildRequires:  mvn(org.apache.felix:org.apache.felix.shell)
BuildRequires:  mvn(org.apache.felix:org.apache.felix.utils)
BuildRequires:  mvn(org.apache.felix:org.osgi.service.obr)
BuildRequires:  mvn(org.codehaus.woodstox:woodstox-core-asl)
BuildRequires:  mvn(org.osgi:org.osgi.compendium)
BuildRequires:  mvn(org.osgi:org.osgi.core)
BuildRequires:  mvn(xpp3:xpp3)
%{?fedora:BuildRequires: mvn(org.easymock:easymock)}


%description
Bundle repository service

%package javadoc
Summary:          API documentation for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{site_name}-%{version}
%patch1 -p1

# Parent POM pulls in unneeded dependencies (mockito)
%pom_remove_parent
%pom_xpath_inject "pom:project" "<groupId>org.apache.felix</groupId>"
%pom_add_dep junit:junit::test
%if 0%{?fedora}
  # easymock is test dependency
  %pom_xpath_inject "pom:dependency[pom:artifactId[text()='easymock']]" "<scope>test</scope>"
%else
  %pom_remove_dep org.easymock:easymock
%endif

%if !0%{?fedora}
  # These tests won't work without easymock3
  rm -f src/test/java/org/apache/felix/bundlerepository/impl/RepositoryAdminTest.java
  rm -f src/test/java/org/apache/felix/bundlerepository/impl/RepositoryImplTest.java
  rm -f src/test/java/org/apache/felix/bundlerepository/impl/StaxParserTest.java
  rm -f src/test/java/org/apache/felix/bundlerepository/impl/ResolverImplTest.java
%endif

# Add xpp3 dependency (upstream bundles this)
%pom_add_dep "xpp3:xpp3:1.1.3.4.O" pom.xml "<optional>true</optional>"

# Make felix utils mandatory dep
%pom_xpath_remove "pom:dependency[pom:artifactId[text()='org.apache.felix.utils']]/pom:optional"

# For compatibility reasons
%mvn_file : felix/%{name}

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE LICENSE.kxml2 NOTICE DEPENDENCIES

%files javadoc -f .mfiles-javadoc
%doc LICENSE LICENSE.kxml2 NOTICE

%changelog
* Wed Jul 17 2013 Michal Srb <msrb@redhat.com> - 1.6.6-14
- Fix license tag. kxml is licensed under MIT, not BSD

* Tue Jul 09 2013 Michal Srb <msrb@redhat.com> - 1.6.6-13
- Make easymock and junit test-only dependencies

* Tue Jul 09 2013 Michal Srb <msrb@redhat.com> - 1.6.6-12
- Run some tests only contidionally
- Remove unneeded BR: mockito

* Wed Jul 03 2013 Michal Srb <msrb@redhat.com> - 1.6.6-11
- Build with XMvn
- Replace patches with %%pom_ macros
- Fix BR

* Wed Jul 03 2013 Michal Srb <msrb@redhat.com> - 1.6.6-10
- Fix BR (Resolves: #979500)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.6.6-8
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.6.6-6
- Make felix-utils mandatory dep in pom.xml

* Mon Apr 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.6-5
- Unbundle libraries
- Add dependency on xpp3
- Include NOTICE in javadoc package
- Resolves #817581

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Jaromir Capik <jcapik@redhat.com> - 1.6.6-3
- osgi.org groupId patch removed (fixed in felix-osgi-* packages)

* Thu Oct 06 2011 Jaromir Capik <jcapik@redhat.com> - 1.6.6-2
- Depmap removed (not needed anymore)
- woodstox-core-asl renamed to woodstox-core

* Tue Sep 14 2011 Jaromir Capik <jcapik@redhat.com> - 1.6.6-1
- Initial packaging
