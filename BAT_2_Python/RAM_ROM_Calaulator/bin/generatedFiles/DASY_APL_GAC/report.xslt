<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output
  method="html"
  media-type="text/html" 
  doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
  doctype-system="DTD/xhtml1-strict.dtd"
  cdata-section-elements="script style"
  indent="yes"
  encoding="UTF-8" />

  <xsl:template match="REPORT">
    <HTML>
      <HEAD>
        <TITLE>resCalcAurix report</TITLE>
      </HEAD>
      <BODY>
        <H1>resCalcAurix report</H1>
        <H3>Report version: <xsl:value-of select="@version" /></H3>
        <H3>Ordering type:
          <xsl:choose>
            <xsl:when test="@order = 'descending_percentage' and @order != ''">
              descending by occupation (<xsl:value-of select="@order" />)
            </xsl:when>
            <xsl:otherwise>not defined</xsl:otherwise>
          </xsl:choose>
        </H3>
        <H3>Summary</H3>
        <H4>RAM: <xsl:value-of select="@ram" /> [Byte] / Used RAM: <xsl:value-of select="@ramUsed" /> [Byte] = Occupation: <xsl:value-of select="number(translate(@ramPercent,',','.'))" /> [%]</H4>
        <H4>ROM: <xsl:value-of select="@rom" /> [Byte] / Used ROM: <xsl:value-of select="@romUsed" /> [Byte] = Occupation: <xsl:value-of select="number(translate(@romPercent,',','.'))" /> [%]</H4>
        <TABLE rules="all" border="1">
           <TR>
                <TH style="wIDth:500px">Name</TH>
                <TH style="wIDth:110px">Address</TH>
                <TH style="wIDth:110px">Size [Byte]</TH>
                <TH style="wIDth:110px">Used [Byte]</TH>
                <TH style="wIDth:110px">Occupation [%]</TH>
                <TH style="wIDth:110px">Free [%]</TH>
                <TH style="wIDth:110px">Free Size [Byte]</TH>
          </TR>
          <xsl:for-each select="SUMMARY/ELEMENT">
            <xsl:variable name="percentageAsNumber" select="number(translate(@percentage,',','.'))" />
          <TR>
              <TD><xsl:value-of select="@name" /></TD>
              <TD><xsl:value-of select="@address" /></TD>
              <TD><xsl:value-of select="@size" /></TD>
              <TD><xsl:value-of select="@occupation" /></TD>
              <xsl:choose>
                <xsl:when test="$percentageAsNumber &gt; 100">
                  <TD bgcolor="red"><xsl:value-of select="@percentage" /></TD>
                </xsl:when>
                <xsl:when test="($percentageAsNumber &gt; 90)
                            and ($percentageAsNumber &lt; 100)">
                  <TD bgcolor="orange">
                    <xsl:value-of select="@percentage" />
                  </TD>
                </xsl:when>
                <xsl:when test="($percentageAsNumber &gt; 80)
                            and ($percentageAsNumber &lt; 90)">
                  <TD bgcolor="yellow"><xsl:value-of select="@percentage" /></TD>
                </xsl:when>
                <xsl:otherwise>                  
                  <TD><xsl:value-of select="@percentage" /></TD>
                </xsl:otherwise>
              </xsl:choose>              
              <TD><xsl:value-of select="@free_percentage" /></TD>
              <TD><xsl:value-of select="@free_sapce" /></TD>
            </TR>
          </xsl:for-each>
        </TABLE>
        <H3>Library detailed information</H3>
        <TABLE rules="all" border="1">
          <TR>
            <TH style="wIDth:500px">Name</TH>
            <TH style="wIDth:110px">Flash Used [Byte]</TH>
            <TH style="wIDth:110px">RAM Used [Byte]</TH>
          </TR>
          <xsl:for-each select="DETAILS/ELEMENT">
            <xsl:variable name="percentageAsNumber" select="number(translate(@percentage,',','.'))" />
            <TR>
              <TD>
                <xsl:value-of select="@name" />
              </TD>
              <TD>
                <xsl:value-of select="@flash_occupation" />
              </TD>
              <TD>
                <xsl:value-of select="@ram_occupation" />
              </TD>
            </TR>
            <xsl:for-each select="SUBELEMENTS/SUBELEMENT">
              <TR>
                <TD style="padding-left: 25px">
                  <xsl:value-of select="@name" />
                </TD>
                <TD>
                  <xsl:value-of select="@flash_occupation" />
                </TD>
                <TD>
                  <xsl:value-of select="@ram_occupation" />
                </TD>
              </TR>
            </xsl:for-each>
          </xsl:for-each>
        </TABLE>
      </BODY>
    </HTML>
</xsl:template>
</xsl:stylesheet>