<xsl:transform xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output version="1.0" encoding="UTF-8" indent="yes" />
<xsl:strip-space elements="*"/>

  <xsl:template match="/">
      <xsl:apply-templates select="root"/>
  </xsl:template>

  <xsl:template match="root">
      <xsl:apply-templates select="batch"/>
  </xsl:template>

  <xsl:template match="batch">
    <batch>
        <serial><xsl:value-of select="serial"/></serial>
        <valDate><xsl:value-of select="valDate"/></valDate>
        <valTime><xsl:value-of select="valTime"/></valTime>
        <recipeNumber><xsl:value-of select="recipeNumber"/></recipeNumber>
        <recipeDescription><xsl:value-of select="recipeDescription"/></recipeDescription>
        <mx><xsl:value-of select="mx"/></mx>
        <smflx><xsl:value-of select="smflx"/></smflx>
        <svty><xsl:value-of select="svty"/></svty>
        <sy><xsl:value-of select="sy"/></sy>
        <fz><xsl:value-of select="fz"/></fz>
    </batch>
  </xsl:template>

</xsl:transform>
