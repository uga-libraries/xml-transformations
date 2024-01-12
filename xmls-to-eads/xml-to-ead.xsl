<?xml version="1.0" encoding="utf-8"?>

<!--This stylesheet converts xml into EAD-->

<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
	<xsl:output method="xml" indent="yes"/>
	
	<!--Main template to construct the EAD-->
	<xsl:template match="/">
		<ead>
			<eadheader findaidstatus="Completed" repositoryencoding="iso15511" countryencoding="iso3166-1" dateencoding="iso8601" langencoding="iso639-2b">
				<!--not sure this is necessary but was part of AT's EAD export-->
				<eadid></eadid>
				<filedesc>
					<titlestmt>
              				<titleproper><num><xsl:value-of select="/dc/identifier"/></num></titleproper>
              			</titlestmt>
					<publicationstmt>
						<publisher>Hargrett Rare Books</publisher>
            		</publicationstmt>
				</filedesc>
			</eadheader>
			<archdesc level="collection">
				<xsl:call-template name="did"/>
				<xsl:call-template name="scopecontent"/>
				<xsl:call-template name="prefercite"/>
				<xsl:call-template name="controlaccess"/>
				<xsl:call-template name="dsc"/>
			</archdesc>
		</ead>
	</xsl:template>

	<!--number of copies of the file, calculated by the python script xmls-to-eads.py-->
	<xsl:param name="count" required="yes"/>

	<xsl:template name="did">
		<did>
			<unittitle><xsl:value-of select="/dc/title[1]"/><xsl:text> map</xsl:text></unittitle>
			<unitid><xsl:value-of select="/dc/identifier"/></unitid>
			<repository><corpname>Hargrett Rare Books</corpname></repository>
			<physdesc><extent>1.0 item</extent></physdesc>
			<xsl:if test="$count > 1">
				<physdesc><extent><xsl:value-of select="$count"/> copies</extent></physdesc>
			</xsl:if>
			<xsl:apply-templates select="/dc/coverage"/>
			<xsl:apply-templates select="/dc/source"/>
			<xsl:apply-templates select="/dc/creator"/>
		</did>
	</xsl:template>
	
	<!--The next three templates construct portions of the did section for elements that may be repeated or may not be present-->
	
	<!--Formats the date-->
	<xsl:template match="coverage">
		<xsl:choose>
			<!--Single year dates that are uncertain. Desired format is circa YYYY-->
			<!--Matches [YYYY] and [YYYY?]; Matches YYYY?; Matches c. YYYY and ca. YYYY and [ca. YYYY]--> 
			<xsl:when test="matches(., '^\[\d{4}') or matches(., '^\d{4}\?') or matches(., '^\[?ca?\. \d{4}\]?$')">
				<xsl:analyze-string select="." regex="(\d{{4}})">
					<xsl:matching-substring>
						<unitdate normal="{regex-group(1)}/{regex-group(1)}">
							<xsl:text>circa </xsl:text><xsl:value-of select="regex-group(1)"/>
						</unitdate>
					</xsl:matching-substring>
				</xsl:analyze-string>	
			</xsl:when>
			
			<!--Year range where both years are full years (4 digits). Desired format is circa YYYY-YYYY-->
			<!--Matches YYYY/YYYY and YYYY-YYYY and  ca. YYYY-YYYY-->
			<xsl:when test="matches(., '\d{4}[/-]\d{4}$')">
				<xsl:analyze-string select="." regex="(\d{{4}}).(\d{{4}})">
					<xsl:matching-substring>
						<unitdate normal="{regex-group(1)}/{regex-group(2)}">
						       <xsl:text>circa </xsl:text><xsl:value-of select="regex-group(1)"/><xsl:text>-</xsl:text><xsl:value-of select="regex-group(2)"/>
						</unitdate>
					</xsl:matching-substring>
				</xsl:analyze-string>	
			</xsl:when>
			
			<!--Year range where the end year is only 2 digits (YYYY/YY) because it is the same century as the start year, e.g. 1593/97 means 1593-1597. Desired format is circa YYYY-YYYY-->
            <xsl:when test="matches(., '^\d{4}/\d{2}$')">
				<!--Explanation of groups: 1. is first 4 digits of the first year, 2. is first 2 digits of the first year, and 3. is the 2 digits of the second year.-->
				<xsl:analyze-string select="." regex="((\d{{2}})\d{{2}})/(\d{{2}})">
					<xsl:matching-substring>
						<unitdate normal="{regex-group(1)}/{regex-group(2)}{regex-group(3)}">
						       <xsl:text>circa </xsl:text><xsl:value-of select="regex-group(1)"/><xsl:text>-</xsl:text><xsl:value-of select="regex-group(2)"/><xsl:value-of select="regex-group(3)"/>
						</unitdate>
					</xsl:matching-substring>
				</xsl:analyze-string>	
			</xsl:when>
			
			<!--Matches YYYY and anything unexpected-->
			<xsl:otherwise>
				<unitdate normal="{.}/{.}"><xsl:value-of select="."/></unitdate>
			</xsl:otherwise>
			
		</xsl:choose>
	</xsl:template>
	
	<!--Physical description-->
	<!--Replacing various abbreviations for color(ed) with the full text for better searching-->
	<xsl:template match="source">   
    		<physdesc label="General Physical Description note">
    		       <xsl:choose>
         		       <xsl:when test="contains(., 'uncol.')">
            			       <xsl:value-of select="replace(., 'uncol.', 'uncolored')"/>
        		       </xsl:when>
        		       <xsl:when test="contains(., 'hand col.')">
            			       <xsl:value-of select="replace(., 'hand col.', 'hand colored')"/>
        		       </xsl:when>
        		       <xsl:when test="contains(., 'col.')">
            			       <xsl:value-of select="replace(., 'col.', 'color')"/>
        		       </xsl:when>
        		       <xsl:when test="contains(., 'col ')">
            			       <xsl:value-of select="replace(., 'col ', 'color ')"/>
        		       </xsl:when>
        		       <xsl:otherwise>
					<xsl:value-of select='.'/>
	                     </xsl:otherwise>
                     </xsl:choose>
              </physdesc>
       </xsl:template>
    
	<!--Creator(s)-->
	<xsl:template match="creator">
		<origination label="creator">
			<persname rules="aacr" source="naf" role="Cartographer (ctg)">
				<xsl:value-of select="."/>
			</persname>
		</origination>
	</xsl:template>
	
	<xsl:template name="scopecontent">
		<!--These are maps without any of the 3 things that go into scopecontent (alternative titles, which are all but the first title, description fields, and the publisher field)-->
		<xsl:if test="/dc/title[2] or /dc/description or /dc/publisher">
			<scopecontent>
				<head>Scope and Contents note</head>
				<p>
					<!--Selecting titles that have a preceding title so that don't include the first title-->
					<xsl:for-each select="/dc/title[preceding::title]">
                                          <xsl:text>Alternate title: </xsl:text>
                                          <xsl:value-of select="."/>
                                          <!--not putting a trailing ";" if it is the last item in the scope content note-->
                                          <xsl:choose>
                                                 <xsl:when test="not(following-sibling::description) and not(following-sibling::publisher)">
                                                        <xsl:if test="position() != last()">; </xsl:if>
                                                 </xsl:when>
                                                 <xsl:otherwise>
                                                        <xsl:text>; </xsl:text>
                                                 </xsl:otherwise>
                                          </xsl:choose>
					</xsl:for-each>
					<xsl:for-each select="/dc/description">
					      <!--Skipping if the description tag is present but empty. This is the only element in our data which does that.-->
					       <xsl:if test=". != ''">
			                            <xsl:value-of select="."/>
			                            <!--not putting a trailing ";" if it is the last item in the scope content note-->
			                            <xsl:choose>
                                                        <xsl:when test="not(following-sibling::publisher)">
                                                               <xsl:if test="position() != last()">; </xsl:if>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                               <xsl:text>; </xsl:text>
                                                        </xsl:otherwise>
                                                 </xsl:choose>
                                          </xsl:if>
					</xsl:for-each>
					<xsl:if test="/dc/publisher">Publication: <xsl:value-of select="/dc/publisher"/></xsl:if>
				</p>
			</scopecontent>
		</xsl:if>
	</xsl:template>
	
	<xsl:template name="prefercite">
		<prefercite>
		    <head>Preferred Citation note</head>
			<p><xsl:value-of select="/dc/title[1]"/>, <xsl:value-of select="/dc/identifier"/>, Hargrett Rare Book and Manuscript Library, The University of Georgia Libraries.</p>
		</prefercite>
	</xsl:template>
	
	<xsl:template name="controlaccess">
		<controlaccess>
			<genreform source="aat">Maps.</genreform>
			<xsl:for-each select="/dc/subject">
				<genreform source="lcsh"><xsl:value-of select="."/>.</genreform>
			</xsl:for-each>
		</controlaccess>
	</xsl:template>
	
	<xsl:template name="dsc">
		<dsc>
			<c01 level="item">
				<did>
					<unittitle><xsl:value-of select="/dc/title[1]"/></unittitle>
					<container type="Item" label="Maps"><xsl:value-of select="/dc/identifier"/></container>
					<xsl:apply-templates select="/dc/coverage"/>
				</did>
			</c01>
		</dsc>
	</xsl:template>

</xsl:stylesheet>
