# First steps #

Keep in mind that bilbo has already been trained on a french and english annotated xml corpus.
It is trained on `<note>` and `<bibl>` section.
By default, bilboV2 is running (for annotation) on a specified pipeline with a default pre-trained model (french and english languages on `<bibl>` tag).   


## Command Line Interface API ##

### Overview Command Line Interface API ###
For an overview of different features and CLI command just launch in a shell :

```bash
cd bilbo_v2
bash bilbo/tests/bilbo_demo.sh  -v
```

### Common use ###

You will see that a quick use, to annotate your bibliographics references (indicate as `<bibl>` in TEI) just launch : 

```bash
cd bilbo_v2
python3 -m bilbo.bilbo --action tag -i PATH_TO_XMLFILE -o XML_OUTPUT_TAGGED
```

For annotate your footnote you need first to mention the tag to process (note) and specify explicitely the config file.
Currently the config file pipeline_note.cfg is available.


```bash
cd bilbo_v2
python3 -m bilbo.bilbo --action tag -t note -c bilbo/config/pipeline_note.cfg -i PATH_TO_XMLFILE -o XML_OUTPUT_TAGGED
```


For train, you just have to change --action=tag to --action=train and given an annotated input xml corpus. Note that output option is not necessay in this case. Saved trained model will be saved at the path indicated in the config file.  

## Interactive Python Interface ##

Open a terminal:
```bash
python3
```
In a interactive python shell:



<aside class="warning">
   WARNING!
   You have to be careful in interactive mode to the relative path of Python interpretor, xml file and of relative/absolute path in the configuration file.
</aside>



```
from bilbo.importer import Importer
from bilbo.bilbo import Bilbo

importer = Importer("path_to_your_xml_file")
doc = importer.parse_xml('tag(bibl or /note)')
bilb = Bilbo(doc, "path_config_file)
bilb.annotate("path_to_output.xml", format_=None)
```



