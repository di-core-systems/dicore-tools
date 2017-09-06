from postprocessing import PostProcessing
from presentation import Presentation
from processing.latex.latex import Latex

if __name__ == "__main__":
    processing = PostProcessing()
    processing.start_processing()

    latex = Latex()
    fig = latex.create_diagram()
    latex.plot_graph(fig)

    presentation = Presentation(processing)
    #presentation.plot()