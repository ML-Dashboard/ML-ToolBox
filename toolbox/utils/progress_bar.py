import datetime
import sys
import time
from typing import Any, List


class ProgressBar:

    def __init__(self,
                 length: int,
                 fmt: str,
                 eta: bool = True,
                 max_normalize_steps: int = 20):
        self.length = length
        self.max_normalize_steps = max_normalize_steps
        self.eta = eta
        if eta:
            self.bar_format = '[%%-%ds](eta: %%s)%s' % (length, fmt)
        else:
            self.bar_format = '[%%-%ds]%s' % (length, fmt)
        self.queue: List[float] = []
        self.step: int = 0
        self.prev_time: float = 0.0
        self.prev_percent: float = -1.0
        self.reset()

    def progress(self, percent: float, *info: Any) -> None:
        if percent == self.prev_percent:
            print('Error: Did not update percentage')
            return
        sys.stdout.write('\r')
        curr_time = time.time()
        eta = ((curr_time - self.prev_time) / (percent - self.prev_percent) *
               (100 - percent))
        self.queue[self.step % (len(self.queue))] = eta
        eta = sum(self.queue) / len(self.queue)
        self.step += 1
        self.prev_time = curr_time
        self.prev_percent = percent
        if self.eta:
            eta_str = datetime.timedelta(seconds=int(eta))
            info = (eta_str,) + info
        bar_val = ('=' * int(percent * self.length / 100), *info)
        sys.stdout.write(self.bar_format % bar_val)
        sys.stdout.write(' ' * 10)
        sys.stdout.flush()

    def reset(self) -> None:
        self.queue = [0.0] * self.max_normalize_steps
        self.step = 0
        self.prev_time = time.time()
        self.prev_percent = -1.0
