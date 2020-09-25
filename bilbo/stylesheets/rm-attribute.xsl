<xsl:stylesheet version="1.0" 
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:tei = "http://www.tei-c.org/ns/1.0"
   exclude-result-prefixes="tei">
<!--empty template suppresses this attribute-->


<xsl:template match="@bilbo"/>

<!--identity template copies everything forward by default-->

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>
</xsl:stylesheet>
