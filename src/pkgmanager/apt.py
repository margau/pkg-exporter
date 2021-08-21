import apt
import apt.progress

upgradable_dict = {}

cache = apt.Cache()
cache.open(None)


class AptPkgManager:
    def labelDict(self, origin):
        lDict = {}
        lDict["archive"] = origin.archive
        lDict["component"] = origin.component
        lDict["label"] = origin.label
        lDict["origin"] = origin.origin
        lDict["site"] = origin.site
        lDict["trusted"] = origin.trusted
        return lDict
    
    

    def getOrigins(self):
        for package_name in cache.keys():
            selected_package = cache[package_name]
            if not selected_package.is_installed:
                continue
            # insert information into upgradable_dict
            # informations are stored "per origin"
            # we use the labels string representation as keys
            origin = selected_package.candidate.origins[0]
            key = str(origin)
            # inside the first iteration, we setup the origin entry
            if key not in upgradable_dict:
                upgradable_dict[key] = {"upgradable": 0, "installed": 0}
                upgradable_dict[key]["labels"] = self.labelDict(origin)
            # increment appropriate counters
            upgradable_dict[key]["installed"] += 1
            if selected_package.is_upgradable:
                upgradable_dict[key]["upgradable"] += 1
        return upgradable_dict
