# Prometheus PKG Exporter

This project provides an textfile-based exporter for apt-repositories. 

**The Project is in its early development phases. Interfaces may change without notice. Compatibility and Stability do vary.**

For the changelog, use the [Releases-Section on GitHub](https://github.com/margau/pkg-exporter/releases/)

## Exported Metrics

At the moment, the packages installed and upgradable are exported per repository as gauge. The label set depends on the packet manager type.

```
# HELP pkg_installed Installed packages per origin
# TYPE pkg_installed gauge
pkg_installed{archive="focal-updates",component="main",label="Ubuntu",origin="Ubuntu",site="ftp.fau.de",trusted="True"} 672.0
# HELP pkg_upgradable Upgradable packages per origin
# TYPE pkg_upgradable gauge
pkg_upgradable{archive="focal-updates",component="main",label="Ubuntu",origin="Ubuntu",site="ftp.fau.de",trusted="True"} 7.0
# HELP pkg_auto_removable Auto-removable packages per origin
# TYPE pkg_auto_removable gauge
pkg_auto_removable{archive="focal-updates",component="main",label="Ubuntu",origin="Ubuntu",site="ftp.fau.de",trusted="True"} 6.0
# HELP pkg_broken Broken packages per origin
# TYPE pkg_broken gauge
pkg_broken{archive="focal-updates",component="main",label="Ubuntu",origin="Ubuntu",site="ftp.fau.de",trusted="True"} 0.0

```

## Contributing

Feel free to contribute improvements, as well as support for non-apt based systems.

## Installation

Clone the repository and run `python setup.py install` from the main directory.
You can also use other standard installation methods for python packages.

Alternatively, a single binary built using pyinstaller is provided.

### apt-based systems

Currently, only apt-based systems are supported. `python3-apt` needs to be installed on the system.

## Configuration and Usage

The node exporter needs to be configured for textfiles using the `--collector.textfile.directory` option. This exporter needs to write the exported metrics into this directory. 

The default path is `/var/prometheus/pkg-exporter.prom`, and may be changed via the `PKG_EXPORTER_FILE`-Environment Variable.
If the directory is not already present, it will be created by the exporter.

The command `pkg_exporter` provided by the package or the binary shall be executed in a appropriate interval, e.g. using cron or systemd timers.
The exporter needs to be executed with appropriate privileges, which are not necessarily root privileges.

An example configuration will be provided in this repository in the future.

## Alerting

Example alerting rules will be provided in the future.

## Roadmap

- Support for other pkg managers
- Timestamp Support ("Last List/Cache Update")
- Deployment as dpkg-Packet