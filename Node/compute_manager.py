#~ Imports
import multiprocessing

#~ Consts
MAX_COMPUTE_UNITS= multiprocessing.cpu_count()
if MAX_COMPUTE_UNITS>2: MAX_COMPUTE_UNITS= MAX_COMPUTE_UNITS-2

#~ ComputeManager
class ComputeManager:

    def __init__(self) -> None:
        pass