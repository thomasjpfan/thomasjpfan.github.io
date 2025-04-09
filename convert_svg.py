from string import Template
from argparse import ArgumentParser
from xml.etree import ElementTree as ET

parser = ArgumentParser()
parser.add_argument("name")
parser.add_argument("svg")

args = parser.parse_args()

root = ET.fromstring(args.svg)

d = root[0].attrib["d"]
viewbox = root.attrib["viewBox"]

template = Template('''
.tf-$NAME {
    mask-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='$VIEWBOX' %3e%3cpath d='$D'/%3e%3c/svg%3e");
    -webkit-mask-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='$VIEWBOX' %3e%3cpath d='$D'/%3e%3c/svg%3e");
}
''')

output = template.substitute(NAME=args.name, VIEWBOX=viewbox, D=d)
print(output)
