# Input - Output

## Input
Input must be a valid XML document. Bilbo has be trained on [TEI-XML](https://tei-c.org/) format (Text Echange Initiative) format. But you could give a [JATS](https://jats.nlm.nih.gov/) input format...
Actually, any valid XML document can be used for bilbo, the annoatation tagging will be done according to TEI schemas.



### Scope of annotation
Bilbo is only handling a scope inside a xml. This scope is bounded by a tag. Element outside the scope are only kept in memory to rebuild the xml file as a result.  



## Output
Output is XML. Bilbo has personnal output for research purpose: this output schema is the default xml output. Any output schema can be specified from this default schema. For this, an xsl sheet must contain the xml conversion. This xsl file should be placed in `bilbo/stylesheets/` directory.
You can specified TEI (Text Echange Initiative), JATS format and personal research.

### XML/TEI OpenEdition Schema

The TEI schema versions is used by the OpenEdition Books and OpenEdition Journals platforms. It is associated to the journals editorial model shipped with the Lodel software https://github.com/OpenEdition/lodel

Among the different XML encoding standards for machine-readable texts, the TEI ([Text Encoding Initiative](http://www.tei-c.org/)) is probably the most comprehensive and mature. The TEI Guidelines define some 500 different textual components and concepts (word, sentence, character, glyph, person, etc.). Any particular usage of the TEI supposes a customization of the TEI to their specificities, so as to adapt and constraint the richness of the TEI to a well scoped and tuned schema. The TEI community has created a specification language called ODD [("One Document Does it all")](http://www.tei-c.org/Guidelines/Customization/odds.xml) to modify the general TEI schema. Having ODD descriptions, it is possible with a tool called Roma to generate automatically customised TEI schemas (xsd, relaxNG, etc.) and some documentation.

### JATS


<aside class="warning">
An xslt sheet (xsl Tranformations) is currently being written. For now, this has not been integrated into the repository.
</aside>


### Personnal research output

This is  NOT A VALID XML/TEI schemas. It is only set for research purpose. Each added tag is mentionned by a an attribute `bilbo="true"`. It could be used to analyse in a same xml document difference between manual annotated and automatic annotation.  
