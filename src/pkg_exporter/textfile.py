#!/usr/bin/env python3

from prometheus_client import CollectorRegistry, Gauge, write_to_textfile, start_http_server
from time import sleep
from pkg_exporter.pkgmanager import apt
from pkg_exporter import reboot
import argparse
import os
import sys

def populate_registry(registry, rootdir=None):
    # get updates from apt
    pkgmanager = apt.AptPkgManager(rootdir=rootdir)

    # initially, check which metrics and labels are available
    metrics = pkgmanager.getMetricDict()
    labels = pkgmanager.getLabelNames()
    gauges = {}
    meta_gauges = {}

    # also add reboot metrics
    rebootmanager = reboot.RebootManager()
    reboot_gauge = Gauge(
        "pkg_reboot_required", "Node Requires an Reboot", [], registry=registry
    )

    # add update statistics
    meta_metric = pkgmanager.getMetaMetricDict()
    for key, value in meta_metric.items():
        meta_gauges[key] = Gauge(f"pkg_{key}", value["description"], registry=registry)

    # Create all the gauge metrics
    for key, value in metrics.items():
        gauges[key] = Gauge(
            f"pkg_{key}", value["description"], labels, registry=registry
        )

    # let the pkgmanager query its internal metrics
    pkgmanager.query()

    # now query metric by metric, and set values for all labels
    for name, gauge in gauges.items():
        metricList = pkgmanager.getMetricValue(name)
        for m in metricList:
            gauge.labels(*m["label"]).set(m["value"])

    for name, gauge in meta_gauges.items():
        gauge.set(pkgmanager.getMetaValue(name))

    rebootmanager.query()
    reboot_gauge.set(rebootmanager.getMetricValue())

def write_registry_to_file(registry, exporter_file=None):
    if not exporter_file:
        exporter_file = os.getenv("PKG_EXPORTER_FILE",
                                  "/var/prometheus/pkg-exporter.prom")
    exporter_dir = os.path.dirname(exporter_file)
    os.makedirs(exporter_dir, exist_ok=True)

    write_to_textfile(exporter_file, registry)

def serve(registry, addr, port, timewait, rootdir):
    start_http_server(addr=addr, port=port, registry=registry)
    while True:
        sleep(timewait)
        registry = CollectorRegistry()
        populate_registry(registry, rootdir)


def processArgs():
    parser = argparse.ArgumentParser(
        description="Collect metrics from apt and export it as a service")
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-f", "--exporter-file",
        type=str,
        default=os.getenv('PKG_EXPORTER_FILE', "/var/prometheus/pkg-exporter.prom"),
        help="File to export, if used the content will not be served")
    group.add_argument("-d", "--daemon",
        action='store_true',
        help="Run as daemon and server metric via http")
    parser.add_argument("-a", "--bind-addr",
        type=str,
        default=os.getenv('PKG_EXPORTER_ADDR', '0.0.0.0'),
        help="Bind address")
    parser.add_argument("-p", "--port",
        type=int,
        default=os.getenv('PKG_EXPORTER_PORT', 8089),
        help="Bind port")
    parser.add_argument("-r", "--rootdir",
        type=str,
        default=os.getenv('PKG_EXPORTER_ROOT_DIR', None),
        help="Custom root directory for dpkg")
    parser.add_argument("-t", "--time-wait",
        type=int,
        default=os.getenv('PKG_EXPORTER_TIME_WAIT', 300),
        help="time (in second) to wait between data updates")
    return parser.parse_args()

def main():
    args = processArgs()
    registry = CollectorRegistry()
    populate_registry(registry, args.rootdir)

    if not args.daemon:
        write_registry_to_file(registry, args.exporter_file)
    else:
        serve(registry, args.bind_addr, args.port, args.time_wait, args.rootdir)


if __name__ == "__main__":
    main()

