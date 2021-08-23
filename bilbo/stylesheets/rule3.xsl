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

<xsl:template match="tei:bibl[not(@bilbo)]">
	<xsl:element name="bibl" namespace="http://www.tei-c.org/ns/1.0">
	<xsl:for-each select="*">
		<xsl:choose>
			<xsl:when test="not(self::tei:title[1][@bilbo] and not(self::tei:title[1][@level]))">
				<xsl:copy>
					<xsl:apply-templates select="@*|node()"/>
				</xsl:copy>
			</xsl:when>
			<xsl:when test="not(name(preceding-sibling::*[1]) = 'title' and not(preceding-sibling::*[1]/self::tei:title[1][@level]))">
				<xsl:element name="title" namespace="http://www.tei-c.org/ns/1.0">
				<xsl:attribute name="bilbo">True</xsl:attribute>
				<xsl:value-of select="."/>
				<xsl:call-template name="create-group">
					<xsl:with-param name="list" select="following-sibling::*" />
				</xsl:call-template>
				</xsl:element>
			</xsl:when>
		</xsl:choose>
	</xsl:for-each>
	</xsl:element>
</xsl:template>

<xsl:template name="create-group">
<xsl:param name="list" />
<xsl:if test="(name($list[1]) = 'title' and not($list[1][@level]))">
	<xsl:value-of select="$list[1]" />
	<xsl:call-template name="create-group">
		<xsl:with-param name="list" select="$list[position() > 1]" />
	</xsl:call-template>
</xsl:if>   
</xsl:template>

</xsl:stylesheet>
