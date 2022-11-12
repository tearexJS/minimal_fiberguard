import h5py
import numpy as np
import torch
import abc
from typing import Generator
from tqdm import tqdm

ENGINES = ["np", "torch"]


class GenericDataGen(abc.ABC):
    def __init__(self, window: int, overlap: float, engine: str):
        self.engine = engine
        self.window = window
        self.overlap = overlap
        self.delta = int(self.window * self.overlap)

    @abc.abstractmethod
    def get_data(self) -> Generator[np.array, None, None]:
        pass

    def get_engine(self, data):
        if self.engine == "np":
            return np.array(data)
        elif self.engine == "torch":
            return torch.tensor(data, device=torch.device("cuda:0"))


class ReadFile(GenericDataGen):
    def __init__(self, window, overlap, file="fiber_guard/nominal.hdf5", engine="np"):
        super().__init__(window, overlap, engine)
        self.file = file

    def get_data(self) -> Generator[np.array, None, None]:
        with h5py.File(self.file) as container:
            for dataset_name in container:
                ds = container[dataset_name]
                for i in tqdm(range(0, len(ds) - self.window, self.delta)):
                    yield super().get_engine(ds[i : i + self.window])
