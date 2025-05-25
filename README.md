# XML schema File to support STGPX.

### Usage
Your XML file should reference the schema as follows:

```xml
<?xml version="1.0"?>
<activity xmlns="https://www.w3schools.com"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
          xsi:schemaLocation="https://www.w3schools.com https://raw.githubusercontent.com/papadeltasierra/stxml/refs/heads/main/schema/stgpx-schema-1.0.xsd">

...

</activity>
```
You can also use the `extension` field by creating your own schema file looking something like this...

```xsd
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
targetNamespace="https://www.w3schools.com"
xmlns="https://www.w3schools.com"
elementFormDefault="qualified">

<xs:element name="someExtension" type="xs:string"/>

</xs:schema>
```
...and then adding this to the schema references...
```xml
<?xml version="1.0"?>
<activity xmlns="https://www.w3schools.com"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
          xsi:schemaLocation="https://www.w3schools.com https://raw.githubusercontent.com/papadeltasierra/stxml/refs/heads/main/schema/stgpx-schema-1.0.xsd mySchema.xsd">

...

</activity>
```
# Sample XML with extensions
```xml
<?xml version="1.0"?>

<activity xmlns="https://www.w3schools.com"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd mySchema.xsd">
    <gpx>02_10_2026 08_00.gpx</gpx>
    <started>2023-10-01T08:00:00Z</started>
    <type>Running</type>
    <extension>
        <holiday>Naples 2023</holiday>
    </extension>
</activity>"
```

## Schema Design
1. Avoid data duplication
   1. Nothing that exists in the GPX file should be duplicated in the XML file
   1. Nothing that can be **calculated** from data in the GPX file should be in the XML file
1. Store additional data provided by [Sports Tracker] but not in the GPX file
1. Store additional informaion that the user might find useful
   1. For example the _name_ of the route could be calculated and added to the XML file
1. Extensions are permitted in the `extension` element
   1. Keep extensions simple!

[Sports Tracker]: https://www.sports-tracker.com