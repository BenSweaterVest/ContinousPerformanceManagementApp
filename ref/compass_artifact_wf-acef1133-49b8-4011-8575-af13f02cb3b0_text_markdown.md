# Comprehensive Documentation for Programmatic Microsoft Teams Power Apps Creation

Microsoft's documentation for hand-writing Dataverse solution files contains critical gaps that force developers into trial-and-error cycles. **The core problem: even Microsoft's own out-of-the-box forms fail validation against their published XSD schemas**—roughly 9-21% of production forms use undocumented attributes. This guide consolidates official documentation with reverse-engineered community knowledge to enable programmatic Power Apps generation.

Your discovery that 38 metadata elements exist when only 19 are documented exemplifies the documentation drift problem. The official XSD schema (version 9.0.0.2090, last updated February 2022) lags 2-3 years behind platform versions currently running 9.2.25063.192. This report provides the complete specifications you need.

## Solution XML Schema & Format

### Official Schema Download and Structure

Microsoft provides schema files, but with significant caveats. Download the complete XSD package from: https://download.microsoft.com/download/B/9/7/B97655A4-4E46-4E51-BA0A-C669106D563F/Schemas.zip

This package includes **CustomizationsSolution.xsd** (root schema), FormXml.xsd, SiteMap.xsd, Fetch.xsd, RibbonCore.xsd, and related schemas. All files must reside in the same directory for proper validation. Configure Visual Studio to associate customizations.xml with CustomizationsSolution.xsd for IntelliSense support.

**Critical finding from community research**: The published XSD schemas contain undocumented attributes used in production. In clean sandbox environments, 22 of 258 forms (9%) fail validation. With Sales and Customer Service solutions installed, this jumps to 307 of 1,462 forms (21%). Undocumented attributes include `headerdensity`, `showinformselector`, `showcommandbar`, `showbody`, `showtabnavigator`, `contenttype`, and `visible`—all absent from official XSD but present in Microsoft's own forms.

### Complete Entity Definition Requirements

Every entity in customizations.xml requires these core child elements within the `<Entity>` block:

**EntityInfo section** containing entity metadata (Name, ObjectTypeCode, IsCustomEntity, OwnershipType, IsActivity, IsConnectionsEnabled), **FormXml section** with form definitions organized by type (main, quick create, quick view, card), **SavedQueries section** for view definitions with FetchXML and LayoutXML, **EntityRelationships section** defining 1:N, N:1, and N:N relationships.

System relationships (owner, createdby, modifiedby, createdonbehalfby, modifiedonbehalfby, owningbusinessunit, owningteam, owninguser) are automatically created for user-owned entities with specific cascade behaviors. These are non-customizable and cannot be deleted. The XML structure for relationships includes:

```xml
<EntityRelationship>
  <EntityRelationshipType>OneToMany</EntityRelationshipType>
  <IsCustomRelationship>true</IsCustomRelationship>
  <IntroducedVersion>1.0.0.0</IntroducedVersion>
  <EntityRelationshipRoles>
    <EntityRelationshipRole>
      <NavPaneDisplayOption>UseCollectionName|UseLabel|DoNotDisplay</NavPaneDisplayOption>
      <NavPaneArea>Details|Sales|Service|Marketing</NavPaneArea>
      <NavPaneOrder>10000</NavPaneOrder>
    </EntityRelationshipRole>
  </EntityRelationshipRoles>
  <CascadeConfiguration>
    <Assign>NoCascade|Cascade|Active|UserOwned</Assign>
    <Delete>NoCascade|Cascade|RemoveLink|Restrict</Delete>
    <Merge>NoCascade|Cascade</Merge>
    <Reparent>NoCascade|Cascade|Active|UserOwned</Reparent>
    <Share>NoCascade|Cascade|Active|UserOwned</Share>
    <Unshare>NoCascade|Cascade|Active|UserOwned</Unshare>
  </CascadeConfiguration>
</EntityRelationship>
```

### Comprehensive Attribute Metadata Specifications

The official XSD defines 30+ top-level attribute metadata elements, though your discovery of 38 likely includes nested complex types. **The complete attribute element list includes**:

**Core identification**: Type (CrmDataType, required), Name, LogicalName, ExternalName, IsCustomField, DisplayMask (free-form string, not enumerated)

**API validation flags**: ValidForCreateApi, ValidForReadApi, ValidForUpdateApi (all TrueFalse01Type)

**Data constraints**: Length, MaxLength, MinValue, MaxValue, Accuracy, AccuracySource, Format

**Relationships**: AttributeOf, YomiOf, CalculationOf, AggregateOf (for rollup/calculated fields)

**Security and audit**: IsAuditEnabled, IsSecured, IsDataSourceSecret

**Customization control**: IsCustomizable, IsRenameable, CanModifySearchSettings, CanModifyRequirementLevelSettings, CanModifyFieldLevelSecuritySettings, CanModifyAdditionalSettings, CanModifyGlobalFilterSettings, CanModifyIsSortableSettings

**Version control**: **IntroducedVersion** (VersionType, critical for proper import), SourceType, FormulaDefinitionFileName

**Display configuration**: RequiredLevel, ImeMode, LinkedAttribute, XmlAbbreviation

**Lookup-specific**: ReferencedEntityObjectTypeCode, LookupBrowse, LookupStyle, LookupTypes

**DateTime behavior**: Behavior (0=UserLocal, 1=DateOnly, 2=TimeZoneIndependent, 3=TimeZoneIndependentDateOnly), CanChangeDateTimeBehavior

**Display elements**: displaynames (localized labels with languagecode attributes), Descriptions, OptionSetName, optionset definitions, AppDefaultValue

**Advanced features**: IsGlobalFilterEnabled, IsSortableEnabled, IsActive, IsLogical

### IntroducedVersion Formatting Rules

IntroducedVersion uses a four-part version string (major.minor.build.revision). **System fields** use organization version numbers matching the Dataverse platform version when introduced (e.g., "5.0.0.0", "9.0.0.0"). **Custom fields** must use solution version numbers matching the solution version where first introduced, critical for proper ALM operations.

This applies across all components: entities use `<IntroducedVersion type="VersionType" minOccurs="0" maxOccurs="1" />`, and the same format extends to OptionSets, Workflows, and Web Resources. Always set IntroducedVersion for custom components to match your solution version.

### DisplayMask Values and Limitations

**Critical documentation gap**: DisplayMask is defined in the XSD as type `xs:string` with optional occurrence, but Microsoft provides no enumeration of valid values. The schema allows free-form strings, suggesting custom patterns are supported. DisplayMask controls input masking in model-driven apps for single-line text fields (phone numbers, postal codes, custom patterns) without data validation.

Related documentation on data type format conversions shows format options for different data types (Phone, Email, Duration) but doesn't provide the complete DisplayMask specification. This is best discovered by exporting existing solutions with similar field types and examining their DisplayMask values.

### Required XML Sections in Customizations.xml

The customizations.xml file requires this structure:

```xml
<ImportExportXml version="9.2.0.0" SolutionPackageVersion="9.2" 
                 languagecode="1033" generatedBy="CrmLive">
```

**Main sections in order** (not all required; only include sections with actual content): Entities, Roles, Workflows, FieldSecurityProfiles, Templates, EntityMaps, EntityRelationships, OrganizationSettings, optionsets, WebResources, CustomControls, SolutionPluginAssemblies, SdkMessageProcessingSteps, ServiceEndpoints, Reports, Dashboards, SiteMap, RibbonDiffXml, AppModules, Languages.

### Solution.xml File Structure

Located at the solution ZIP root alongside customizations.xml:

```xml
<ImportExportXml version="9.2.0.0" SolutionPackageVersion="9.2" 
  languagecode="1033" generatedBy="CrmLive">
  <SolutionManifest>
    <UniqueName>solution_uniquename</UniqueName>
    <LocalizedNames>
      <LocalizedName description="Solution Display Name" languagecode="1033" />
    </LocalizedNames>
    <Version>1.0.0.0</Version>
    <Managed>0</Managed> <!-- 0=Unmanaged, 1=Managed -->
    <Publisher>
      <UniqueName>publisher_prefix</UniqueName>
      <CustomizationPrefix>prefix</CustomizationPrefix> <!-- 3-8 chars -->
      <CustomizationOptionValuePrefix>10000</CustomizationOptionValuePrefix>
    </Publisher>
    <RootComponents>
      <RootComponent type="1" id="{GUID}" behavior="0" />
      <!-- Types: 1=Entity, 2=Attribute, 9=OptionSet, 26=View, 29=Process, 
           60=Dashboard, 62=Form, 300=Canvas App -->
    </RootComponents>
  </SolutionManifest>
</ImportExportXml>
```

**Component behavior values**: 0 = Include Subcomponents, 1 = Do Not Include Subcomponents, 2 = Include As Shell Only.

**Undocumented finding**: Connection Reference component codes are NOT fixed. Documentation states code 10039, but community research reveals they start at 10000+ and increment sequentially based on installation order, meaning codes differ between environments. Query with `objecttypecode eq componentCode` to determine actual values.

## Canvas App File Formats

### .msapp File Structure and Critical Warnings

**The .msapp file is a ZIP archive**, but **critical undocumented requirement**: you cannot simply unzip and rezip. The file requires special compression handled by Power Platform CLI. Manual zip operations will fail on import. Always use `pac canvas unpack` and `pac canvas pack`.

After unpacking with PAC CLI, the directory structure contains:

```
/src/ - Source code in .pa.yaml format (or legacy .fx.yaml)
  ├── App.pa.yaml
  ├── [ScreenName].pa.yaml (one per screen)
  ├── /Component/ - Custom components
  └── /EditorState/ - Editor metadata (App.editorstate.json, screen-specific files)

/DataSources/ - Data source definitions (JSON)
/Connections/ - Connections.json
/Assets/ - Media files (images, audio, video, PDFs)
/pkgs/TableDefinitions/ - Table schema details
/other/ - entropy.json, checksum.json, References/Theme.json

CanvasManifest.json (root)
ComponentReferences.json
ControlTemplates.json
```

**Breaking change documented by community**: The .msapp structure changed approximately 2 years ago. Old tutorials referencing entities.json are obsolete.

### .pa.yaml Format Documentation (Current Schema v3.0)

**.pa.yaml is the current human-readable source code format** for Canvas Apps. Status: Active development. Official schema location: https://github.com/microsoft/PowerApps-Tooling/blob/master/schemas/pa-yaml/v3.0/pa.schema.yaml

JSON Schema for IDE validation: https://raw.githubusercontent.com/microsoft/PowerApps-Tooling/master/docs/pa.yaml-schema.json

**Configure VS Code validation**:
```json
{
  "yaml.schemas": {
    "https://raw.githubusercontent.com/microsoft/PowerApps-Tooling/master/docs/pa.yaml-schema.json": "*.pa.yaml"
  }
}
```

**Power Fx YAML Formula Grammar Rules**:

All formulas start with `=` (Excel-style). Space between `:` and `=` required for YAML compliance. Single-line formulas: `PropertyName: =Expression`. Multi-line formulas use YAML block scalar indicators:

```yaml
PropertyName: |
  =If(condition,
     trueResult,
     falseResult)
```

**Restrictions**: `#` and `:` not allowed in single-line formulas (use multi-line instead). YAML comments (`#`) are not preserved—use Power Fx comments (`//` or `/* */`). Normal YAML escaping not supported.

**Control versioning**: Specify versions with `@` operator:
```yaml
Button1:
  Control: Button@2.3.0
  Properties:
    Text: ="Click me"
```

**ZIndex ordering**: All controls use ascending order starting from 1.

**Top-level nodes**: App (application-level properties), Screens (screen definitions), DataSources (mappings), ComponentDefinitions (custom components).

### .fx.yaml Format (Legacy - Deprecated)

**Status: Retired**. Original experimental format by Power Platform CLI. Files named `*.fx.yaml` in `/src/` folder. **Cannot directly convert .fx.yaml to .pa.yaml**. Migration requires: Package as .msapp → Import to Power Apps Studio → Re-export. Studio will convert to current format.

### CanvasManifest.json Complete Structure

Located at root of unpacked .msapp directory. Contains metadata about the published app:

```json
{
  "FormatVersion": "string",
  "Properties": {
    "AppCreationSource": "string",
    "AppDescription": "string",
    "AppName": "string",
    "AuthorizationReferences": [],
    "BackgroundColor": "RGBA(value)",
    "DocumentAppType": "Phone|Tablet|Desktop",
    "DocumentLayoutHeight": number,
    "DocumentLayoutWidth": number,
    "EnableInstrumentation": boolean,
    "FileID": "guid",
    "Id": "guid",
    "LocalDatabaseReferences": {},
    "OriginatingVersion": "string"
  },
  "Header": {
    "DocVersion": "string",
    "MinVersionToLoad": "string",
    "MSAppStructureVersion": "string"
  },
  "PublishInfo": {
    "AppName": "string",
    "BackgroundColor": "string",
    "IconName": "string",
    "IconColor": "string",
    "PublishTarget": "string"
  }
}
```

Contains app name/description/ID, form factor (Phone/Tablet/Desktop), canvas dimensions, version information, authorization and data references, theme/background colors, and logo/icon references (typically in /Assets/).

### entropy.json Purpose and Format

Located at `/other/entropy.json`. **Purpose**: Collects "volatile elements" needed for faithful round-tripping but can be safely ignored or deleted for version control.

**Contains**: Timestamps (creation/modification times), checksums (round-trip validation), order information (original ordering that doesn't affect functionality), volatile metadata (changes frequently but doesn't affect app logic).

**Usage guidance**: Safe to delete (can be regenerated). Safe to take latest version during merges. Not user-editable (managed by pac CLI tools). Include in .gitignore for cleaner version control. Microsoft states: "A file where we collect all the other bits of information needed for us to faithfully roundtrip the app, but can be easily ignored and/or deleted at any time."

### DataSources Folder Format and Requirements

Located at `/DataSources/` in unpacked .msapp. Defines all data sources including connected data sources (SharePoint, SQL, Dataverse), static/imported data (Excel tables), collections, and sample data.

**File format (JSON)**:
```json
{
  "Name": "DataSourceName",
  "Type": "Table|Actions",
  "ConnectorId": "optional-connector-guid",
  "OrderedColumnNames": ["Column1", "Column2"],
  "Schema": [
    "Column1:s",  // s=string
    "Column2:n",  // n=number
    "Column3:d",  // d=date
    "Column4:b"   // b=boolean
  ],
  "Parameters": {"key": "value"}
}
```

**Data type codes**: s=String/Text, n=Number, d=Date/DateTime, b=Boolean, c=Color, h=Hyperlink.

**Static data format** for imported Excel data:
```json
{
  "Name": "StaticDataSource",
  "Type": "StaticDataSource",
  "OrderedColumnNames": ["Name", "Value"],
  "Schema": ["Name:s", "Value:n"],
  "Data": [
    {"Name": "Item1", "Value": 100},
    {"Name": "Item2", "Value": 200}
  ]
}
```

Date values are expressed in Unix timestamp format (milliseconds since epoch). `/pkgs/TableDefinitions/` contains detailed table schemas with DataEntityMetadataJson (escaped JSON with full column definitions) and ConnectedDataSourceInfoNameMapping (maps display names to logical names).

### Connections Folder Structure

Located at `/Connections/` with primary file `Connections.json`. Stores connection instances saved with the app for reloading into Power Apps Studio.

**Format**:
```json
{
  "ConnectionGuid": {
    "connectionRef": "connection-reference-name",
    "connectionId": "guid",
    "datasourceId": "datasource-guid",
    "id": "connection-guid",
    "apiId": "/providers/Microsoft.PowerApps/apis/connector-name"
  }
}
```

**Security note**: Does NOT contain actual login tokens or credentials. Only GUIDs pointing to environment where tokens are stored. Deleting connection files is similar to "logging out". Connections are environment-specific and must be reconfigured when moving between environments.

**Merge conflict handling**: If merge conflicts occur under `/Connections/`, it's NOT safe to merge automatically. Connections can vary by environment and user.

### Assets Folder Requirements

Located at `/Assets/`. Contains all media files embedded in the app.

**Supported file types**: Images (.jpg, .png, .gif, .svg), Videos (.mp4, .mov), Audio (.mp3, .wav), Documents (.pdf), Icons/Logos (app icon referenced in CanvasManifest.json).

Files can be easily copied for reuse. Binary files stored as-is (not base64 in most cases). Referenced in controls via resource name. Empty if no media: `{ "Resources": [] }`.

### File Interrelationships and Workflow

**Cross-references**: Formulas in .pa.yaml reference DataSource names from /DataSources/. DataSources reference ConnectionIds from /Connections/. CanvasManifest.json references Assets (logo.jpg). EditorState files mirror structure of .pa.yaml files. entropy.json tracks metadata for all files.

**Unpack process** (`pac canvas unpack`): .msapp (ZIP) → JSON preserved as-is, Control JSON converted to .pa.yaml, Formulas extracted and placed in .pa.yaml with =, Metadata goes to entropy.json and checksum.json.

**Pack process** (`pac canvas pack`): Source files → .pa.yaml converted to control JSON, All JSON files validated and included, Assets copied to package, entropy.json used for validation → .msapp (ZIP).

**Merging strategy for version control**: Always merge `/src/*.pa.yaml` (actual source code). Take latest version for `/other/checksum.json` and `/other/entropy.json`. Safe to delete `/src/EditorState/*.editorstate.json` and `/other/entropy.json`. NOT safe to merge `/Connections/*`, `/DataSources/*`, `/pkgs/*`, or `CanvasManifest.json`.

## Model-Driven App Definitions

### FormXML Schema and Structure

**Official documentation**: https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/form-xml-schema

Download XSD schemas from Microsoft (same package as solution schemas). FormXml.xsd defines form structure.

**Complete FormXML structure**:

```xml
<form>
  <tabs>
    <tab name="tabName" id="{guid}" expanded="true" verticallayout="true">
      <labels>
        <label description="Tab Label" languagecode="1033" />
      </labels>
      <columns>
        <column width="100%">
          <sections>
            <section name="sectionName" showlabel="true" showbar="true" id="{guid}">
              <labels>
                <label description="Section Label" languagecode="1033" />
              </labels>
              <rows>
                <row>
                  <cell id="{guid}" showlabel="true" colspan="1">
                    <labels>
                      <label description="Field Label" languagecode="1033" />
                    </labels>
                    <control id="fieldname" classid="{guid}" datafieldname="fieldname" />
                  </cell>
                </row>
              </rows>
            </section>
          </sections>
        </column>
      </columns>
    </tab>
  </tabs>
  <header id="{guid}"><!-- Similar row/cell structure --></header>
  <footer id="{guid}"><!-- Similar row/cell structure --></footer>
  <Navigation>
    <NavBar>
      <NavBarByRelationshipItem RelationshipName="relationshipname" />
    </NavBar>
  </Navigation>
  <formLibraries>
    <Library name="libraryname" libraryUniqueId="{guid}" />
  </formLibraries>
  <events>
    <event name="onload" application="false" active="true">
      <Handlers>
        <Handler functionName="functionName" libraryName="libraryname" 
                 handlerUniqueId="{guid}" enabled="true" 
                 passExecutionContext="true" />
      </Handlers>
    </event>
  </events>
</form>
```

**Control type ClassId GUIDs**: Text={4273EDBD-AC1D-40d3-9FB2-095C621B552D}, Lookup={270BD3DB-D9AF-4782-9025-509E298DEC0A}, OptionSet={3EF39988-22BB-4f0b-BBBE-64B5A3748AEE}, DateTime={5B773807-9FB2-42db-97C3-7A91EFF8ADFF}, Subgrid={E7A81278-8635-4d9e-8D4D-59480B391C5B}, Web Resource={9FDF5F91-88B1-47f4-AD53-C11EFC01A01D}, IFRAME={1FB28AB1-0E87-4A67-9F63-EB60DA9A0D0D}.

**Key attributes**: Tabs support max 100, sections support 1-4 columns, cells support rowspan/colspan for layout control.

### SavedQuery XML Structure (Views)

SavedQuery records contain two key XML properties:

**FetchXML (query definition)**:
```xml
<fetch version='1.0' output-format='xml-platform' mapping='logical' distinct='false'>
  <entity name='account'>
    <attribute name='name' />
    <attribute name='accountid' />
    <order attribute='name' descending='false' />
    <filter type='and'>
      <condition attribute='statecode' operator='eq' value='0' />
    </filter>
    <link-entity name='contact' from='parentcustomerid' to='accountid' link-type='outer'>
      <attribute name='fullname' />
    </link-entity>
  </entity>
</fetch>
```

**LayoutXML (column display)**:
```xml
<grid name='resultset' object='1' jump='name' select='1' preview='1' icon='1'>
  <row name='result' id='accountid'>
    <cell name='name' width='150' />
    <cell name='primarycontactid' width='150' />
    <cell name='telephone1' width='100' />
  </row>
</grid>
```

**SavedQuery key attributes**: querytype (0=Public, 1=Advanced Find, 2=Associated, 4=Quick Find, 64=Lookup), returnedtypecode (entity logical name), isdefault (boolean, only one per entity can be true), fetchxml (query definition), layoutxml (column layout), columnsetxml (column formatting).

Complete FetchXML documentation: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/use-fetchxml-construct-query

### SiteMap XML Structure

**Official documentation**: https://learn.microsoft.com/en-us/dynamics365/customerengagement/on-premises/developer/customize-dev/sitemap-schema

**Complete structure**:
```xml
<SiteMap>
  <Area Id="SFA" ResourceId="Area_Sales" Icon="/_imgs/area/sales_24x24.gif">
    <Titles>
      <Title LCID="1033" Title="Sales" />
    </Titles>
    <Group Id="SalesGroup" ResourceId="Group_Sales">
      <Titles>
        <Title LCID="1033" Title="Sales Records" />
      </Titles>
      <SubArea Id="nav_accounts" Entity="account" 
               Icon="/_imgs/area/accounts_24x24.gif">
        <Titles>
          <Title LCID="1033" Title="Accounts" />
        </Titles>
        <Privilege Entity="account" Privilege="Read" />
      </SubArea>
      <SubArea Id="nav_custompage" Url="/custom/custompage.aspx">
        <Titles>
          <Title LCID="1033" Title="Custom Page" />
        </Titles>
      </SubArea>
    </Group>
  </Area>
</SiteMap>
```

**Key attributes**: Area (Id required, ResourceId for localization, Icon path, ShowGroups boolean), Group (Id required, ResourceId for localization), SubArea (Id required, Entity for entity subareas OR Url for custom pages, Icon 16x16 path, Client: Web|Outlook|All, AvailableOffline boolean, PassParams boolean).

**Privilege element** (within SubArea): `<Privilege Entity="entityname" Privilege="Read|Write|Create|Delete|Append|AppendTo" />`

### AppModule Definition

The AppModule table defines model-driven apps. **Key properties**: name (display name), uniquename (unique identifier), description, webresourceid (GUID of app icon), welcomepageid (GUID of welcome page), formfactor (1=Desktop, 2=Tablet, 4=Phone, 7=All), clienttype (1=Web, 2=Mobile), url (app URL slug), sitemapxml (associated sitemap XML).

**AppModuleComponent** adds components to apps via componenttype values: 1=Entity, 26=View, 29=Business Process Flow, 48=Command (Ribbon), 59=Chart, 60=Dashboard, 62=Form.

**Programmatic creation pattern**:
```csharp
Entity appModule = new Entity("appmodule");
appModule["name"] = "Custom Sales App";
appModule["uniquename"] = "custom_salesapp";
appModule["formfactor"] = 1; // Desktop
Guid appId = service.Create(appModule);

Entity component = new Entity("appmodulecomponent");
component["appmoduleid"] = new EntityReference("appmodule", appId);
component["objectid"] = accountEntityId;
component["componenttype"] = 1; // Entity
service.Create(component);
```

**Undocumented community finding**: One AppModule.xml file insufficient for both managed/unmanaged solutions. Need separate AppModule definitions.

## Programmatic Creation APIs

### Dataverse Web API for Entities, Attributes, and Relationships

**Core documentation**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/use-web-api-metadata

**API endpoint**: `POST https://[org].api.crm.dynamics.com/api/data/v9.2/EntityDefinitions`

**Key headers**: MSCRM.SolutionUniqueName (to add to specific solution), Content-Type: application/json, OData-MaxVersion: 4.0

**Create entity example**:
```http
POST [Organization URI]/api/data/v9.2/EntityDefinitions
MSCRM.SolutionUniqueName: examplesolution
{
  "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata",
  "Attributes": [...],
  "Description": {...},
  "DisplayCollectionName": {...},
  "DisplayName": {...},
  "HasActivities": false,
  "HasNotes": false,
  "IsActivity": false,
  "OwnershipType": "UserOwned",
  "SchemaName": "new_BankAccount"
}
```

**Create attribute documentation**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-update-column-definitions-using-web-api

**Supported attribute types**: String, Money, DateTime, Boolean, Decimal, Integer, Memo, Picklist, MultiSelectPicklist, Lookup, BigInt

**Create relationship documentation**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-update-entity-relationships-using-web-api

### Power Platform CLI Commands

**Installation**: `dotnet tool install --global Microsoft.PowerApps.CLI.Tool`

**Key pac solution commands**: `pac solution init` (initialize new solution), `pac solution clone` (clone from environment), `pac solution export` (export solution), `pac solution import` (import solution), `pac solution pack` (package solution), `pac solution unpack` (extract solution), `pac solution sync` (sync with environment), `pac solution check` (run Power Apps Checker), `pac solution version` (update version).

**Canvas app commands**: `pac canvas list` (list apps in environment), `pac canvas download` (download app as .msapp), `pac canvas unpack` (unpack to source files), `pac canvas pack` (repack from source), `pac canvas validate` (validate unpacked app).

**Known timeout issues documented by community**: Default timeout is 2 minutes. **Workaround**: Edit pac.exe.config file to increase timeout. Location for standalone: `%localappdata%\Microsoft\PowerAppsCLI\Microsoft.PowerApps.CLI.X.X.X\tools\pac.exe.config`. Location for VSCode: `%appdata%\code\User\globalStorage\microsoft-isvexptools.powerplatform-vscode\pac\tools\pac.exe.config`.

**Language issue workaround**: PAC CLI uses OS language by default. To force English, rename or delete localization folders in `\tools\loc\`.

### Power Apps SDK for .NET

**Documentation**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/org-service/overview

**Essential NuGet packages**: Microsoft.PowerPlatform.Dataverse.Client (recommended for .NET Framework/.NET Core), Microsoft.CrmSdk.CoreAssemblies (legacy .NET Framework), Microsoft.CrmSdk.Workflow (custom workflow activities).

**Key namespaces**: Microsoft.Xrm.Sdk (core types, IOrganizationService), Microsoft.Xrm.Sdk.Messages (CreateRequest, UpdateRequest, etc.), Microsoft.Crm.Sdk.Messages (Dataverse-specific messages), Microsoft.PowerPlatform.Dataverse.Client (ServiceClient implementation).

**Solution management example**:
```csharp
// Export solution
var exportRequest = new ExportSolutionRequest
{
    SolutionName = "MySolution",
    Managed = false
};
var response = (ExportSolutionResponse)service.Execute(exportRequest);

// Import solution
byte[] solutionBytes = File.ReadAllBytes("solution.zip");
var importRequest = new ImportSolutionRequest
{
    CustomizationFile = solutionBytes,
    PublishWorkflows = true
};
service.Execute(importRequest);
```

### PowerShell Modules for Power Apps

**Modules**: Microsoft.PowerApps.Administration.PowerShell, Microsoft.PowerApps.PowerShell

**Installation**:
```powershell
Install-Module -Name Microsoft.PowerApps.Administration.PowerShell
Install-Module -Name Microsoft.PowerApps.PowerShell -AllowClobber
Add-PowerAppsAccount
```

**Key cmdlets**: Environment management (New-AdminPowerAppEnvironment, Get-AdminPowerAppEnvironment, Remove-AdminPowerAppEnvironment), Apps (Get-AdminPowerApp, Remove-AdminPowerApp, Set-AdminPowerAppOwner), Flows (Get-AdminFlow, Enable-AdminFlow, Disable-AdminFlow), Database (New-AdminPowerAppCdsDatabase).

### Azure DevOps Build Tools

**Marketplace**: https://marketplace.visualstudio.com/items?itemName=microsoft-IsvExpTools.PowerPlatform-BuildTools

**Key build tool tasks**: PowerPlatformToolInstaller@2 (required first), PowerPlatformExportSolution@2, PowerPlatformImportSolution@2, PowerPlatformPackSolution@2, PowerPlatformUnpackSolution@2, PowerPlatformChecker@2 (static analysis), PowerPlatformPublishCustomizations@2, PowerPlatformSetSolutionVersion@2.

**Environment tasks**: PowerPlatformCreateEnvironment@2, PowerPlatformDeleteEnvironment@2, PowerPlatformBackupEnvironment@2, PowerPlatformCopyEnvironment@2.

**ALM best practices**: Use solution-aware components only, store unpacked solutions in source control, implement CI/CD pipelines, use connection references and environment variables, automated testing with solution checker, approval gates for production, modular solution design.

## Teams Integration Requirements

### Teams App Manifest.json for Power Apps

**Current schema version**: 1.24 (October 2025). Stable version for Power Apps: 1.17+ recommended.

**Schema URL**: https://developer.microsoft.com/json-schemas/teams/v1.17/MicrosoftTeams.schema.json

**Full reference**: https://learn.microsoft.com/en-us/microsoftteams/platform/resources/schema/manifest-schema

**Required manifest for Canvas Apps in Teams**:
```json
{
  "$schema": "https://developer.microsoft.com/en-us/json-schemas/teams/v1.17/MicrosoftTeams.schema.json",
  "manifestVersion": "1.17",
  "version": "1.0.0",
  "id": "<unique-guid>",
  "packageName": "com.company.appname",
  "developer": {
    "name": "Developer Name",
    "websiteUrl": "https://www.company.com",
    "privacyUrl": "https://www.company.com/privacy",
    "termsOfUseUrl": "https://www.company.com/terms"
  },
  "name": {
    "short": "App Name",
    "full": "Full Application Name"
  },
  "description": {
    "short": "Short description (80 chars max)",
    "full": "Full description"
  },
  "icons": {
    "color": "color.png",
    "outline": "outline.png"
  },
  "accentColor": "#FFFFFF",
  "staticTabs": [
    {
      "entityId": "uniqueId",
      "name": "My App",
      "contentUrl": "https://web.powerapps.com/webplayer/iframeapp?source=teamstab&appId={appId}",
      "scopes": ["personal"]
    }
  ],
  "validDomains": [
    "apps.powerapps.com",
    "web.powerapps.com",
    "*.login.microsoftonline.com",
    "microsoft.sharepoint.com"
  ],
  "webApplicationInfo": {
    "id": "475226c6-020e-4fb2-8a90-7a972cbfc1d4",
    "resource": "https://service.powerapps.com/"
  }
}
```

**Icon requirements**: Color icon 192x192 pixels PNG, outline icon 32x32 pixels PNG with white outline on transparent background, 32x32 color icon (v1.21+) with transparent background for Outlook/Microsoft 365.

### Dataverse for Teams Environment Differences

**Critical differences from standard Dataverse**:

| Feature | Dataverse for Teams | Standard Dataverse |
|---------|-------------------|-------------------|
| Creation | Automatic when first app created | Manual admin provisioning |
| Capacity | 2 GB per team (~1M rows) | Unlimited with licensing |
| Lifecycle | Tied to Teams team | Independent |
| API Access | **No direct API access** | Full API access |
| Model-driven apps | Not supported | Supported |
| Plug-ins/PCF | Not supported | Supported |
| Security roles | 3 predefined only | Fully customizable |
| Field-level security | Not supported | Supported |
| Advanced data types | Not supported | Supported |

**Table feature differences**: Basic data types supported in both. Advanced data types (customer, multiple currencies) only in standard. Relational storage in both. Advanced Dataverse search only in standard. Mobile offline only in standard.

**Integration capabilities in Teams**: Power Automate with standard connectors supported, Dataverse connector access supported, premium connectors with Premium licenses. NOT supported: Azure Synapse Link, Data Export Service, webhooks, Event Hubs/Service Bus, TDS protocol/SQL Server Management Studio.

**Upgrade path**: When you need more than 2 GB storage, require API access, need advanced security features, want plug-ins or PCF, need model-driven apps, or require Azure service integration. Upgrade requires tenant capacity, makes environment independent from Teams lifecycle, requires Power Platform licenses post-upgrade, and cannot be reversed.

### Teams Deployment Process

**Administrative deployment (recommended approach)**:

**Step 1**: Export app package from Power Apps. Navigate to make.powerapps.com, select app → "..." menu → "Add to Teams" → Choose "Download app" (NOT "Add to Teams"). Receives .zip file containing manifest.json, color.png (192x192), outline.png (32x32).

**Step 2**: Customize manifest (optional but recommended). Edit manifest.json for better descriptions, replace default icons with branded images, update app metadata. Use Developer Portal for Teams (https://dev.teams.microsoft.com) for validation.

**Step 3**: Upload to Teams Admin Center. Requires Microsoft Teams Administrator role. Navigate to Teams Admin Center → "Teams Apps" → "Manage Apps" → "Upload New App" → Upload customized .zip file. App becomes available in "Built for your org" catalog.

**Step 4**: Assign to users (optional). Use Teams app setup policies to auto-install app in user's app bars, assign policy to Azure AD groups, pin app to specific positions, control app visibility.

**Solution-based deployment for Dataverse for Teams**: Power Apps app in Teams → Build tab → Select environment → "See all" → Select items to export → "Export" → Choose "Export all dependencies" (recommended) → Export as .zip solution file. Import: Target team → Build tab → "See all" → "Import" → Browse and select .zip → Review items and dependencies → Configure connection references → "Import".

**Critical note**: Solutions from Dataverse for Teams are unmanaged. Solutions with standard Dataverse tables won't import to Teams. All dependencies must be included or present in target.

### Teams vs Standard Environment Solution Packaging

**Dataverse for Teams solutions contain**: Canvas apps (XML definition), custom tables (schema only, no standard tables), flows (cloud flows), connection references, environment variables, custom connectors (limited).

**Standard Dataverse solutions can additionally contain**: Model-driven apps, business process flows, custom security roles, plug-ins and custom workflow activities, web resources, site maps, dashboards and charts, standard table customizations, PCF components.

**Migration considerations**: Teams → Teams (direct solution export/import, no conversion needed). Standard → Teams (remove model-driven apps, remove standard table dependencies, remove complex security roles, remove plug-ins/custom workflows). Teams → Standard upgrade (environment upgrade required, post-upgrade adds capabilities, retains existing components, can add advanced features after, licensing changes apply).

## Undocumented Requirements and Community Knowledge

### Critical Undocumented Discoveries

**Connection Reference component codes vary by installation**: Documentation states code 10039, but they actually start at 10000+ and increment sequentially based on installation order. Codes differ between environments. Query with `objecttypecode eq componentCode` to determine actual values.

**Solution layers override managed solutions**: If you have Solution 1 (managed) with Flow v1 and Solution 2 (managed) with Flow v2, Flow v2 changes appear as solution layer in Solution 1. This creates ALM nightmares where updates may not apply as expected. Community documents this extensively but Microsoft provides limited guidance.

**Component sharing must happen at Dataverse table level**: You cannot share solution components through the solution UI. Must go to Advanced Settings, find component in Dataverse table, share from table record (not from solution).

**Both managed and unmanaged AppModule definitions needed**: Single AppModule.xml file insufficient for both managed/unmanaged solutions according to community findings.

### Community Tools for Learning Solution Format

**XrmToolBox** (https://www.xrmtoolbox.com) provides 200+ plugins for solution work:

**Solution Manager** (_n.SolutionManager): View solution import progress, parse import output logs XML in tree view (54,276 downloads).

**Dependency Identifier** (Power-Maverick): Identifies all solution dependencies, critical for avoiding import errors (https://github.com/Power-Maverick/DependencyIdentifier).

**Albanian Solution Packager**: Alternative to Microsoft SolutionPackager (31,772 downloads, https://github.com/albanian-xrm/solution-packager).

**FetchXML Builder** (Jonas Rapp): Essential for understanding Dataverse queries (1,001,030+ downloads, https://fetchxmlbuilder.com/).

**Metadata Browser**: Browse all Dataverse metadata, understand component types and relationships (316,453 downloads).

**Capgemini Power Apps Project Template** (https://github.com/Capgemini/powerapps-project-template): Yeoman-based generator scaffolding Power Platform projects with best practices. Generates solution metadata source code, scaffolds Azure DevOps pipelines, handles SolutionPackager with MappingFile.xml configuration, includes spkl task runner configuration, supports TypeScript web resources with automatic compilation.

### Common Errors with Community-Documented Solutions

**Error: "Cannot find required file 'Customizations.xml'"**: File paths incorrect or files not on build server. Ensure all files copied to build server before packing.

**Error: "An item with the same key has already been added"**: Duplicate IDs in solution XML files (often in forms with repeated fields). Check solution.xml for duplicate component IDs, look for duplicate field IDs in form definitions, remove repeated form fields (header vs. body).

**Error: "Following root components are not defined in customizations"**: Component in folder structure but not defined in solution.xml or vice versa. Ensure consistency between files in extracted folder, component definitions in solution.xml, and OtherComponents.xml entries.

**Error: "Missing Dependencies"**: Global Choice not included in solution, components not shared with importing user, or referenced components in different managed solution. Use "Add Required Components" carefully (beware of over-inclusion), manually add Choice columns via "Add Subcomponents", share components with deployment service account.

**Error: "ConnectionAuthorizationFailed"**: Connections not shared with service account running import. Share all connections in target environment with pipeline/CLI service account BEFORE import.

**SolutionPackager timeout**: Default timeout 2 minutes. Edit pac.exe.config file to increase timeout (documented by community MVP Diana Birkelbach).

### Solution Settings File (ImportConfig.xml) - Undocumented Feature

Can pre-populate connection references and environment variables, preventing "select connection" prompt during import. Format documented by community:

```xml
<ImportConfig>
  <Solutions>
    <Solution>
      <ConnectionReferences>
        <ConnectionReference>
          <ConnectionReferenceLogicalName>...</ConnectionReferenceLogicalName>
          <ConnectionId>...</ConnectionId>
        </ConnectionReference>
      </ConnectionReferences>
      <EnvironmentVariables>
        <EnvironmentVariable>
          <SchemaName>...</SchemaName>
          <Value>...</Value>
        </EnvironmentVariable>
      </EnvironmentVariables>
    </Solution>
  </Solutions>
</ImportConfig>
```

## Critical Gaps and Validation Issues

**XSD schema validation gap**: Even Microsoft's out-of-the-box forms don't validate against published XSD schemas. In clean sandbox: 22 of 258 forms invalid (9%). With Sales/Customer Service: 307 of 1,462 forms invalid (21%). Some attributes used in production (like `headerdensity`) not declared in official XSD.

**Recommendation from community**: Trust documentation but always test with real exports. The XSD provides guidance but may not be 100% complete. The exact count of metadata elements depends on how you count nested structures—the XSD shows 30+ top-level elements plus nested structures, explaining your discovery of 38 vs. 19 documented.

**DisplayMask complete values**: Not comprehensively documented. Schema shows free-form string. Best learned by exporting existing solutions with similar field types.

**Component type codes**: No complete list in official docs. Community maintains reverse-engineered lists showing codes like 1=Entity, 2=Attribute, 9=OptionSet, 26=View, 29=Process (Flows), 60=Dashboard, 62=Form, 300=Canvas Apps, 380=Environment Variable Definition, 381=Environment Variable Value.

## Best Practices for Hand-Writing Solution Files

**Always validate with XSD** in Visual Studio or similar tool with schema validation. **Export similar components first** to see exact XML structure—this is the most reliable way to discover undocumented requirements. **Use SolutionPackager** or pac CLI to decompose existing solutions for reference. **Test in dev environment** before production. **Keep IntroducedVersion consistent** with your solution version. **Follow naming conventions** using CustomizationPrefix consistently. **Respect minOccurs/maxOccurs** in schema definitions.

**For Canvas apps**: Always use `pac canvas unpack/pack`, never manual zip operations. Structure changed approximately 2 years ago, making old tutorials obsolete. Include entropy.json in .gitignore for cleaner version control.

**For merging**: Always merge /src/*.pa.yaml files (actual source code). Take latest version for checksum.json and entropy.json. Not safe to merge Connections/*, DataSources/*, or CanvasManifest.json files—these are environment-specific.

## Complete Reference Links

**Official Schemas**: https://download.microsoft.com/download/B/9/7/B97655A4-4E46-4E51-BA0A-C669106D563F/Schemas.zip

**Solution XML Schema Documentation**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/customization-solutions-file-schema

**Canvas App YAML Schema**: https://github.com/microsoft/PowerApps-Tooling/blob/master/schemas/pa-yaml/v3.0/pa.schema.yaml

**Form XML Schema**: https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/form-xml-schema

**FetchXML Reference**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/use-fetchxml-construct-query

**SiteMap Schema**: https://learn.microsoft.com/en-us/dynamics365/customerengagement/on-premises/developer/customize-dev/sitemap-schema

**Dataverse Web API Metadata**: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/use-web-api-metadata

**Power Platform CLI Reference**: https://learn.microsoft.com/en-us/power-platform/developer/cli/introduction

**Teams Manifest Schema**: https://learn.microsoft.com/en-us/microsoftteams/platform/resources/schema/manifest-schema

**XrmToolBox**: https://www.xrmtoolbox.com

**Capgemini Template**: https://github.com/Capgemini/powerapps-project-template

**Community Knowledge** (Dave Wyatt's comprehensive guide): https://dev.to/wyattdave/everything-you-didnt-know-you-needed-to-know-about-power-platform-solutions-1b4

This documentation combines official Microsoft resources with community-discovered tribal knowledge to provide the complete specification needed for programmatic Power Apps generation without trial-and-error discovery. The key insight: Microsoft's published schemas lag behind their implementations, making community reverse-engineering and exported solution analysis essential for success.