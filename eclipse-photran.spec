%{?_javapackages_macros:%_javapackages_macros}

%global eclipse_base            %{_datadir}/eclipse
%global cdtreq                  1:8.1.0
%global photran_git_tag         accb92132f3474bdc8c241ba86990d65dc68b970
%global photran_build_id        201505301604

Summary:        Fortran Development Tools (Photran) for Eclipse
Name:           eclipse-photran
Version:        9.1.0
Release:        2
License:        EPL
Group:          Development/Tools
URL:            https://www.eclipse.org/ptp

# The following tarballs were downloaded from the git repositories
Source0:        http://git.eclipse.org/c/ptp/org.eclipse.photran.git/snapshot/org.eclipse.photran-%{photran_git_tag}.tar.bz2

BuildRequires:  maven-local
BuildRequires:  tycho
BuildRequires:  eclipse-cdt >= %{cdtreq}
BuildRequires:  eclipse-license
BuildArch:      noarch
Requires:       eclipse-cdt >= %{cdtreq}

%description
An Eclipse-based Integrated Development Environment for Fortran.


%package intel
Summary:        Intel Fortran compiler support for Photran
Group:          Development/Java
Requires:       eclipse-photran = %{version}-%{release}

%description intel
This feature packages the plugins required to support
the Intel Fortran compiler in Photran/FDT.


%package xlf
Summary:        IBM XLF Compiler Support
Group:          Development/Java
Requires:       eclipse-photran = %{version}-%{release}

%description xlf
Error parser and managed build tool chain for the IBM XLF compiler.


%prep
%setup -q -n org.eclipse.photran-%{photran_git_tag}

# We need to rebuild this jar from the sources within it
pwd
mkdir cdtdb-4.0.3-eclipse
pushd cdtdb-4.0.3-eclipse
unzip -q ../org.eclipse.photran.core.vpg/lib/cdtdb-4.0.3-eclipse.jar
find -name \*.class -exec rm {} +
popd
# Delete any other jars in the project
find -name \*.jar -exec rm {} +
# This prevents the Photran Intel feature from building
sed -i -e 's/os="linux"//' org.eclipse.photran.intel-feature/feature.xml
#Fix line endings, causes problems with pdebuild link names
#find -name MANIFEST.MF -exec sed -i -e 's|\r||' {} +


%build
export JAVA_HOME=%{java_home}
export PATH=/usr/bin:$PATH
# Build the helper jar first
pushd cdtdb-4.0.3-eclipse
classpath=$(echo /usr/lib*/eclipse/plugins/org.eclipse.equinox.common_*.jar | sed -e 's/ /:/g')
find -name \*java -exec javac -classpath $classpath '{}' +
jar cf ../org.eclipse.photran.core.vpg/lib/cdtdb-4.0.3-eclipse.jar *
popd
#Interferes with feature build
rm -rf cdtdb-4.0.3-eclipse
# Build the projects
xmvn -o -DforceContextQualifier=%{photran_build_id} verify


%install
mkdir -p %{buildroot}%{eclipse_base}/dropins/photran/eclipse/{features,plugins}

# Features
for jar in org.eclipse.photran.repo/target/repository/features/*.jar
do
  name=$(basename $jar .jar)
  unzip -u -d %{buildroot}%{eclipse_base}/dropins/photran/eclipse/features/$name $jar
  sed -ne '/id=/s#.*"\(.*\)"#%{eclipse_base}/dropins/photran/eclipse/plugins/\1_*.jar#gp' %{buildroot}%{eclipse_base}/dropins/photran/eclipse/features/$name/feature.xml | tail -n +2 > files.$name
done
# Plugins
cp -u org.eclipse.photran.repo/target/repository/plugins/*.jar \
   %{buildroot}%{eclipse_base}/dropins/photran/eclipse/plugins/


%files -f files.org.eclipse.photran_%{version}.%{photran_build_id}
%doc org.eclipse.photran-feature/epl-v10.html
%dir %{eclipse_base}/dropins/photran
%dir %{eclipse_base}/dropins/photran/eclipse
%dir %{eclipse_base}/dropins/photran/eclipse/features
%dir %{eclipse_base}/dropins/photran/eclipse/plugins
%{eclipse_base}/dropins/photran/eclipse/features/org.eclipse.photran_*

%files intel -f files.org.eclipse.photran.intel_%{version}.%{photran_build_id}
%doc org.eclipse.photran-feature/epl-v10.html
%{eclipse_base}/dropins/photran/eclipse/features/org.eclipse.photran.intel_*

%files xlf -f files.org.eclipse.photran.xlf_%{version}.%{photran_build_id}
%doc org.eclipse.photran-feature/epl-v10.html
%{eclipse_base}/dropins/photran/eclipse/features/org.eclipse.photran.xlf_*


%changelog
* Thu Jun 25 2015 Orion Poplawski <orion@cora.nwra.com> - 9.1.0-1
- Update to 9.1.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 9 2015 Orion Poplawski <orion@cora.nwra.com> - 9.0.1-1
- Update to 9.0.1

* Wed Oct 15 2014 Orion Poplawski <orion@cora.nwra.com> - 9.0.0-1
- Update to 9.0.0

* Wed Aug 20 2014 Orion Poplawski <orion@cora.nwra.com> - 8.2.1-1
- Update to 8.2.1

* Wed Jul 2 2014 Alexander Kurtakov <akurtako@redhat.com> 8.2.0-1
- Update to 8.2.0.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 8 2014 Orion Poplawski <orion@cora.nwra.com> - 8.1.4-1
- Update to 8.1.4

* Fri Aug 16 2013 Orion Poplawski <orion@cora.nwra.com> - 8.1.3-1
- Update to 8.1.3

* Sat Aug 3 2013 Orion Poplawski <orion@cora.nwra.com> - 8.1.2-1
- Update to 8.1.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 8 2013 Orion Poplawski <orion@cora.nwra.com> - 8.1.1-1
- Update to 8.1.1

* Mon Jul 8 2013 Orion Poplawski <orion@cora.nwra.com> - 8.1.0-1
- Update to 8.1.0

* Fri May 10 2013 Orion Poplawski <orion@cora.nwra.com> - 8.1.0-0.3.20130510git71fea65
- Update to current git

* Wed May 1 2013 Orion Poplawski <orion@cora.nwra.com> - 8.1.0-0.2.20130501git71fea65
- Update to current git

* Wed Apr 10 2013 Orion Poplawski <orion@cora.nwra.com> - 8.1.0-0.1.20130409git
- Split photran out of eclipse-ptp package
