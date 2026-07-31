import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import * as ExternalPlugin from "./.quartz/plugins"

const folderOrder = ['Signal Introduction','GNSS Security','Wi-Fi Security','Bluetooth Security','Mobile Network Security']

ExternalPlugin.Explorer({
    sortFn: (a, b) => {
        // folders before files
        if (a.isFolder !== b.isFolder) {
            return a.isFolder ? -1 : 1
        }

        if (a.isFolder && b.isFolder) {
            const idxA = folderOrder.indexOf(a.displayName)
            const idxB = folderOrder.indexOf(b.displayName)
            // folders not in the list fall to the bottom, alphabetically
            if (idxA === -1 && idxB === -1) return a.displayName.localeCompare(b.displayName)
                if (idxA === -1) return 1
                    if (idxB === -1) return -1
                        return idxA - idxB
        }

        // files within a folder: alphabetical
        return a.displayName.localeCompare(b.displayName)
    },
})


const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()
