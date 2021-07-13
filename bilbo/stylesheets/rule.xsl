<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:tei="http://www.tei-c.org/ns/1.0">
<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>

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



<!-- Added sibling comma to title tag -->
 <xsl:template match="tei:title[@bilbo]" priority="1">
        <xsl:choose>
		<xsl:when test="following-sibling::tei:c[@bilbo][1]" >
			<xsl:copy>
				<xsl:apply-templates select="@*|node()"/>
				<xsl:value-of select="following-sibling::tei:c[@bilbo][1]"/>
			</xsl:copy>
		 </xsl:when>

		 <xsl:otherwise>
			 <xsl:copy>
				<xsl:apply-templates select="@*|node()"/>
			 </xsl:copy>
		  </xsl:otherwise>
        </xsl:choose>
</xsl:template>



<!-- Deleted sibling comma after a title tag, copy else --> 
<xsl:template match="tei:c[@bilbo][preceding-sibling::*[1][self::tei:title]]" />



</xsl:stylesheet>
