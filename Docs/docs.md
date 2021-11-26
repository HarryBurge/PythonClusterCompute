# Python Cluster Compute


## Nodes
Currently nodes only care about one heuristic, could make them on indurvidual basis

### Messages
Messages passed in the form "{Tag}:{len of msg}" with spaces after based off header length. Then "{msg}".

#### Message Tag Enum
Each Enum name has to be exactly 4 letters long
- INFO (Infomation to be stored by other nodes about another node)

### Data Stored About Other Nodes
- IP <sub>of other node</sub>
- Port <sub>of other node</sub>
- Offload, Nothing or Gain heuristic <sub>of other node</sub>
- Since last update <sub>from other node</sub>
- Since last push or pull <sub>from this node</sub>

##### Local storage
Stored in the form {(target ip, target port) : [target heuristic, last update from target, last push or pull to target device], ...}

##### Send to other devices
Passed in the form "{Offload, Nothing or Gain heuristic 2dp}" with info tag.

