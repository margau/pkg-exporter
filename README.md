# Prometheus PKG Exporter

This project provides an textfile-based exporter for apt-repositories. 

**The Project is in its early development phases. Interfaces may change without notice. Compatibility and Stability do vary.**

For the changelog, use the [Releases-Section on GitHub](https://github.com/margau/pkg-exporter/releases/)

## Exported Metrics

At the moment, the packages installed, upgradable, broken and autoremovable are exported per repository as gauge. The label set depends on the packet manager type.

Additionally, `pkg_reboot_required` is exported to indicate that an reboot is needed.

```
# HELP pkg_reboot_required Node Requires an Reboot
# TYPE pkg_reboot_required gauge
pkg_reboot_required 1.0
# HELP pkg_update_start_time timestamp of last apt update start
# TYPE pkg_update_start_time gauge
pkg_update_start_time 1.641382890503045e+09
# HELP pkg_update_end_time Timestamp of last apt update finish
# TYPE pkg_update_end_time gauge
pkg_update_end_time 1.641382892755024e+09
# HELP pkg_update_time_available Availability of the apt update timestamp
# TYPE pkg_update_time_available gauge
pkg_update_time_available 1.0
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

### Global pip installation
Run `pip3 install pkg-exporter`.

### Install from source
Clone the repository and run `poetry install` from the main directory.
You can also use other standard installation methods for python packages, like directly installing from this git repository.

The pyinstaller-based binary is not provided any more.

### pipx
If a global pip installation is not possible (e.g. from debian 12 onwards), you can use [pipx](https://pypa.github.io/pipx), either for install, and/or for running pkg-exporter ad hoc:
```
pipx run --system-site-packages pkg-exporter
```

`--system-site-packages` is necessary to provide access to the system python3-apt lib.

### apt-based systems

Currently, only apt-based systems are supported. `python3-apt` needs to be installed on the system.

## Configuration and Usage

The node exporter needs to be configured for textfiles using the `--collector.textfile.directory` option. This exporter needs to write the exported metrics into this directory. 

The default path is `/var/prometheus/pkg-exporter.prom`, and may be changed via the `PKG_EXPORTER_FILE`-Environment Variable.
If the directory is not already present, it will be created by the exporter.

The command `pkg_exporter` provided by the package or the binary shall be executed in a appropriate interval, e.g. using cron or systemd timers.
The exporter needs to be executed with appropriate privileges, which are not necessarily root privileges.

An example configuration will be provided in this repository in the future.

### apt hook
To enable monitoring for apt update calls, place the file under `docs/00-pve-exporter` in `/etc/apt/apt.conf.d` on your system.
It will place files under `/tmp`. To customize the filepath of the timestamp files, the the environment variables `PKG_EXPORTER_APT_PRE_FILE` & `PKG_EXPORTER_APT_POST_FILE` may be used.
You can see the success of monitoring the apt update timestamps if the following metric is 1: `pkg_update_time_available 1.0`

Please not that the presence of an timestamp does not mean that all repositories were updated without issues.

## Alerting

Example alerting rules will be provided in the future.

## Roadmap

- Support for other pkg managers
- Deployment as dpkg-Packet
