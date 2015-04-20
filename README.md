##Directory miscn

TO be provided.

## Directory csdms 

The files in the CSDMS directory support auto-generating the 4 CSDMS ORR-ready ontologies for objects, quantities, operators, and assumptions. They assume the CSDMS 0.8.1 ontology format (likely to change, alas), and perform all the necessary tweaks to transform the files into a .owl form that ORR likes.

Broadly, the csdms_converter.py file reads the configuration file that has been specified on the run-line (only been used in Python notebook form so far -- I hand-edit the default configuration file name), from that learns the destination file, and all the mappings (in individual JSON objects) for the different components (header, from a header template, and body, from matching lines in the CSDMS.owl file). The OWL file is stored and used locally for convenience, as the source file on-line seems likely to evolve.

The main changes required included:
* changing rdf:ID to rdf:about, and the term ID to a full path ID
* removing prefixes from quantity, object, and operator terms
* defining the main classes locally, rather than in the geo file/space, and adding an rdfs:comment for them
* and a bunch of tweaks and documentation in the header (metadata and OWL header) content
