import apt
import apt.progress


class AptPkgManager:
    def __init__(self):
        self.metricDict = {}
        self.metricDict["installed"] = \
            {"description": "Installed packages per origin"}
        self.metricDict["upgradable"] = \
            {"description": "Upgradable packages per origin"}
        self.metricDict["auto_removable"] = \
            {"description": "Auto-removable packages per origin"}
        self.metricDict["broken"] = \
            {"description": "Broken packages per origin"}
        self.metricsByOrigin = {}
        self.cache = apt.Cache()
        self.cache.open(None)

    def labelValues(self, origin):
        labelValues = [origin.archive, origin.component, origin.label,
                       origin.origin, origin.site, origin.trusted]
        return labelValues

    def getMetricDict(self):
        return self.metricDict

    def getLabelNames(self):
        labelNames = ["archive", "component", "label", "origin",
                      "site", "trusted"]
        return labelNames

    def query(self):
        for package_name in self.cache.keys():
            selected_package = self.cache[package_name]
            if not selected_package.is_installed:
                continue
            origin = selected_package.candidate.origins[0]
            key = str(origin)
            if key not in self.metricsByOrigin:
                self.metricsByOrigin[key] = {}
                for k, _ in self.metricDict.items():
                    self.metricsByOrigin[key][k] = 0

                self.metricsByOrigin[key]["label_values"] = \
                    self.labelValues(origin)

            # Count Packages for the metrics
            if selected_package.is_installed:
                self.metricsByOrigin[key]["installed"] += 1
            if selected_package.is_upgradable:
                self.metricsByOrigin[key]["upgradable"] += 1
            if selected_package.is_auto_removable:
                self.metricsByOrigin[key]["auto_removable"] += 1
            if selected_package.is_now_broken:
                self.metricsByOrigin[key]["broken"] += 1

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
