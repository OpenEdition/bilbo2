# Purpose

## Context
In academic papers, bibliographies are an essential aspect of research.
In many case, only few bibiographic references are identified by an information system.

We can consider that there are three levels of detections of bibliographic references:

* Standart bibliographique references: These are usually located at the end of the scientific article.
There are mentioned in a TEI-XML document by the tag `<bibl>`
* Footnote: Footnote do not mentioned every time a bibliography. The classification of notes that contains bibliographies or not is the main difficulty
Implemented by the tag `<note>` (TEI-XML Document). 
* Implicit reference. In the full text, authors mention sometimes a references bibliography. This reference is partial and explicit.
Implemented by the tag `<p>` (TEI-XML Document). 

## Philosophy

Algoritym complexity to extract bibliography  is increasing at each level (`<bibl>`,`<note>`,`<p>`).
Currently, the first level could be considered as efficient. The others not.
Bilbo_v2 is considered to be dedicated to research.
It has been thought to be a tools for implement easily new machine learning algorithms at any level of bibliography.
Everything has been done so that we can easily add new algorithms to existing codes without affecting what can be deployed in production.
Data structure of a document is constructed to manipulate a Document at any level. A level (that we called a section) is a tag. The scope of processing algorithm will be the section choosen. Then all sections corresponding to this tag will be processed.
Each instance bilbo is specialized in a specific tag. To handle different type of tag, you can pass and process each time the xml document.


