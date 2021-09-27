#!/usr/bin/env python3

from prometheus_client import CollectorRegistry, Gauge, write_to_textfile
from pkg_exporter.pkgmanager import apt
from pkg_exporter import reboot
import os


def main():
    registry = CollectorRegistry()

    # get updates from apt
    pkgmanager = apt.AptPkgManager()

    # initially, check which metrics and labels are available
    metrics = pkgmanager.getMetricDict()
    labels = pkgmanager.getLabelNames()

    # also add reboot metrics
    rebootmanager = reboot.RebootManager()
    reboot_gauge = Gauge(
                'pkg_reboot_required', 'Node Requires an Reboot',
                [], registry=registry
                )

    # Create all the gauge metrics
    gauges = {}
    for key, value in metrics.items():
        gauges[key] = Gauge(
                f'pkg_{key}', value["description"],
                labels, registry=registry
                )

    # let the pkgmanager query its internal metrics
    pkgmanager.query()

    # now query metric by metric, and set values for all labels
    for name, gauge in gauges.items():
        metricList = pkgmanager.getMetricValue(name)
        for m in metricList:
            gauge.labels(*m["label"]).set(m["value"])

    rebootmanager.query()
    reboot_gauge.set(rebootmanager.getMetricValue())

    exporter_file = os.getenv("PKG_EXPORTER_FILE",
                            "/var/prometheus/pkg-exporter.prom")
    exporter_dir = os.path.dirname(exporter_file)
    os.makedirs(exporter_dir, exist_ok=True)

    write_to_textfile(exporter_file, registry)

if __name__ == "__main__":
    main()