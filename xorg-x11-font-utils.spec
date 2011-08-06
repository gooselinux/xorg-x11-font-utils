%define pkgname font-utils

Summary: X.Org X11 font utilities
Name: xorg-x11-%{pkgname}
# IMPORTANT: If package ever gets renamed to something else, remove the Epoch line!
Epoch: 1
Version: 7.2
Release: 10%{?dist}
License: MIT
Group: User Interface/X
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: ftp://ftp.x.org/pub/individual/app/bdftopcf-1.0.1.tar.bz2
Source1: ftp://ftp.x.org/pub/individual/app/fonttosfnt-1.0.3.tar.bz2
Source2: ftp://ftp.x.org/pub/individual/app/mkfontdir-1.0.5.tar.bz2
Source3: ftp://ftp.x.org/pub/individual/app/mkfontscale-1.0.7.tar.bz2
Source4: ftp://ftp.x.org/pub/individual/font/font-util-1.0.1.tar.bz2

Patch0: font-util-1.0.1-mapdir-use-datadir-fix.patch
Patch1: font-util-1.0.1-autoconf-add-with-fontdir-option.patch

BuildRequires: pkgconfig(xfont) pkgconfig(x11)
BuildRequires: libfontenc-devel >= 0.99.2-2
BuildRequires: freetype-devel
BuildRequires: zlib-devel
BuildRequires: autoconf

Provides: %{pkgname}
Provides: bdftopcf, fonttosfnt, mkfontdir, mkfontscale, ucs2any

%description
X.Org X11 font utilities required for font installation, conversion,
and generation.

%package -n bdftruncate
Summary: Generate truncated BDF font from ISO 10646-1 encoded BDF font
Group:   Applications/System

%description -n bdftruncate
bdftruncate allows one to generate from an ISO10646-1 encoded BDF font
other ISO10646-1 BDF fonts in which all characters above a threshold
code value are stored unencoded. This is often desirable because the
Xlib API and X11 protocol data structures used for representing font
metric information are extremely inefficient when handling sparsely
populated fonts.

%prep
%setup -q -c %{name}-%{version} -a1 -a2 -a3 -a4
%patch0 -p0 -b .font-util-mapdir-use-datadir-fix
%patch1 -p0 -b .autoconf-add-with-fontdir-option

%build
# Build all apps
{
   for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util ; do
      pushd $app-*
      # FIXME: We run autoconf to activate font-util-0.99.1-mapdir-use-datadir-fix.patch
      case $app in
         font-util)
            autoconf
            ;;
      esac
      %configure
      make
      popd
   done
}

%install
rm -rf $RPM_BUILD_ROOT
# Install all apps
{
    for app in bdftopcf fonttosfnt mkfontdir mkfontscale font-util; do
	pushd $app-*
	make install DESTDIR=$RPM_BUILD_ROOT
	popd
    done
    for i in */README ; do
	[ -s $i ] && cp $i README-$(echo $i | sed 's/-[0-9].*//')
    done
    for i in */COPYING ; do
	grep -q stub $i || cp $i COPYING-$(echo $i | sed 's/-[0-9].*//')
    done
}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README-* COPYING-*
%{_bindir}/bdftopcf
%{_bindir}/fonttosfnt
%{_bindir}/mkfontdir
%{_bindir}/mkfontscale
%{_bindir}/ucs2any
%dir %{_datadir}/X11/fonts
%dir %{_datadir}/X11/fonts/util
%{_datadir}/X11/fonts/util/map-*
%{_datadir}/aclocal/fontutil.m4
%{_libdir}/pkgconfig/fontutil.pc
%{_mandir}/man1/bdftopcf.1*
%{_mandir}/man1/fonttosfnt.1*
%{_mandir}/man1/mkfontdir.1*
%{_mandir}/man1/mkfontscale.1*
%{_mandir}/man1/ucs2any.1*

%files -n bdftruncate
%defattr(-,root,root,-)
%{_bindir}/bdftruncate
%{_mandir}/man1/bdftruncate.1*


%changelog
* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 7.2-10
- mkfontscale 1.0.7
- mkfontdir 1.0.5

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 7.2-8
- Un-require xorg-x11-filesystem
- Other general spec cleanup.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:7.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 7.2-6
- Fix license tag.

* Mon Jul 07 2008 Adam Jackson <ajax@redhat.com> 7.2-5
- Fix Source url for font-util.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:7.2-4
- Autorebuild for GCC 4.3

* Mon Dec 10 2007 Adam Jackson <ajax@redhat.com> 1:7.2-3
- Move bdftruncate (and its perl dependency) to a subpackage.
- %%doc for the non-empty READMEs and non-stub COPYINGs.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1:7.2-2
- Rebuild for build id

* Thu Apr 26 2007 Adam Jackson <ajax@redhat.com> 1:7.2-1
- bdftopcf 1.0.1
- Superstition bump to 7.2-1

* Mon Mar 26 2007 Adam Jackson <ajax@redhat.com> 1:7.1-5
- mkfontdir 1.0.3

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1:7.1-4.fc7
- fonttosfnt 1.0.3

* Thu Aug 17 2006 Adam Jackson <ajackson@redhat.com> 1:7.1-3
- Remove X11R6 symlinks.

* Fri Jul 14 2006 Adam Jackson <ajackson@redhat.com> 1:7.1-2
- Added fonttosfnt-1.0.1-freetype22-build-fix.patch to fix a build failure
  with new freetype 2.2.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:7.1-1.1
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1:7.1-1
- Update to font-util-1.0.1 from X11R7.1
- Set package version to X11 release the tarballs are based from.

* Thu Apr 26 2006 Adam Jackson <ajackson@redhat.com> 1:1.0.2-2
- Update mkfontdir

* Wed Feb 22 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-3
- Remove "Obsoletes: xorg-x11-font-utils" as the package should not obsolete
  itself.  Leftover from the original package template it seems.  (#182439)

* Fri Feb 17 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-2
- Added with_X11R6_compat macro to conditionalize inclusion of mkfontdir and
  mkfontscale symlinks in the old X11R6 locations, pointing to the X11R7
  binaries.  This will provide backward compatibilty for Fedora Core 5, however
  3rd party developers and rpm package maintainers should update to using the
  new X11R7 locations immediately, as these compatibility links are temporary,
  and will be removed from a future OS release.
- Remove system directories from file manifest to appease the banshees.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1:1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1:1.0.1-1
- Updated all utilities to the versions shipped in X11R7.0.

* Thu Dec 15 2005 Mike A. Harris <mharris@redhat.com> 1:1.0.0-1
- Updated all utilities to version 1.0.0 from X11R7 RC4.
- Updated font-util-1.0.0-mapdir-use-datadir-fix.patch to work with RC4.
- Added font-util-1.0.0-autoconf-add-with-fontdir-option.patch to add a new
  variable "fontdir" to the fontutil.pc file which all of the font packages
  can autodetect and use instead of having to put manual fontdir overrides
  in every single rpm package.

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.2-1
- Updated bdftopcf, fonttosfnt to version 0.99.3, and mkfontdir, mkfontscale,
  and font-util to version 0.99.2 from X11R7 RC3.
- Changed manpage dir from man1x back to man1 due to another upstream change.
- Added fontutil.m4 to file manifest.

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 1:0.99.1-1
- Changed package version to 0.99.1 to match the upstream font-util tarball
  version, and added "Epoch: 1" to the package for upgrades.
- Added font-util-0.99.1-mapdir-use-datadir-fix.patch to fix the font-util
  mapfiles data to install into datadir instead of libdir (#173943)
- Added "Requires(pre): libfontenc >= 0.99.2-2" to force a version of
  libfontenc to be installed that fixes bug #173453, and to also force it
  to be installed before xorg-x11-font-utils in a multi-package rpm
  transaction, which will ensure that when font packages get installed
  during upgrades via anaconda or yum, that the right libfontenc is being
  used by mkfontscale/mkfontdir.
- Added ">= 0.99.2-2" to BuildRequires for libfontenc, as a convenience to
  people rebuilding xorg-x11-font-utils, as they'll need to install the new
  libfontenc now anyway before they can install the font-utils package.

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 6.99.99.902-2
- require newer filesystem (#172610)

* Wed Nov 09 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.902-1
- Updated bdftopcf, fonttosfnt, mkfontdir, mkfontscale to version 0.99.1 from
  X11R7 RC1.

* Wed Nov 09 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-3
- Glob util/map-* files in file manifest.
- Added missing "Obsoletes: xorg-x11-font-utils".
- Added "BuildRequires: pkgconfig".

* Sun Nov 06 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-2
- Added font-util-0.99.1 to package, from X11R7 RC1 release, which provides
  ucs2any, bdftruncate.

* Wed Oct 26 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.901-1
- Updated bdftopcf, fonttosfnt, mkfontdir, mkfontscale to version 0.99.1 from
  X11R7 RC1.
- Bumped package version to 6.99.99.901, the X11R7 RC1 release version tag.
- Updated file manifest to to find the manpages in "man1x".

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 6.99.99.0-1
- Initial build.
