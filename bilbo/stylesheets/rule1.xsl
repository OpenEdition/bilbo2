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

		
<!-- AUTHOR -->
<!-- leading surname (Added author tag around surname and forename) -->
<xsl:template match="tei:surname[@bilbo][following-sibling::*[1][self::tei:forename]]" priority="1">
	<xsl:element name="author" namespace="http://www.tei-c.org/ns/1.0">
		<xsl:copy-of select=". | following-sibling::tei:forename[1][@bilbo]"/>
	</xsl:element>
</xsl:template>

<!-- leading forename (Added author tag around forename and surname) -->
<xsl:template match="tei:forename[@bilbo][following-sibling::*[1][self::tei:surname]]" priority="1">
	<xsl:element name="author" namespace="http://www.tei-c.org/ns/1.0">
		<xsl:copy-of select=". | following-sibling::tei:surname[1][@bilbo]"/>
	</xsl:element>
</xsl:template>

<!-- surname or forename, standalone (Added author around) -->
<xsl:template match="tei:surname[@bilbo] | tei:forename[@bilbo]">
	<xsl:element name="author" namespace="http://www.tei-c.org/ns/1.0">
		<xsl:copy-of select="."/>
	</xsl:element>
</xsl:template>

<!-- trailing surname (deleted) -->
<xsl:template match="tei:surname[@bilbo][preceding-sibling::*[1][self::tei:forename]]"/>

<!-- trailing forename (delete) -->
<xsl:template match="tei:forename[@bilbo][preceding-sibling::*[1][self::tei:surname]]"/>


<!-- TITLE -->
<!-- Renamed journal tag to title tag with j attribute -->
 <xsl:template match="tei:journal[@bilbo]">
	<xsl:element name="title" namespace="http://www.tei-c.org/ns/1.0">
 	<xsl:attribute name="level">j</xsl:attribute>
 	<xsl:attribute name="bilbo">True</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template>

<!-- Renamed booktitle tag to title tag with m attribute -->
 <xsl:template match="tei:booktitle[@bilbo]">
	<xsl:element name="title" namespace="http://www.tei-c.org/ns/1.0">
 	<xsl:attribute name="level">m</xsl:attribute>
 	<xsl:attribute name="bilbo">True</xsl:attribute>
		<xsl:value-of select="."/>
	</xsl:element>
</xsl:template>

<!-- BIBLSCOPE -->
<!-- Group together bilbscope, comma and date under biblscope when comma is '-'coy else -->
<xsl:template match="tei:biblScope[@bilbo]" priority="1">
        <xsl:choose>
		<xsl:when test="following-sibling::tei:c[1][text()[contains(., '-')]] and following-sibling::tei:c[1]/following-sibling::tei:date[1][@bilbo]">
			<xsl:copy>
				<xsl:apply-templates select="@*|node()"/>
				<xsl:value-of select="following-sibling::tei:c[1]"/>
				<xsl:value-of select="following-sibling::tei:c[1]/following-sibling::tei:date[1]"/>
			</xsl:copy>
		 </xsl:when>
		<xsl:when test="following-sibling::tei:c[1][text()[contains(., '-')]] and following-sibling::tei:c[1]/following-sibling::tei:biblScope[1][@bilbo]">
			<xsl:copy>
				<xsl:apply-templates select="@*|node()"/>
				<xsl:value-of select="following-sibling::tei:c[1]"/>
				<xsl:value-of select="following-sibling::tei:c[1]/following-sibling::tei:biblScope[1]"/>
			</xsl:copy>
		 </xsl:when>
		
		<xsl:when test="preceding-sibling::tei:c[text()[contains(., '-')]] and preceding-sibling::tei:c[1]/preceding-sibling::tei:biblScope[1][@bilbo]">
		 </xsl:when>

		 <xsl:otherwise>
			 <xsl:copy>
				<xsl:apply-templates select="@*|node()"/>
			 </xsl:copy>
		  </xsl:otherwise>
        </xsl:choose>
</xsl:template>

<!-- Deleted biblScope when preceded by comma and biblScope -->
<xsl:template match="tei:biblScope[@bilbo][preceding-sibling::*[1]/self::tei:c[text()[contains(., '-')]] and  preceding-sibling::*[2]/self::tei:biblScope[@bilbo]]"/>

<!-- Deleted comma when surrounded by biblScope and biblScope -->
<xsl:template match="tei:c[text()[contains(., '-')] and preceding-sibling::*[1]/self::tei:biblScope[@bilbo] and following-sibling::*[1]/self::tei:biblScope[@bilbo]]"/>

<!-- Deleted date when preceded by comma and biblScope -->
<xsl:template match="tei:date[@bilbo][preceding-sibling::*[1]/self::tei:c[text()[contains(., '-')]] and  preceding-sibling::*[2]/self::tei:biblScope[@bilbo]]"/>

<!-- Deleted comma when surrounded by date and biblScope -->
<xsl:template match="tei:c[text()[contains(., '-')] and preceding-sibling::*[1]/self::tei:biblScope[@bilbo] and following-sibling::*[1]/self::tei:date[@bilbo]]"/>


</xsl:stylesheet>
