# Yggdrasil RPM

This is a specification file used to build RPMs for RiV-mesh.


---
**There's no need to build the package yourself**, if you're using CentOS/RedHat >= 7 or Fedora >= 29. You can find pre-built packages on Fedora COPR.

* Fedora COPR page: https://copr.fedorainfracloud.org/coprs/leisteth/RiV-mesh/
* RiV-mesg installation instructions: https://riv-mesh.github.io/installation-linux-rpm.html

---


## How-to (General)

This assumes you have Go 1.11 or later installed.

Start by installing `rpmbuild`:
```
dnf install rpmbuild
```

Create the working folders:
```
mkdir -p /tmp/rpmbuild/BUILD /tmp/rpmbuild/RPMS /tmp/rpmbuild/SOURCES /tmp/rpmbuild/SPECS /tmp/rpmbuild/SRPMS
```

Place the `mesh.spec` file into `/tmp/rpmbuild/SPECS`.

Download the sources for the specified version, e.g. `v0.3.5`:
```
curl -o /tmp/rpmbuild/SOURCES/v0.4.0 https://codeload.github.com/RiV-chain/RiV-mesh/tar.gz/v0.4.0
```

Build the RPM:
```
cd /tmp/rpmbuild/
rpmbuild -v -bb SPECS/mesh.spec
```



## Build package on Fedora using mock

Make sure you have rpmbuild and mock installed:

```bash
sudo dnf install rpmbuild mock
```

Download all sources defined in SPEC file:

```bash
spectool -g -R mesh.spec
```

Create a SRPM (source RPM) package from the SPEC file:

```bash
rpmbuild -bs mesh.spec
```

Create RPM package in an isolated environment using `mock`:

```bash
mock -r fedora-30-x86_64 --rebuild ~/rpmbuild/SRPMS/mesh-0.4.0-1.fc30.src.rpm --old-chroot
```

*(--old-chroot is needed because it enables internet connection in the build environment)*

You will find your package in `/var/lib/mock/fedora-29-x86_64/result`.
