<xsl:stylesheet version="1.0" 
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   xmlns:tei = "http://www.tei-c.org/ns/1.0"
   exclude-result-prefixes="tei">
<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
<!-- <xsl:strip-space elements="*"/>-->
<!-- identity transform -->
<!--empty template suppresses this attribute-->
<xsl:template match="tei:c[@bilbo]">
		<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="tei:bibl/tei:bibl[@bilbo]">
		<xsl:value-of select="."/>
</xsl:template>

<xsl:template match="@bilbo"/>

<!--identity template copies everything forward by default-->

<xsl:template match="@*|node()">
	<xsl:copy>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:copy>
</xsl:template>

</xsl:stylesheet>
