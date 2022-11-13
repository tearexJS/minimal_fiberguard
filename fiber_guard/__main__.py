from torch.multiprocessing import set_start_method
from fiber_guard.pipeline import AnalyzingPipeline
import sys
from fiber_guard.data_gen import ReadFile


def main() -> int:
    set_start_method("spawn")
    data_gen = ReadFile(overlap=0.5, window=1024, engine="torch")

    pipeline = AnalyzingPipeline(data_gen=data_gen)
    try:

        pipeline.init_eval_pipeline()
        pipeline.execute_pipeline()
    except Exception as e:
        raise e

    return 0


if __name__ == "__main__":
    sys.exit(main())
