# CLI toolkit usage #

If you want to start and understand how bilbo is handling each pipeline, you can launch independantly some test on bilbo component. As above you can do in CLI or in Interactive Python. Beware input of each component. Examples: it does not make sense to lauch CRF modules if you have not extract features previously (in a file or in bilbo data structure).


## Overview ##

For an overview and a test of cli usage, from a terminal, run:

```
cd bilbo2
/bin/bash bilbo/tests/bilbo_demo.sh -v
```

You can add -v argument to see output. 

## Command Line Interface API ##


To see an exhaustive list of modules which could be used by bilbo you can launch

```
python3 -m bilbo.bilbo -L
```

For instance, you should see wich features are extracted for each token according to the default configuration file.
Your features (crf++ format) will be extracted in the output file mentioned in "bilbo/config/pipeline_bibl.cfg"
If you want to see explicit output just add -vvvv for a logger output.


```
python3 -m bilbo.components.features -cf bilbo/config/pipeline_bibl.cfg -s "Amblard F., Bommel P., Rouchier J., 2007, « Assessment and validation of multi-agent models »...."
```

In order to improve your research you want to analyse directly from a crf++ input format and crf++ pattern your prediction.
 
```
python3 -m bilbo.components.crf -cf bilbo/config/pipeline_bibl.cfg -i bilbo/testFiles/features.output.txt --tag -v
```

