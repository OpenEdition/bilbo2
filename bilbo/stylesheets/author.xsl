<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:tei="http://www.tei-c.org/ns/1.0">
<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
<xsl:strip-space elements="*"/>

<!-- identity transform -->
<xsl:template match="@*|node()">
	<xsl:copy>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:copy>
</xsl:template>

<!-- leading surname -->
<xsl:template match="tei:surname[@bilbo][following-sibling::*[1][self::tei:forename]]" priority="1">
	<xsl:element name="author" namespace="http://www.tei-c.org/ns/1.0">
		<xsl:copy-of select=". | following-sibling::tei:forename[1][@bilbo]"/>
	</xsl:element>
</xsl:template>

<!-- leading forename -->
<xsl:template match="tei:forename[@bilbo][following-sibling::*[1][self::tei:surname]]" priority="1">
	<xsl:element name="author" namespace="http://www.tei-c.org/ns/1.0">
		<xsl:copy-of select=". | following-sibling::tei:surname[1][@bilbo]"/>
	</xsl:element>
</xsl:template>

<!-- surname or forename, standalone -->
<xsl:template match="tei:surname[@bilbo] | tei:forename[@bilbo]">
	<xsl:element name="author" namespace="http://www.tei-c.org/ns/1.0">
		<xsl:copy-of select="."/>
	</xsl:element>
</xsl:template>

<!-- trailing surname -->
<xsl:template match="tei:surname[@bilbo][preceding-sibling::*[1][self::tei:forename]]"/>

<!-- trailing forename -->
<xsl:template match="tei:forename[@bilbo][preceding-sibling::*[1][self::tei:surname]]"/>

</xsl:stylesheet>
