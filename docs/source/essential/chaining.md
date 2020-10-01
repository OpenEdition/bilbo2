# Chaining algorithms
For chained Algorithms with action train, tag or evaluate you need to specified parameters in a configuration file. Two default configuration files are defined in *./bilbo/config/* directory. The order of data processing must be clarified. For each pipe you need to fullfilled the algorithm specification.  


For specify order and used algorithms see [pipeline options](../configuration/options.html#pipeline)


Each pipe is launching a component. At each passage, document object is enhanced from differents attribute. Attribute can be extract (extractor component class) or predict (estimator component class)


