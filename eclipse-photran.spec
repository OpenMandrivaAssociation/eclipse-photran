%define gcj_support             1
%define major                   4
%define minor                   0       
%define majmin                  %{major}.%{minor}
%define eclipse_base            %{_datadir}/eclipse
%define eclipse_lib_base        %{_libdir}/eclipse

# All arches line up except i386 -> x86
%ifarch %{ix86}
%define eclipse_arch    x86
%else
%define eclipse_arch   %{_arch}
%endif

Summary:        Eclipse Fortran Development Tools (Photran) plugin
Name:           eclipse-photran
Version:        %{majmin}
Release:        %mkrel 0.b3.1.1
License:        EPL
Group:          Development/Java
URL:            http://www.eclipse.org/photran
Requires:       eclipse-platform

# The following tarball was generated like this:
#
# cvs -d :pserver:anonymous@dev.eclipse.org:/cvsroot/technology export -r v20071108_4_0_0_Beta3 org.eclipse.photran
# rm -rf org.eclipse.photran/*.analysis org.eclipse.photran/*.debug.* org.eclipse.photran/*.launch org.eclipse.photran/*.refactoring* org.eclipse.photran/org.eclipse.photran.intel-feature org.eclipse.photran/org.eclipse.photran.vpg-feature
# tar czf org.eclipse.photran.tar.gz org.eclipse.photran
#
Source0: org.eclipse.photran.tar.gz
BuildRequires: eclipse-pde
BuildRequires: eclipse-cdt >= 4.0.1
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel >= 1.0.64
%endif

BuildRequires:  java-rpmbuild
Requires:       gdb make gcc-gfortran
Requires:       eclipse-platform >= 1:3.3.0

# Currently, upstream CDT only supports building on the platforms listed here.
%if %{gcj_support}
ExclusiveArch: %{ix86} x86_64 ppc ia64
%else
ExclusiveArch: %{ix86} x86_64 ppc ia64
%endif
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 


%description
The eclipse-photran package contains the Photran Eclipse feature and plugins
that are useful for Fortran development.


%prep
%setup -q -n org.eclipse.photran
# Fixup to use 1.5 source level
find -name \*.prefs | xargs sed -i -e 's/source=1.3/source=1.5/'


%build
#export JAVA_HOME=%{java_home}
#export PATH=%{java_home}/bin:%{java_home}/jre/bin:/usr/bin:$PATH

# See comments in the script to understand this.
/bin/sh -x %{eclipse_base}/buildscripts/copy-platform SDK %{eclipse_base} cdt
SDK=$(cd SDK >/dev/null && pwd)

# Eclipse may try to write to the home directory.
mkdir home
homedir=$(cd home > /dev/null && pwd)

%{java} -cp $SDK/startup.jar \
        -Dosgi.sharedConfiguration.area=%{eclipse_lib_base}/configuration                        \
        -Duser.home=$homedir                        \
        org.eclipse.core.launcher.Main             \
        -application org.eclipse.ant.core.antRunner       \
        -Dtype=feature                                    \
        -Did=org.eclipse.photran_feature                  \
        -DsourceDirectory=$(pwd)                          \
        -DbuildDirectory=$(pwd)/build                     \
        -DbaseLocation=$SDK                               \
        -DjavacSource=1.5 \
        -DjavacTarget=1.5 \
        -Dbuilder=%{eclipse_base}/plugins/org.eclipse.pde.build/templates/package-build  \
        -f %{eclipse_base}/plugins/org.eclipse.pde.build/scripts/build.xml 


%install
rm -rf ${RPM_BUILD_ROOT}

install -d -m755 ${RPM_BUILD_ROOT}/%{eclipse_base}

unzip -d ${RPM_BUILD_ROOT}/%{_datadir} build/rpmBuild/org.eclipse.photran_feature.zip

# We move arch-specific plugins to libdir.
mkdir -p ${RPM_BUILD_ROOT}%{eclipse_lib_base}/plugins
for archplugin in $(find ${RPM_BUILD_ROOT}%{eclipse_base}/plugins -name \*%{eclipse_arch}_%{version}\*); do
  mv $archplugin ${RPM_BUILD_ROOT}%{eclipse_lib_base}/plugins
  chmod -R 755 ${RPM_BUILD_ROOT}%{eclipse_lib_base}/plugins/$(basename $archplugin)
done

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif


%clean 
rm -rf ${RPM_BUILD_ROOT}


%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif


%files
%defattr(-,root,root)
%doc org.eclipse.photran-feature/epl-v10.html
%{eclipse_base}/plugins/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(0755,root,root) %{_libdir}/gcj/%{name}/*
%endif


