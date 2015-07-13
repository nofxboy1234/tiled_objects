from xml.etree.ElementTree import Element, SubElement, parse, ElementTree, XMLParser
from xml.etree.ElementTree import tostring, fromstring
from xml.dom import minidom

class Tiled_ObjectGroup(object):
    def __init__(self, group_name):
        self.group_name = group_name
        self.sprite = "spr_%s" % (group_name)

class Tiled_Object(Tiled_ObjectGroup):
    def __init__(self, group_name, tiled_id, x, y, width, height,
                        object_name="", tiled_type="",
                        sprite=""):
        super(Tiled_Object, self).__init__(group_name)

        self.id = tiled_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.object_name = object_name
        self.type = tiled_type

        if sprite != "":
            self.sprite = sprite

def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_GMS_sprite(name, width, height, output_dir, sprite):
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
    elem.text = "%s" % (int(width) - 1)

    elem = SubElement(root, "bbox_top")
    elem.text = "0"

    elem = SubElement(root, "bbox_bottom")
    elem.text = "%s" % (int(height) - 1)

    elem = SubElement(root, "HTile")
    elem.text = "0"

    elem = SubElement(root, "VTile")
    elem.text = "0"

    elem = SubElement(root, "TextureGroups")
    texture_group = SubElement(elem, "TextureGroup0")
    texture_group.text = "0"

    elem = SubElement(root, "For3D")
    elem.text = "0"

    elem = SubElement(root, "width")
    elem.text = "%s" % (width)

    elem = SubElement(root, "height")
    elem.text = "%s" % (height)

    elem = SubElement(root, "frames")
    frame = SubElement(elem, "frame", index="0")
    frame.text = "images\%s_0.png" % (sprite)

    # Prettify and convert back to XML
    root = fromstring(prettify(root))

    write_file = open("%s/spr_%s.sprite.gmx" % (output_dir, name), "w")
    ElementTree(root).write(write_file, encoding="utf-8", xml_declaration=True)
    write_file.close()

def get_tiled_objects(filename):

    tree = ElementTree(file=filename)
    elem = tree.getroot()

    tiled_objectgroups = elem.findall('objectgroup')
    groups = {}
    for tiled_objectgroup in tiled_objectgroups:
        # Check if there's a sprite set for the objectgroup
        properties = tiled_objectgroup.find('properties')
        objectgroup_sprite = ''
        # Check tiled custom properties
        if properties is not None:
            for prop in properties:
                name = prop.get('name')
                if name == 'sprite':
                    value = prop.get('value')
                    objectgroup_sprite = value

        tiled_object_list = tiled_objectgroup.findall('object')
        objects = []
        for tiled_object in tiled_object_list:
            tiled_object_dict = {}

            tiled_object_dict['name'] = tiled_objectgroup.get('name')
            tiled_object_dict['type'] = tiled_objectgroup.get('name')

            tiled_object_dict['id'] = tiled_object.get('id')
            tiled_object_dict['x'] = tiled_object.get('x')
            tiled_object_dict['y'] = tiled_object.get('y')
            tiled_object_dict['width'] = tiled_object.get('width')
            tiled_object_dict['height'] = tiled_object.get('height')

            # Check if there's a sprite set for the object
            # This will override any objectgroup sprite set
            properties = tiled_object.find('properties')
            object_sprite = ''
            # Check tiled custom properties
            if properties is not None:
                for prop in properties:
                    name = prop.get('name')
                    if name == 'sprite':
                        value = prop.get('value')
                        object_sprite = value

            # If there's an object_sprite, use this instead of objectgroup_sprite
            if object_sprite != '':
                tiled_object_dict['sprite'] = object_sprite
            else:
                tiled_object_dict['sprite'] = objectgroup_sprite

            objects.append(tiled_object_dict)
        # Add a group to the groups dict
        # groups = {group_name: [{'name': '',},]}
        groups[tiled_objectgroup.get('name')] = objects

    return groups

def create_GMS_object(name, output_dir):
    root = Element("object")

    elem = SubElement(root, "spriteName")
    elem.text = "spr_%s" % (name)

    elem = SubElement(root, "solid")
    elem.text = "0"

    elem = SubElement(root, "visible")
    elem.text = "-1"

    elem = SubElement(root, "depth")
    elem.text = "0"

    elem = SubElement(root, "persistent")
    elem.text = "0"

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


    # Prettify and convert back to XML
    root = fromstring(prettify(root))

    # re-set text for special char texts
    parentName = root.find("parentName")
    parentName.text = "#undefined#"

    maskName = root.find("maskName")
    maskName.text = "#undefined#"

    appendfile = open("%s/obj_%s.object.gmx" % (output_dir, name), "w")
    ElementTree(root).write(appendfile, encoding="utf-8", xml_declaration=True)
    appendfile.close()

    editfile = open("%s/obj_%s.object.gmx" % (output_dir, name), "r")
    data = editfile.readlines()
    editfile.close()

    parentName_index = data.index("  <parentName>#undefined#</parentName>\n")
    parentName_value = data[parentName_index]
    data[parentName_index] = parentName_value.replace("#undefined#", "&lt;undefined&gt;")

    maskName_index = data.index("  <maskName>#undefined#</maskName>\n")
    maskName_value = data[maskName_index]
    data[maskName_index] = maskName_value.replace("#undefined#", "&lt;undefined&gt;")

    editfile = open("%s/obj_%s.object.gmx" % (output_dir, name), "w")
    editfile.writelines(data)
    editfile.close()

def get_tile_size(tmx_filename):
    tree = ElementTree(file=tmx_filename)
    root = tree.getroot()

    tilewidth = root.get('tilewidth')
    tileheight = root.get('tileheight')

    return tilewidth, tileheight

def clear_instances_from_room(room_filename):
    """ Remove the instances element """

    tree = ElementTree(file=room_filename)
    root = tree.getroot()

    instances_element = root.find('instances')
    if instances_element is not None:
        root.remove(instances_element)

    ElementTree(root).write(room_filename, encoding="utf-8", xml_declaration=True)

def add_instance_to_room(tiled_object, room_filename, tmx_filename):
    """ Add tiled objects to an existing room created by GMSTiled """

    # tree = ElementTree(file=tmx_filename)
    # root = tree.getroot()

    # tilewidth = root.get('tilewidth')
    # tileheight = root.get('tileheight')
    # # print("root.tag: %s" % root.tag)
    # # print("tilewidth: %s tileheight: %s" % (tilewidth, tileheight))

    tree = ElementTree(file=room_filename)
    root = tree.getroot()

    # # print("root.tag: %s" %(root.tag))
    # instances_element = root.find('instances')
    # if instances_element is not None:
    #     root.remove(instances_element)

    tilewidth, tileheight = get_tile_size(tmx_filename)

    existing_instances_element = root.find('instances')
    if existing_instances_element is None:
        print("1")
        instances = Element("instances")
    else:
        print("2")
        instances = existing_instances_element

    room_name = room_filename.split('/')[-1].split(".")[0]

    elem = Element("instance",
                        objName = "obj_%s" % (tiled_object['name']),
                        x = tiled_object['x'],
                        y = tiled_object['y'],
                        name = "inst_%s_%04d" % (room_name, int(tiled_object['id'])),
                        locked = "0",
                        code = "",
                        scaleX = str(int(tiled_object['width'])/int(tilewidth)),
                        scaleY = str(int(tiled_object['height'])/int(tileheight)),
                        colour = "4294967295",
                        rotation = "0")
    instances.append(elem)

    instances = fromstring(prettify(instances))

    if existing_instances_element is None:
        root.append(instances)

    appendfile = room_filename
    ElementTree(root).write(appendfile, encoding="utf-8", xml_declaration=True)

def main():
    object_groups = get_tiled_objects("C:/Users/dylan/tiled_maps/crate_land.tmx")

    clear_instances_from_room("C:/Users/dylan/tiled_maps/crate_land/crate_land.room.gmx")

    # object_groups = {group_name: [{'name': '',},]}
    for group in object_groups:
        for tiled_object in object_groups[group]:
            print(str(tiled_object))
            create_GMS_sprite(tiled_object['name'],
                                tiled_object['width'],
                                tiled_object['height'],
                                "C:/Users/dylan/tiled_maps",
                                tiled_object['sprite'])

            create_GMS_object(tiled_object['name'],
                                "C:/Users/dylan/tiled_maps")

            add_instance_to_room(tiled_object,
                                "C:/Users/dylan/tiled_maps/crate_land/crate_land.room.gmx",
                                "C:/Users/dylan/tiled_maps/crate_land.tmx")

# main()
