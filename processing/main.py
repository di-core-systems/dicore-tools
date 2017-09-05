from postprocessing import PostProcessing
from presentation import Presentation


if __name__ == "__main__":
    processing = PostProcessing()
    processing.start_processing()

    presentation = Presentation(processing)
    #presentation.plot()