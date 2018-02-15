from malcolm.core import Info

from .util import DatasetType, AttributeDatasetType


class NDArrayDatasetInfo(Info):
    """Declare the NDArray data this produces as being a useful dataset to store
    to file

     Args:
         rank: The rank of the dataset, e.g. 2 for a 2D detector
    """
    def __init__(self, rank):
        # type: (int) -> None
        self.rank = rank


class CalculatedNDAttributeDatasetInfo(Info):
    """Declare that we have calculated some statistics from the main dataset
    and these will be available

    Args:
        name: Dataset name that should be written to
        attr: NDAttribute name to get data from
    """
    def __init__(self, name, attr):
        self.name = name
        self.attr = attr


class NDAttributeDatasetInfo(Info):
    """Declare an NDAttribute attached to this NDArray to produce a useful
    dataset to store to file

    Args:
        name: Dataset name that should be written to
        type: What NeXuS dataset type it produces
        attr: NDAttribute name to get data from
        rank: The rank of the dataset
    """
    def __init__(self, name, type, attr, rank):
        # type: (str, AttributeDatasetType, str, int) -> None
        self.name = name
        self.type = type
        self.attr = attr
        self.rank = rank


class DatasetProducedInfo(Info):
    """Declare that we will write the following dataset to file

    Args:
        name: Dataset name
        filename: Filename relative to the fileDir we were given
        type: What NeXuS dataset type it produces
        rank: The rank of the dataset including generator dims
        path: The path of the dataset within the file
        uniqueid: The path of the UniqueID dataset within the file
    """
    def __init__(self, name, filename, type, rank, path, uniqueid):
        # type: (str, str, DatasetType, int, str, str) -> None
        self.name = name
        self.filename = filename
        self.type = type
        self.rank = rank
        self.path = path
        self.uniqueid = uniqueid
