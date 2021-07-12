<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:tei="http://www.tei-c.org/ns/1.0">
<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
<xsl:strip-space elements="*"/>

<!-- identity transform -->
<xsl:template match="@*|node()" name="identity">
	<xsl:copy>
		<xsl:apply-templates select="@*|node()"/>
	</xsl:copy>
</xsl:template>


 <xsl:template match="tei:title[@bilbo]">
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



<xsl:template match="tei:c[@bilbo]">
	<xsl:choose>
		<xsl:when test="preceding-sibling::tei:title[@bilbo][1]" >
		</xsl:when>

		<xsl:otherwise>
			<xsl:copy>
				<xsl:apply-templates select="@*|node()"/>
			</xsl:copy>
		</xsl:otherwise>
	</xsl:choose>
</xsl:template>


</xsl:stylesheet>
