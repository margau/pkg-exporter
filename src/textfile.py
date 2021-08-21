#!/usr/bin/env python3

from prometheus_client import CollectorRegistry, Gauge, write_to_textfile
from pkgmanager import apt
import os

registry = CollectorRegistry()

# get updates from apt
source = apt.AptPkgManager()

origins = source.getOrigins()

g_inst = None
g_upgr = None

for k, v in origins.items():
    label_names = []
    label_values = []
    for lk, lv in v["labels"].items():
        label_names.append(lk)
        label_values.append(lv)

    # only initialze in the first iteration
    if g_inst is None:
        g_inst = Gauge(
            'pkg_installed', 'Installed Packages from this package origin',
            label_names, registry=registry
            )
    if g_upgr is None:
        g_upgr = Gauge(
            'pkg_upgradable', 'Upgradable packages in this package origin',
            label_names, registry=registry
            )

    g_inst.labels(*label_values).set(v["installed"])
    g_upgr.labels(*label_values).set(v["upgradable"])

exporter_file = os.getenv("PKG_EXPORTER_FILE",
                          "/var/prometheus/pkg-exporter.prom")
exporter_dir = os.path.dirname(exporter_file)
os.makedirs(exporter_dir, exist_ok=True)

write_to_textfile(exporter_file, registry)
