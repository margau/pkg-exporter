# Prometheus PKG Exporter

This project provides an textfile-based exporter for apt-repositories. 

**The Project is in its early development phases. Interfaces may change without notice. Compatibility and Stability do vary.**

## Exported Metrics

At the moment, the packages installed and upgradable are exported per repository as gauge. The label set depends on the packet manager type.

```
# HELP pkg_installed Installed Packages from this package origin
# TYPE pkg_installed gauge
pkg_installed{archive="stable",component="main",label="Debian",origin="Debian",site="deb.debian.org",trusted="True"} 293.0
# HELP pkg_upgradable Upgradable packages in this package origin
# TYPE pkg_upgradable gauge
pkg_upgradable{archive="stable",component="main",label="Debian",origin="Debian",site="deb.debian.org",trusted="True"} 0.0

```

## Contributing

Feel free to contribute improvements, as well as support for non-apt based systems.

## Installation

The easiest installation method is downloading the prebuilt binary from the relase. 

Alternatively, the scripts and requirements in the repositoriy may be installed manually.

## Configuration and Usage

The node exporter needs to be configured for textfiles using the `--collector.textfile.directory` option. This exporter needs to write into this directory. The default path is `/var/prometheus/pkg-exporter.prom`, and may be changed via the `PKG_EXPORTER_FILE`-Environment Variable.

The script `texfile.py` or the binary shall be executed in a appropriate interval, e.g. using cron or systemd timers.

An example configuration will be provided in this repository in the future.

## Alerting

Example alerting rules will be provided in the future.

## Roadmap

- Support for other pkg managers
- Timestamp Support ("Last List/Cache Update")
- Deployment as dpkg-Packet