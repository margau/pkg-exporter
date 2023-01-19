import os
import apt
import apt.progress
from pathlib import Path


class AptPkgManager:
    def __init__(self):
        self.metricDict = {}
        self.metricDict["installed"] = {"description": "Installed packages per origin"}
        self.metricDict["upgradable"] = {
            "description": "Upgradable packages per origin"
        }
        self.metricDict["auto_removable"] = {
            "description": "Auto-removable packages per origin"
        }
        self.metricDict["broken"] = {"description": "Broken packages per origin"}
        self.metricsByOrigin = {}
        self.metaMetrics = {}
        self.metaMetrics["update_time_available"] = 0
        self.metaMetrics["update_start_time"] = 0
        self.metaMetrics["update_end_time"] = 0

        self.cache = apt.Cache()
        self.cache.open(None)

    def labelValues(self, origin):
        labelValues = [
            origin.archive,
            origin.component,
            origin.label,
            origin.origin,
            origin.site,
            origin.trusted,
        ]
        return labelValues

    def getMetricDict(self):
        return self.metricDict

    def getMetaMetricDict(self):
        updateMetrics = {}
        updateMetrics["update_start_time"] = {
            "description": "timestamp of last apt update start"
        }
        updateMetrics["update_end_time"] = {
            "description": "Timestamp of last apt update finish"
        }
        updateMetrics["update_time_available"] = {
            "description": "Availability of the apt update timestamp"
        }
        return updateMetrics

    def getLabelNames(self):
        labelNames = ["archive", "component", "label", "origin", "site", "trusted"]
        return labelNames

    def query(self):
        for package_name in self.cache.keys():
            selected_package = self.cache[package_name]
            if not selected_package.is_installed:
                continue
            for origin in selected_package.candidate.origins:
                key = str(origin)
                if key not in self.metricsByOrigin:
                    self.metricsByOrigin[key] = {}
                    for k, _ in self.metricDict.items():
                        self.metricsByOrigin[key][k] = 0

                    self.metricsByOrigin[key]["label_values"] = self.labelValues(origin)

                # Count Packages for the metrics
                if selected_package.is_installed:
                    self.metricsByOrigin[key]["installed"] += 1
                if selected_package.is_upgradable:
                    self.metricsByOrigin[key]["upgradable"] += 1
                if selected_package.is_auto_removable:
                    self.metricsByOrigin[key]["auto_removable"] += 1
                if selected_package.is_now_broken:
                    self.metricsByOrigin[key]["broken"] += 1
        # apt update time
        preUpdatePath = Path(
            os.getenv(
                "PKG_EXPORTER_APT_PRE_FILE",
                "/tmp/pkg-exporter-apt-update-pre",
            )
        )
        postUpdatePath = Path(
            os.getenv(
                "PKG_EXPORTER_APT_POST_FILE",
                "/tmp/pkg-exporter-apt-update-post",
            )
        )

        if preUpdatePath.is_file() and postUpdatePath.is_file():
            self.metaMetrics["update_time_available"] = 1
            self.metaMetrics["update_start_time"] = preUpdatePath.stat().st_mtime
            self.metaMetrics["update_end_time"] = postUpdatePath.stat().st_mtime

    def getMetricValue(self, name):
        metricValue = []
        for _, value in self.metricsByOrigin.items():
            v = {}
            v["label"] = value["label_values"]
            if name in value:
                v["value"] = value[name]
            else:
                continue
            metricValue.append(v)
        return metricValue

    def getMetaValue(self, name):
        return self.metaMetrics[name]
