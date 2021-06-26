import apt
import apt.progress

upgradable_dict = {}

cache = apt.Cache()
# Now, lets update the package list
# cache.update()
# We need to re-open the cache because it needs to read the package list
cache.open(None)

class AptPkgManager:
    def labelDict(self, origin):
        l = {}
        l["archive"] = origin.archive
        l["component"] = origin.component
        l["label"] = origin.label
        l["origin"] = origin.origin
        l["site"] = origin.site
        l["trusted"] = origin.trusted
        return l

    def getOrigins(self):
        for package_name in cache.keys():
            selected_package = cache[package_name]
            if not selected_package.is_installed:
                continue
            # insert information into upgradable_dict
            # informations are stored "per origin", we use the labels string representation as labels
            key = str(selected_package.candidate.origins[0])
            # inside the first iteration, we setup the origin entry
            if key not in upgradable_dict:
                upgradable_dict[key] = {"upgradable":0,"installed":0}
                upgradable_dict[key]["labels"] = self.labelDict(selected_package.candidate.origins[0])
            # increment appropriate counters
            upgradable_dict[key]["installed"] += 1
            if selected_package.is_upgradable:
                upgradable_dict[key]["upgradable"] += 1
        return upgradable_dict

