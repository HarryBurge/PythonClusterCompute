# Python Cluster Compute


## Nodes

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

Passed in the form "{ONG heuristic 2dp}" with info tag.

