from xml.etree.ElementTree import Element, SubElement, parse, ElementTree, XMLParser
from xml.etree.ElementTree import tostring, fromstring
from xml.dom import minidom

# root = Element("root")
# print root.tag

# elem = SubElement(root, "one", first="1", second="2")
# print elem.get("first")
# print elem.keys()
# print elem.items()

# print elem.get("third", "default")
# elem.set("third", 3)
# print elem.get("third", "default")

# SubElement(root, "two")

# SubElement(root, "three")

# for node in root:
# 	print node

# parentmap = dict((c, p) for p in root.getiterator() for c in p)
# print parentmap

def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_GMS_sprite():
    root = Element("sprite")

    elem = SubElement(root, "type")
    elem.text = "0"

    elem = SubElement(root, "xorig")
    elem.text = "0"

    elem = SubElement(root, "yorigin")
    elem.text = "0"

    elem = SubElement(root, "colkind")
    elem.text = "1"

    elem = SubElement(root, "coltolerance")
    elem.text = "0"

    elem = SubElement(root, "sepmasks")
    elem.text = "0"

    elem = SubElement(root, "bboxmode")
    elem.text = "0"

    elem = SubElement(root, "bbox_left")
    elem.text = "0"

    elem = SubElement(root, "bbox_right")
    elem.text = "31"

    elem = SubElement(root, "bbox_top")
    elem.text = "0"

    elem = SubElement(root, "bbox_bottom")
    elem.text = "31"

    elem = SubElement(root, "HTile")
    elem.text = "0"

    elem = SubElement(root, "VTile")
    elem.text = "0"

    elem = SubElement(root, "TextureGroups")
    # texture_group = SubElement(elem, "TextureGroup")
    # texture_group.text = 0
    texture_group = SubElement(elem, "TextureGroup0")
    texture_group.text = "0"

    elem = SubElement(root, "For3D")
    elem.text = "0"

    elem = SubElement(root, "width")
    elem.text = "32"

    elem = SubElement(root, "height")
    elem.text = "32"

    elem = SubElement(root, "frames")
    frame = SubElement(elem, "frame", index="0")
    frame.text = "images\sprite0_0.png"

    # write to file
    # filename = "C:/Users/dylan/tiled_maps/sprite0.sprite.gmx"
    # ElementTree(treetop).write(filename)

    # Convert back to XML
    root = fromstring(prettify(root))

    # append to file
    appendfile = open("C:/Users/dylan/tiled_maps/sprite0.sprite.gmx", "w")
    ElementTree(root).write(appendfile, encoding="utf-8", xml_declaration=True)
    appendfile.close()

def get_tiled_objects():
    filename = "C:/Users/dylan/tiled_maps/crate_land.tmx"
    # tree = parse(filename)
    tree = ElementTree(file=filename)
    elem = tree.getroot()

    tiled_objects = []
    tiled_objectgroup = elem.find('objectgroup')
    for tiled_object in tiled_objectgroup:
        tiled_object_dict = {}
        tiled_object_dict['id'] = tiled_object.get('id')
        tiled_object_dict['x'] = tiled_object.get('x')
        tiled_object_dict['y'] = tiled_object.get('y')
        tiled_object_dict['width'] = tiled_object.get('width')
        tiled_object_dict['height'] = tiled_object.get('height')

        tiled_objects.append(tiled_object_dict)

    return tiled_objects

def create_GMS_object():
    root = Element("object")

    elem = SubElement(root, "spriteName")
    elem.text = "sprite0"

    elem = SubElement(root, "solid")
    elem.text = "0"

    elem = SubElement(root, "visible")
    elem.text = "-1"

    elem = SubElement(root, "depth")
    elem.text = "0"

    elem = SubElement(root, "persistent")
    elem.text = "0"

    # elem = SubElement(root, "parentName")
    # elem.text = "&lt;undefined&gt;"

    # elem = SubElement(root, "maskName")
    # elem.text = "&lt;undefined&gt;"

    parentName = SubElement(root, "parentName")

    maskName = SubElement(root, "maskName")

    elem = SubElement(root, "events")

    elem = SubElement(root, "PhysicsObject")
    elem.text = "0"

    elem = SubElement(root, "PhysicsObjectSensor")
    elem.text = "0"

    elem = SubElement(root, "PhysicsObjectShape")
    elem.text = "0"

    elem = SubElement(root, "PhysicsObjectDensity")
    elem.text = "0.5"

    elem = SubElement(root, "PhysicsObjectRestitution")
    elem.text = "0.100000001490116"

    elem = SubElement(root, "PhysicsObjectGroup")
    elem.text = "0"

    elem = SubElement(root, "PhysicsObjectLinearDamping")
    elem.text = "0.100000001490116"

    elem = SubElement(root, "PhysicsObjectAngularDamping")
    elem.text = "0.100000001490116"

    elem = SubElement(root, "PhysicsObjectFriction")
    elem.text = "0.200000002980232"

    elem = SubElement(root, "PhysicsObjectAwake")
    elem.text = "-1"

    elem = SubElement(root, "PhysicsObjectKinematic")
    elem.text = "0"

    elem = SubElement(root, "PhysicsShapePoints")


    # Convert back to XML
    root = fromstring(prettify(root))

    # re-set text for special char texts
    parentName = root.find("parentName")
    parentName.text = "#undefined#"

    maskName = root.find("maskName")
    maskName.text = "#undefined#"

    # write to file
    appendfile = open("C:/Users/dylan/tiled_maps/object0.object.gmx", "w")
    ElementTree(root).write(appendfile, encoding="utf-8", xml_declaration=True)
    appendfile.close()

    editfile = open("C:/Users/dylan/tiled_maps/object0.object.gmx", "r")
    data = editfile.readlines()
    # print(data)
    editfile.close()

    parentName_index = data.index("  <parentName>#undefined#</parentName>\n")
    parentName_value = data[parentName_index]
    data[parentName_index] = parentName_value.replace("#undefined#", "&lt;undefined&gt;")

    maskName_index = data.index("  <maskName>#undefined#</maskName>\n")
    maskName_value = data[maskName_index]
    data[maskName_index] = maskName_value.replace("#undefined#", "&lt;undefined&gt;")

    editfile = open("C:/Users/dylan/tiled_maps/object0.object.gmx", "w")
    editfile.writelines(data)
    editfile.close()

def add_instances_to_room(tiled_objects):
    filename = "C:/Users/dylan/tiled_maps/crate_land/crate_land.room.gmx"
    # tree = parse(filename)
    tree = ElementTree(file=filename)
    root = tree.getroot()

    # all_items = root.getiterator()
    # print all_items
    # return

    # root_str = "".join(tostring(root).split())
    # print root_str
    # root = fromstring(root_str)

    instances = Element("instances")
    room_name = filename.split('/')[-1].split(".")[0]
    count = 0
    for tiled_object in tiled_objects:
        count += 1
        elem = Element("instance",
                            objName="object0",
                            x = tiled_object['x'],
                            y = tiled_object['y'],
                            name = "inst_%s_%04d" % (room_name, count),
                            locked = "0",
                            code = "",
                            scaleX = str(int(tiled_object['width'])/32),
                            scaleY = str(int(tiled_object['height'])/32),
                            colour = "4294967295",
                            rotation = "0")
        instances.append(elem)

    instances = fromstring(prettify(instances))
    root.append(instances)

    # root.append(instances)
    # root = fromstring(prettify(root))

    # write to file
    appendfile = "C:/Users/dylan/tiled_maps/crate_land/crate_land.room.gmx"
    ElementTree(root).write(appendfile, encoding="utf-8", xml_declaration=True)

def main():
    create_GMS_sprite()
    create_GMS_object()
    tiled_objects = get_tiled_objects()
    add_instances_to_room(tiled_objects)

main()
