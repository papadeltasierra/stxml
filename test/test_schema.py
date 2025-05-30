"""Test suite for the STGPX schema."""

import os
import pytest
import xml.etree.ElementTree as ET
import xmlschema

# Combine schema files to test extensions.
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "combined.xsd")

successful_cases = [
    (
        "minimal",
        '<?xml version="1.0"?>'
        + '<activity xmlns="https://www.w3schools.com" '
        + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        + 'xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd">'
        + "</activity>",
    ),
    (
        "minimal with whitespace",
        """<?xml version="1.0"?>

<activity xmlns="https://www.w3schools.com"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd">
</activity>""",
    ),
    (
        "maximal",
        '<?xml version="1.0"?>'
        + '<activity xmlns="https://www.w3schools.com" '
        + 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        + 'xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd ./extension.xsd">'
        + "<gpx>boris.gpx</gpx>"
        + "<started>2023-10-01T12:00:00Z</started>"
        + "<type>Running</type>"
        + "<extension>"
        + "<someExtension>Some value</someExtension>"
        + "</extension>"
        + "</activity>",
    ),
    (
        "maximal with whitespace",
        """<?xml version="1.0"?>
        <activity xmlns="https://www.w3schools.com"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd ./extension.xsd">
            <gpx>boris.gpx</gpx>
            <started>2023-10-01T12:00:00Z</started>
            <type>Running</type>
            <extension>
                <someExtension>Some value</someExtension>
            </extension>
        </activity>""",
    ),
]

failure_cases = [
    (
        "Unknown with whitespace",
        """<?xml version="1.0"?>

<activity xmlns="https://www.w3schools.com"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd">

        <gpx>boris.gpx</gpx>
        <started>2023-10-01T12:00:00Z</started>
        <type>Running</type>
        <unknown>What is this?</unknown>
</activity>
""",
        "Unexpected child with tag '{https://www.w3schools.com}unknown'",
    ),
    (
        "Unknown extension",
        """<?xml version="1.0"?>

<activity xmlns="https://www.w3schools.com"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd">

        <gpx>boris.gpx</gpx>
        <started>2023-10-01T12:00:00Z</started>
        <type>Running</type>
        <extension>
            <noIdea>hat is this?</noIdea>
        </extension>
</activity>
""",
        "element '{https://www.w3schools.com}noIdea' not found",
    ),
    (
        "Duplicate GPX",
        """<?xml version="1.0"?>

<activity xmlns="https://www.w3schools.com"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd">

        <gpx>boris.gpx</gpx>
        <gpx>boris2.gpx</gpx>
        <started>2023-10-01T12:00:00Z</started>
        <type>Running</type>
</activity>
""",
        "Unexpected child with tag '{https://www.w3schools.com}gpx",
    ),
    (
        "Duplicate started",
        """<?xml version="1.0"?>

<activity xmlns="https://www.w3schools.com"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd">

        <gpx>boris.gpx</gpx>
        <started>2023-10-01T12:00:00Z</started>
        <started>2023-10-01T12:00:01Z</started>
        <type>Running</type>
</activity>
""",
        "Unexpected child with tag '{https://www.w3schools.com}started",
    ),
    (
        "Duplicate type",
        """<?xml version="1.0"?>

<activity xmlns="https://www.w3schools.com"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="https://www.w3schools.com ../../schema/stgpx-schema-1.0.xsd">

        <gpx>boris.gpx</gpx>
        <started>2023-10-01T12:00:00Z</started>
        <type>Walking</type>
        <type>Running</type>
</activity>
""",
        "Unexpected child with tag '{https://www.w3schools.com}type",
    ),
]


@pytest.fixture
def schema():
    return xmlschema.XMLSchema(SCHEMA_FILE)


@pytest.mark.parametrize("name,xml", successful_cases)
def test_valid_xml(schema, name, xml):
    # Parse the XML schema

    # Test parse the XML file.
    xmlData = ET.fromstring(xml)

    # Validate the XML file.
    schema.validate(xmlData)


@pytest.mark.parametrize("name,xml,cause", failure_cases)
def test_invalid_xml(schema, name, xml, cause):
    # Parse the XML schema
    try:
        # Test parse the XML file.
        xmlData = ET.fromstring(xml)

        # Validate the XML file.
        schema.validate(xmlData)

    except xmlschema.validators.exceptions.XMLSchemaValidationError as ee:
        assert (
            cause in ee.reason
        ), f"Expected '{cause}' in error message, got {ee.reason}"
