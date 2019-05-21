import unittest
import sys, os, time
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import random_graph
import logging, time
import numpy as np
from matplotlib import pyplot as plt
import random
import string
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

class TestCorrectness(unittest.TestCase):
    def init_logging(self, name='testname', log_level=logging.WARNING):
        fileh = logging.FileHandler(f'./log/{name}-{logging.getLevelName(log_level)}.log', 'w', encoding='utf-8')
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(message)s')
        fileh.setFormatter(formatter)

        log = logging.getLogger()  # root logger
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        log.addHandler(fileh)      # set the new handler
        log.setLevel(log_level)

        return fileh


    def test_correctness(self):
        fileh = self.init_logging('correctness', logging.DEBUG)
        
        rg = random_graph.RandomGraph()
        rg.run(3)

        fileh.close()
    
    def test_benchmark(self):
        fileh = self.init_logging('benchmark', logging.INFO)
        rg = random_graph.RandomGraph()

        n_array = np.arange(1, 100)
        E_array = np.zeros(n_array.shape)
        avg_time_array = np.zeros(n_array.shape)
        for i in range(len(n_array)):
            # n_array[i] = 2 ** n_array[i]
            logging.info(f'n = {n_array[i]}')
            run_times = 10
            begin = time.time()
            for j in range(run_times):
                E_array[i] += rg.run(n_array[i])
            avg_time_array[i] = time.time() - begin
            avg_time_array[i] /= run_times
            E_array[i] /= (run_times)

        fig, (ax1, ax2) = plt.subplots(
            nrows=2, ncols=1,
            figsize=(8, 8)
        )

        ax1.set_title('Average total weight of random MST - $n$ curve')
        ax1.set_ylabel('Average Total weight')
        ax1.plot(n_array, E_array)

        ax2.set_title('Avearge time used - $n$ curve')
        ax2.set_xlabel('$n$')
        ax2.set_ylabel('Average time used')
        ax2.plot(n_array, avg_time_array, c = 'r')

        plt.savefig('./figures/' + 'benchmark' + '.svg')

        fileh.close()

if __name__ == "__main__":
    unittest.main()
