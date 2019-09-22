# Graph-to-p4

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3457291.svg)](https://doi.org/10.5281/zenodo.3457291)

## Goal

This project tries to convert/translate visual representations of hardware functions (such as the parse graph) into P4 code. The originla goal was to provide a smooth start into P4 for our students at DTU. However, right now the project might try to accommodate other pipeline abstractions such as tables and actions into profiles or similar entities. The goal could be to represent all the releveant pipeline entities and then try to build one from the visual representation we make. The project might also evolve into full visual programming and providing a 2-way conversion between high-level visual representations and P4. The ability to change the visual representations, build a pipeline using visual entities and the reflect all this back and forth to P4 code.

As the toolset also uses a browser based diagram tool, the project could also try to aim for developing a full toolset for P4 in the browser. A browser based code editor for P4, possibly the visual representations of the the P4 pipeline and also a JS-based tool for translating between would be a great step forward.

## Usage
In principle, the tool only used argparse and xml modules but those might already come with your python distribution (likely versions from 2.7 already include them).  The code was tested with Python 3.5 using Jetbrains Pycharm.

First of, go to draw.io and upload the file example_parse_graph.xml included in the repo. Use it to first get familiar with the tool. When you upload it you will see an exmaple of a parse graph already drawn and also a library with some predefined header and the transition (straight, not curved) arrow. One important thing is to snap the arrow to the edge of the entities or the compiler will not be able to convert it (the default parse graph should work just fine). Then hit File -> Export As -> XML -> (uncheck Compressed) -> Export. That exported file should be the input of the toll of this repository.

The following command takes the graph in the examples directory and creates the equivalent P4 file in the output directory. You can process the parse graph and output the P4 code as follows:

```bash
python main.py --arch v1model --output-path ./output/
```
You can also create separate files for defines (defines, constants and typedefs), headers of the parser and put them in the include directory. Any directories that do no exist will be created. Do it as follows:

```bash
python main.py --arch v1model --output-path ./output/ -i -s defines,headers,parser
```
## Future additions
The project is now prepared to accommodate other architectures (see arch directory) but I have not tested others yet. This could be done in the following weeks.


## Style
The project as a whole might lack some of the common best practices for Python coding  (PEP 8)  as well as other project structuring best practises, If you spot anything worth mentioning open and issue or make a correction yourself :)

