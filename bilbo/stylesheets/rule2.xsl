<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:tei="http://www.tei-c.org/ns/1.0">
<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
<xsl:strip-space elements="*"/>

<!-- identity transform -->
<xsl:template match="@*|node()">
	<xsl:copy>
		<xsl:apply-templates select="node()[boolean(normalize-space())]|@*"/>
	</xsl:copy>
</xsl:template>


<!-- TITLE -->
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
