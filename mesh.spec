Name:           mesh
Version:        0.4.0.1rc6
Release:        1%{?dist}
Summary:        IoT end-to-end encrypted IPv6 network

License:        GPLv3
URL:            https://github.com/RiV-chain
Source0:        https://codeload.github.com/RiV-chain/RiV-mesh/tar.gz/v%{version}

BuildRequires:  systemd golang >= 1.18 git
Requires(pre):  shadow-utils
Requires(post): /sbin/chkconfig, /sbin/service
Requires(preun): /sbin/chkconfig, /sbin/service
Conflicts:      mesh-develop

%description
RiV-mesh is an implementation of a fully end-to-end encrypted IPv6 network,
created in the scope to produce the Transport Layer for RiV Chain Blockchain,
also to facilitate secure conectivity between a wide spectrum of endpoint devices like IoT devices,
desktop computers or even routers.
It is lightweight, self-arranging, supported on multiple platforms and allows pretty
much any IPv6-capable application to communicate securely with other RiV-mesh nodes.
RiV-mesh does not require you to have IPv6 Internet connectivity - it also works over IPv4.

%pre
getent group mesh >/dev/null || groupadd -r mesh
exit 0

%prep
%setup -qn RiV-mesh-%{version}

%build
export PKGNAME="%{name}"
export PKGVER="%{version}"
export GOPROXY="https://proxy.golang.org,direct"
./build

%install
rm -rf "%{buildroot}"
mkdir -p "%{buildroot}"/%{_datadir}/riv
install -m 0755 -D mesh "%{buildroot}"/%{_bindir}/mesh
install -m 0755 -D meshctl "%{buildroot}"/%{_bindir}/meshctl
install -m 0755 -D contrib/systemd/mesh.service "%{buildroot}"/%{_sysconfdir}/systemd/system/mesh.service
cp -a contrib/ui/mesh-ui/ui "%{buildroot}"/%{_datadir}/riv

%post
/sbin/chkconfig --add mesh >/dev/null 2>/dev/null #supress notes on systemd

if [ "$1" -ge "1" ]; then
    /sbin/service mesh condrestart >/dev/null 2>&1 || :
fi

if [ -f /etc/mesh.conf ]; then
  mkdir -p /var/backups
  echo "Backing up configuration file to /var/backups/mesh.conf.`date +%Y%m%d`"
  cp /etc/mesh.conf /var/backups/mesh.conf.`date +%Y%m%d`
  echo "Normalising and updating /etc/mesh.conf"
  /usr/bin/mesh -useconf -normaliseconf < /var/backups/mesh.conf.`date +%Y%m%d` > /etc/mesh.conf
else
  echo "-----------------------------------------------------------------------------" > /dev/stderr
  echo "  To finish the installation, you need to configure the peers list" > /dev/stderr
  echo "  in the file /etc/mesh.config then run 'service mesh start'." > /dev/stderr
  echo "-----------------------------------------------------------------------------" > /dev/stderr
  echo "Generating initial configuration file /etc/mesh.conf"
  echo "Please familiarise yourself with this file before starting RiV-mesh"
  sh -c 'umask 0027 && /usr/bin/mesh -genconf > /etc/mesh.conf'
fi
chmod 755 /etc/mesh.conf

%preun
if [ $1 = 0 ] ; then
    /sbin/service mesh stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del mesh >/dev/null 2>/dev/null #supress notes on systemd
fi
exit 0

%files
%defattr(-,root,root)
%{_bindir}/mesh
%{_bindir}/meshctl
%{_sysconfdir}/systemd/system/mesh.service
%{_datadir}/riv/ui/index.html
%{_datadir}/riv/ui/country.json
%{_datadir}/riv/ui/webfonts/fa-brands-400.ttf
%{_datadir}/riv/ui/webfonts/fa-brands-400.woff2
%{_datadir}/riv/ui/webfonts/fa-regular-400.ttf
%{_datadir}/riv/ui/webfonts/fa-regular-400.woff2
%{_datadir}/riv/ui/webfonts/fa-solid-900.ttf
%{_datadir}/riv/ui/webfonts/fa-solid-900.woff2
%{_datadir}/riv/ui/webfonts/fa-v4compatibility.ttf
%{_datadir}/riv/ui/webfonts/fa-v4compatibility.woff2
%{_datadir}/riv/ui/assets/all.min.css
%{_datadir}/riv/ui/assets/bulmaswatch.min.css
%{_datadir}/riv/ui/assets/flag-icons.css
%{_datadir}/riv/ui/assets/flag-icons.min.css
%{_datadir}/riv/ui/assets/mesh-ui-es5.js
%{_datadir}/riv/ui/assets/mesh-ui.css
%{_datadir}/riv/ui/assets/mesh-ui.js
%{_datadir}/riv/ui/assets/polyfills.js
%{_datadir}/riv/ui/flags/4x3/ac.svg
%{_datadir}/riv/ui/flags/4x3/ad.svg
%{_datadir}/riv/ui/flags/4x3/ae.svg
%{_datadir}/riv/ui/flags/4x3/af.svg
%{_datadir}/riv/ui/flags/4x3/ag.svg
%{_datadir}/riv/ui/flags/4x3/ai.svg
%{_datadir}/riv/ui/flags/4x3/al.svg
%{_datadir}/riv/ui/flags/4x3/am.svg
%{_datadir}/riv/ui/flags/4x3/ao.svg
%{_datadir}/riv/ui/flags/4x3/aq.svg
%{_datadir}/riv/ui/flags/4x3/ar.svg
%{_datadir}/riv/ui/flags/4x3/as.svg
%{_datadir}/riv/ui/flags/4x3/at.svg
%{_datadir}/riv/ui/flags/4x3/au.svg
%{_datadir}/riv/ui/flags/4x3/aw.svg
%{_datadir}/riv/ui/flags/4x3/ax.svg
%{_datadir}/riv/ui/flags/4x3/az.svg
%{_datadir}/riv/ui/flags/4x3/ba.svg
%{_datadir}/riv/ui/flags/4x3/bb.svg
%{_datadir}/riv/ui/flags/4x3/bd.svg
%{_datadir}/riv/ui/flags/4x3/be.svg
%{_datadir}/riv/ui/flags/4x3/bf.svg
%{_datadir}/riv/ui/flags/4x3/bg.svg
%{_datadir}/riv/ui/flags/4x3/bh.svg
%{_datadir}/riv/ui/flags/4x3/bi.svg
%{_datadir}/riv/ui/flags/4x3/bj.svg
%{_datadir}/riv/ui/flags/4x3/bl.svg
%{_datadir}/riv/ui/flags/4x3/bm.svg
%{_datadir}/riv/ui/flags/4x3/bn.svg
%{_datadir}/riv/ui/flags/4x3/bo.svg
%{_datadir}/riv/ui/flags/4x3/bq.svg
%{_datadir}/riv/ui/flags/4x3/br.svg
%{_datadir}/riv/ui/flags/4x3/bs.svg
%{_datadir}/riv/ui/flags/4x3/bt.svg
%{_datadir}/riv/ui/flags/4x3/bv.svg
%{_datadir}/riv/ui/flags/4x3/bw.svg
%{_datadir}/riv/ui/flags/4x3/by.svg
%{_datadir}/riv/ui/flags/4x3/bz.svg
%{_datadir}/riv/ui/flags/4x3/ca.svg
%{_datadir}/riv/ui/flags/4x3/cc.svg
%{_datadir}/riv/ui/flags/4x3/cd.svg
%{_datadir}/riv/ui/flags/4x3/cefta.svg
%{_datadir}/riv/ui/flags/4x3/cf.svg
%{_datadir}/riv/ui/flags/4x3/cg.svg
%{_datadir}/riv/ui/flags/4x3/ch.svg
%{_datadir}/riv/ui/flags/4x3/ci.svg
%{_datadir}/riv/ui/flags/4x3/ck.svg
%{_datadir}/riv/ui/flags/4x3/cl.svg
%{_datadir}/riv/ui/flags/4x3/cm.svg
%{_datadir}/riv/ui/flags/4x3/cn.svg
%{_datadir}/riv/ui/flags/4x3/co.svg
%{_datadir}/riv/ui/flags/4x3/cp.svg
%{_datadir}/riv/ui/flags/4x3/cr.svg
%{_datadir}/riv/ui/flags/4x3/cu.svg
%{_datadir}/riv/ui/flags/4x3/cv.svg
%{_datadir}/riv/ui/flags/4x3/cw.svg
%{_datadir}/riv/ui/flags/4x3/cx.svg
%{_datadir}/riv/ui/flags/4x3/cy.svg
%{_datadir}/riv/ui/flags/4x3/cz.svg
%{_datadir}/riv/ui/flags/4x3/de.svg
%{_datadir}/riv/ui/flags/4x3/dg.svg
%{_datadir}/riv/ui/flags/4x3/dj.svg
%{_datadir}/riv/ui/flags/4x3/dk.svg
%{_datadir}/riv/ui/flags/4x3/dm.svg
%{_datadir}/riv/ui/flags/4x3/do.svg
%{_datadir}/riv/ui/flags/4x3/dz.svg
%{_datadir}/riv/ui/flags/4x3/ea.svg
%{_datadir}/riv/ui/flags/4x3/ec.svg
%{_datadir}/riv/ui/flags/4x3/ee.svg
%{_datadir}/riv/ui/flags/4x3/eg.svg
%{_datadir}/riv/ui/flags/4x3/eh.svg
%{_datadir}/riv/ui/flags/4x3/er.svg
%{_datadir}/riv/ui/flags/4x3/es-ct.svg
%{_datadir}/riv/ui/flags/4x3/es-ga.svg
%{_datadir}/riv/ui/flags/4x3/es.svg
%{_datadir}/riv/ui/flags/4x3/et.svg
%{_datadir}/riv/ui/flags/4x3/eu.svg
%{_datadir}/riv/ui/flags/4x3/fi.svg
%{_datadir}/riv/ui/flags/4x3/fj.svg
%{_datadir}/riv/ui/flags/4x3/fk.svg
%{_datadir}/riv/ui/flags/4x3/fm.svg
%{_datadir}/riv/ui/flags/4x3/fo.svg
%{_datadir}/riv/ui/flags/4x3/fr.svg
%{_datadir}/riv/ui/flags/4x3/ga.svg
%{_datadir}/riv/ui/flags/4x3/gb-eng.svg
%{_datadir}/riv/ui/flags/4x3/gb-nir.svg
%{_datadir}/riv/ui/flags/4x3/gb-sct.svg
%{_datadir}/riv/ui/flags/4x3/gb-wls.svg
%{_datadir}/riv/ui/flags/4x3/gb.svg
%{_datadir}/riv/ui/flags/4x3/gd.svg
%{_datadir}/riv/ui/flags/4x3/ge.svg
%{_datadir}/riv/ui/flags/4x3/gf.svg
%{_datadir}/riv/ui/flags/4x3/gg.svg
%{_datadir}/riv/ui/flags/4x3/gh.svg
%{_datadir}/riv/ui/flags/4x3/gi.svg
%{_datadir}/riv/ui/flags/4x3/gl.svg
%{_datadir}/riv/ui/flags/4x3/gm.svg
%{_datadir}/riv/ui/flags/4x3/gn.svg
%{_datadir}/riv/ui/flags/4x3/gp.svg
%{_datadir}/riv/ui/flags/4x3/gq.svg
%{_datadir}/riv/ui/flags/4x3/gr.svg
%{_datadir}/riv/ui/flags/4x3/gs.svg
%{_datadir}/riv/ui/flags/4x3/gt.svg
%{_datadir}/riv/ui/flags/4x3/gu.svg
%{_datadir}/riv/ui/flags/4x3/gw.svg
%{_datadir}/riv/ui/flags/4x3/gy.svg
%{_datadir}/riv/ui/flags/4x3/hk.svg
%{_datadir}/riv/ui/flags/4x3/hm.svg
%{_datadir}/riv/ui/flags/4x3/hn.svg
%{_datadir}/riv/ui/flags/4x3/hr.svg
%{_datadir}/riv/ui/flags/4x3/ht.svg
%{_datadir}/riv/ui/flags/4x3/hu.svg
%{_datadir}/riv/ui/flags/4x3/ic.svg
%{_datadir}/riv/ui/flags/4x3/id.svg
%{_datadir}/riv/ui/flags/4x3/ie.svg
%{_datadir}/riv/ui/flags/4x3/il.svg
%{_datadir}/riv/ui/flags/4x3/im.svg
%{_datadir}/riv/ui/flags/4x3/in.svg
%{_datadir}/riv/ui/flags/4x3/io.svg
%{_datadir}/riv/ui/flags/4x3/iq.svg
%{_datadir}/riv/ui/flags/4x3/ir.svg
%{_datadir}/riv/ui/flags/4x3/is.svg
%{_datadir}/riv/ui/flags/4x3/it.svg
%{_datadir}/riv/ui/flags/4x3/je.svg
%{_datadir}/riv/ui/flags/4x3/jm.svg
%{_datadir}/riv/ui/flags/4x3/jo.svg
%{_datadir}/riv/ui/flags/4x3/jp.svg
%{_datadir}/riv/ui/flags/4x3/ke.svg
%{_datadir}/riv/ui/flags/4x3/kg.svg
%{_datadir}/riv/ui/flags/4x3/kh.svg
%{_datadir}/riv/ui/flags/4x3/ki.svg
%{_datadir}/riv/ui/flags/4x3/km.svg
%{_datadir}/riv/ui/flags/4x3/kn.svg
%{_datadir}/riv/ui/flags/4x3/kp.svg
%{_datadir}/riv/ui/flags/4x3/kr.svg
%{_datadir}/riv/ui/flags/4x3/kw.svg
%{_datadir}/riv/ui/flags/4x3/ky.svg
%{_datadir}/riv/ui/flags/4x3/kz.svg
%{_datadir}/riv/ui/flags/4x3/la.svg
%{_datadir}/riv/ui/flags/4x3/lb.svg
%{_datadir}/riv/ui/flags/4x3/lc.svg
%{_datadir}/riv/ui/flags/4x3/li.svg
%{_datadir}/riv/ui/flags/4x3/lk.svg
%{_datadir}/riv/ui/flags/4x3/lr.svg
%{_datadir}/riv/ui/flags/4x3/ls.svg
%{_datadir}/riv/ui/flags/4x3/lt.svg
%{_datadir}/riv/ui/flags/4x3/lu.svg
%{_datadir}/riv/ui/flags/4x3/lv.svg
%{_datadir}/riv/ui/flags/4x3/ly.svg
%{_datadir}/riv/ui/flags/4x3/ma.svg
%{_datadir}/riv/ui/flags/4x3/mc.svg
%{_datadir}/riv/ui/flags/4x3/md.svg
%{_datadir}/riv/ui/flags/4x3/me.svg
%{_datadir}/riv/ui/flags/4x3/mf.svg
%{_datadir}/riv/ui/flags/4x3/mg.svg
%{_datadir}/riv/ui/flags/4x3/mh.svg
%{_datadir}/riv/ui/flags/4x3/mk.svg
%{_datadir}/riv/ui/flags/4x3/ml.svg
%{_datadir}/riv/ui/flags/4x3/mm.svg
%{_datadir}/riv/ui/flags/4x3/mn.svg
%{_datadir}/riv/ui/flags/4x3/mo.svg
%{_datadir}/riv/ui/flags/4x3/mp.svg
%{_datadir}/riv/ui/flags/4x3/mq.svg
%{_datadir}/riv/ui/flags/4x3/mr.svg
%{_datadir}/riv/ui/flags/4x3/ms.svg
%{_datadir}/riv/ui/flags/4x3/mt.svg
%{_datadir}/riv/ui/flags/4x3/mu.svg
%{_datadir}/riv/ui/flags/4x3/mv.svg
%{_datadir}/riv/ui/flags/4x3/mw.svg
%{_datadir}/riv/ui/flags/4x3/mx.svg
%{_datadir}/riv/ui/flags/4x3/my.svg
%{_datadir}/riv/ui/flags/4x3/mz.svg
%{_datadir}/riv/ui/flags/4x3/na.svg
%{_datadir}/riv/ui/flags/4x3/nc.svg
%{_datadir}/riv/ui/flags/4x3/ne.svg
%{_datadir}/riv/ui/flags/4x3/nf.svg
%{_datadir}/riv/ui/flags/4x3/ng.svg
%{_datadir}/riv/ui/flags/4x3/ni.svg
%{_datadir}/riv/ui/flags/4x3/nl.svg
%{_datadir}/riv/ui/flags/4x3/no.svg
%{_datadir}/riv/ui/flags/4x3/np.svg
%{_datadir}/riv/ui/flags/4x3/nr.svg
%{_datadir}/riv/ui/flags/4x3/nu.svg
%{_datadir}/riv/ui/flags/4x3/nz.svg
%{_datadir}/riv/ui/flags/4x3/om.svg
%{_datadir}/riv/ui/flags/4x3/pa.svg
%{_datadir}/riv/ui/flags/4x3/pe.svg
%{_datadir}/riv/ui/flags/4x3/pf.svg
%{_datadir}/riv/ui/flags/4x3/pg.svg
%{_datadir}/riv/ui/flags/4x3/ph.svg
%{_datadir}/riv/ui/flags/4x3/pk.svg
%{_datadir}/riv/ui/flags/4x3/pl.svg
%{_datadir}/riv/ui/flags/4x3/pm.svg
%{_datadir}/riv/ui/flags/4x3/pn.svg
%{_datadir}/riv/ui/flags/4x3/pr.svg
%{_datadir}/riv/ui/flags/4x3/ps.svg
%{_datadir}/riv/ui/flags/4x3/pt.svg
%{_datadir}/riv/ui/flags/4x3/pw.svg
%{_datadir}/riv/ui/flags/4x3/py.svg
%{_datadir}/riv/ui/flags/4x3/qa.svg
%{_datadir}/riv/ui/flags/4x3/re.svg
%{_datadir}/riv/ui/flags/4x3/ro.svg
%{_datadir}/riv/ui/flags/4x3/rs.svg
%{_datadir}/riv/ui/flags/4x3/ru.svg
%{_datadir}/riv/ui/flags/4x3/rw.svg
%{_datadir}/riv/ui/flags/4x3/sa.svg
%{_datadir}/riv/ui/flags/4x3/sb.svg
%{_datadir}/riv/ui/flags/4x3/sc.svg
%{_datadir}/riv/ui/flags/4x3/sd.svg
%{_datadir}/riv/ui/flags/4x3/se.svg
%{_datadir}/riv/ui/flags/4x3/sg.svg
%{_datadir}/riv/ui/flags/4x3/sh.svg
%{_datadir}/riv/ui/flags/4x3/si.svg
%{_datadir}/riv/ui/flags/4x3/sj.svg
%{_datadir}/riv/ui/flags/4x3/sk.svg
%{_datadir}/riv/ui/flags/4x3/sl.svg
%{_datadir}/riv/ui/flags/4x3/sm.svg
%{_datadir}/riv/ui/flags/4x3/sn.svg
%{_datadir}/riv/ui/flags/4x3/so.svg
%{_datadir}/riv/ui/flags/4x3/sr.svg
%{_datadir}/riv/ui/flags/4x3/ss.svg
%{_datadir}/riv/ui/flags/4x3/st.svg
%{_datadir}/riv/ui/flags/4x3/sv.svg
%{_datadir}/riv/ui/flags/4x3/sx.svg
%{_datadir}/riv/ui/flags/4x3/sy.svg
%{_datadir}/riv/ui/flags/4x3/sz.svg
%{_datadir}/riv/ui/flags/4x3/ta.svg
%{_datadir}/riv/ui/flags/4x3/tc.svg
%{_datadir}/riv/ui/flags/4x3/td.svg
%{_datadir}/riv/ui/flags/4x3/tf.svg
%{_datadir}/riv/ui/flags/4x3/tg.svg
%{_datadir}/riv/ui/flags/4x3/th.svg
%{_datadir}/riv/ui/flags/4x3/tj.svg
%{_datadir}/riv/ui/flags/4x3/tk.svg
%{_datadir}/riv/ui/flags/4x3/tl.svg
%{_datadir}/riv/ui/flags/4x3/tm.svg
%{_datadir}/riv/ui/flags/4x3/tn.svg
%{_datadir}/riv/ui/flags/4x3/to.svg
%{_datadir}/riv/ui/flags/4x3/tr.svg
%{_datadir}/riv/ui/flags/4x3/tt.svg
%{_datadir}/riv/ui/flags/4x3/tv.svg
%{_datadir}/riv/ui/flags/4x3/tw.svg
%{_datadir}/riv/ui/flags/4x3/tz.svg
%{_datadir}/riv/ui/flags/4x3/ua.svg
%{_datadir}/riv/ui/flags/4x3/ug.svg
%{_datadir}/riv/ui/flags/4x3/um.svg
%{_datadir}/riv/ui/flags/4x3/un.svg
%{_datadir}/riv/ui/flags/4x3/us.svg
%{_datadir}/riv/ui/flags/4x3/uy.svg
%{_datadir}/riv/ui/flags/4x3/uz.svg
%{_datadir}/riv/ui/flags/4x3/va.svg
%{_datadir}/riv/ui/flags/4x3/vc.svg
%{_datadir}/riv/ui/flags/4x3/ve.svg
%{_datadir}/riv/ui/flags/4x3/vg.svg
%{_datadir}/riv/ui/flags/4x3/vi.svg
%{_datadir}/riv/ui/flags/4x3/vn.svg
%{_datadir}/riv/ui/flags/4x3/vu.svg
%{_datadir}/riv/ui/flags/4x3/wf.svg
%{_datadir}/riv/ui/flags/4x3/ws.svg
%{_datadir}/riv/ui/flags/4x3/xk.svg
%{_datadir}/riv/ui/flags/4x3/xx.svg
%{_datadir}/riv/ui/flags/4x3/ye.svg
%{_datadir}/riv/ui/flags/4x3/yt.svg
%{_datadir}/riv/ui/flags/4x3/za.svg
%{_datadir}/riv/ui/flags/4x3/zm.svg
%{_datadir}/riv/ui/flags/4x3/zw.svg
%{_datadir}/riv/ui/doc/favicon-16x16.png
%{_datadir}/riv/ui/doc/favicon-32x32.png
%{_datadir}/riv/ui/doc/index.css
%{_datadir}/riv/ui/doc/index.html
%{_datadir}/riv/ui/doc/oauth2-redirect.html
%{_datadir}/riv/ui/doc/swagger-initializer.js
%{_datadir}/riv/ui/doc/swagger-ui-bundle.js
%{_datadir}/riv/ui/doc/swagger-ui-bundle.js.map
%{_datadir}/riv/ui/doc/swagger-ui-es-bundle-core.js
%{_datadir}/riv/ui/doc/swagger-ui-es-bundle-core.js.map
%{_datadir}/riv/ui/doc/swagger-ui-es-bundle.js
%{_datadir}/riv/ui/doc/swagger-ui-es-bundle.js.map
%{_datadir}/riv/ui/doc/swagger-ui-standalone-preset.js
%{_datadir}/riv/ui/doc/swagger-ui-standalone-preset.js.map
%{_datadir}/riv/ui/doc/swagger-ui.css
%{_datadir}/riv/ui/doc/swagger-ui.css.map
%{_datadir}/riv/ui/doc/swagger-ui.js
%{_datadir}/riv/ui/doc/swagger-ui.js.map
