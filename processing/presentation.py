from postprocessing import PostProcessing
import matplotlib.pyplot as plt

class Presentation:

    def __init__(self, processing):
        self.processing = processing

    def plot(self):
        plt.plot([1,2,3,4])
        plt.ylabel('some numbers')
        plt.show()