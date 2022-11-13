import torch.multiprocessing as mp
from time import sleep
from fiber_guard.data_gen import GenericDataGen


class AnalyzingPipeline:
    def __init__(self, data_gen) -> None:
        self.data_gen = data_gen
        self.processes: list[mp.Process] = []
        self.queues: list[mp.Queue] = []
        self.stop_pipeline = mp.Value("b", False)
        self.out_of_data = mp.Value("b", False)

    def init_eval_pipeline(self):
        self.queues = [mp.Queue(1024) for _ in range(4)]

        self.processes.append(
            mp.Process(target=self._input, args=(self.data_gen, self.queues[0]))
        )
        self.processes.append(
            mp.Process(
                target=self.addition,
            )
        )

    def execute_pipeline(self):
        # start processes
        for proc in self.processes:
            proc.start()

        sleep(1)
        try:
            while not self.stop_pipeline.value:
                sleep(0.5)
                if not any(q.qsize() for q in self.queues) and self.out_of_data.value:
                    self.stop_pipeline.value = True

            # wait for processes
            for proc in self.processes:
                proc.join()

        except KeyboardInterrupt:
            self.stop_pipeline.value = True
            sleep(1)
            # kill it all
            self.clean_res()

    def _input(self, data_gen: GenericDataGen, in_q: mp.Queue):
        # signal.signal(signal.SIGINT, signal.SIG_IGN)
        for i in data_gen.get_data():
            in_q.put(i)

        self.out_of_data.value = True

    def addition(self):
        while not self.stop_pipeline.value:
            print(1 + 1)
