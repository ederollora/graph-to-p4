# Graph-to-p4

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3457291.svg)](https://doi.org/10.5281/zenodo.3457291)

## Introduction and goal

This project tries to convert/translate visual representations of hardware functions (such as the parse graph) into P4 code. The original goal was to provide a smooth start into P4 for our students at DTU. However, right now the project might try to accommodate other pipeline abstractions such as tables and actions into profiles or similar entities. The goal could be to represent all the relevant pipeline entities and then try to build one from the visual representation we make. The project might also evolve into full visual programming and providing a 2-way conversion between high-level visual representations and P4. The ability to change the visual representations, build a pipeline using visual entities and the reflect all this back and forth to P4 code.

As the toolset also uses a browser-based diagram tool, the project could also try to aim for developing a full toolset for P4 in the browser. A browser-based code editor for P4, possibly the visual representations of the P4 pipeline and also a JS-based tool for translating between would be a great step forward.

## Usage
In principle, the tool only used argparse and xml modules but those might already come with your python distribution (likely versions from 2.7 already include them).  The code was tested with Python 3.5 using Jetbrains Pycharm.

First, of, go to draw.io and upload the file **diagram.xml** included in the diagram directory. Use it to first get familiar with the tool. When you upload it you will see an example of a parse graph already drawn and also a **library** with some predefined header and the transition (straight, not curved) arrow. If no library box appears the Scratchpad, then we have included the **library.xml** in the diagram directory. It contains a few standard headers and transition (straight) arrow (the curved one is going to be used for header stacks in the future). Import it by hitting the **Edit** button (pencil icon) in the Scratchpad located at the left tool column. 

If you modify the graph or add new states, an important thing is to properly snap the arrow to the edge of the entities or the compiler will not be able to convert it (the default parse graph should work just fine). If the arrow is not properly attached to the source parse node and destination node it cannot determine if there is a connection between two parse states.

If you want to check the metadata underlying states and transitions, select any of the ones available in the diagram and right-click on it. Then hit **Edit data**, you will see which fields are extracted, in which order and their bitwidth. You will also see the name for the header, the parse state, and default transition criteria. For transitions, you will mainly see the transition criteria for the current transition, which can override the predefined ones but has not been fully tested yet, so transitions in states have a preference for now on. This will be pushed soon.

Then hit **File -> Export As -> XML -> (uncheck Compressed) -> Export**. That exported file should be the input of the toll of this repository.

The following command takes the graph in the examples directory and creates the equivalent P4 file in the output directory. You can process the parse graph and output the P4 code as follows:

```bash
python3.5 main.py --arch v1model --output-path ./output/
```
You can also create separate files for defines (includes defines, constants, and typedefs), headers of the parser and put them in the include directory. Any directories that do not exist will be created. You see no reference to the XML graph because the default argument assigns the **example/graph.xml** as the input file. You can, however, add the -x argument to specify the path to the graph. Wun as follows to create separate files:

```bash
python3.5 main.py --arch v1model --output-path ./output/ -i -s defines,headers,parser
```

To compile the generated P4 file(s) run the command below (you need p4c). The output of these files has been added to the **example_output** directory for exemplary means. 

```bash
p4c --target bmv2 --arch v1model --std p4-16 switch.p4
```

## Future additions
The project is now prepared to accommodate other architectures (see **config/arch** directory) but I have not tested others yet. This is likely to be tested soon, probably starting with SUME and maybe PSA.


## Style
The project as a whole might lack some of the common best practices for Python coding  (PEP 8)  as well as other project structuring best practices. If you spot anything worth mentioning open an issue or make a correction yourself :)

