from torch.multiprocessing import set_start_method
from fiber_guard.pipeline import AnalyzingPipeline
import sys
from fiber_guard.data_gen import ReadFile


def main() -> int:
    method_set = False
    try:
        set_start_method("spawn")
    except Exception:
        method_set = True
        pass
    data_gen = ReadFile(overlap=0.5, window=1024, engine="torch")
    if not method_set:
        pipeline = AnalyzingPipeline(data_gen=data_gen)
        try:

            pipeline.init_eval_pipeline()
            pipeline.execute_pipeline()
        except Exception as e:
            # print(e)
            raise e
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
