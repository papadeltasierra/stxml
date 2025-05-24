import sys
import xml.etree.ElementTree as ET
import xmlschema

# Parse the XML schema
stgpx_schema = xmlschema.XMLSchema(sys.argv[1])

# Test parse the XML file.
ET.parse(sys.argv[2])

# Validate the XML file.
try:
    stgpx_schema.validate(sys.argv[2])
    print("The XML document is valid.")
    sys.exit(0)

except xmlschema.validators.exceptions.XMLSchemaValidationError as ee:
    print("The XML document is invalid:\n%s" % ee)
    sys.exit(1)
