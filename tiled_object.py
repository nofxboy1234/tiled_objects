# Design tile-based levels with Tiled and position objects in the level.

# Workflow: add gm objects to tiled, layout objects, run gmsTiled, add tiled objects to gms room

from PySide.QtGui import *

import shutil
import os.path

from xml.etree.ElementTree import Element, SubElement, parse, ElementTree, XMLParser
from xml.etree.ElementTree import tostring, fromstring
from xml.dom import minidom

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

event_types = enum('CREATE', 'DESTROY', 'ALARM', 'STEP', 'COLLISION',
                    'KEYBOARD', 'MOUSE', 'OTHER', 'DRAW', 'KEY_PRESS',
                    'KEY_RELEASE', 'ASYNCHRONOUS')

class Tiled_ObjectGroup(object):
    def __init__(self, group_name):
        self.group_name = group_name
        self.sprite = "spr_%s" % (group_name)

class Tiled_Object(Tiled_ObjectGroup):
    def __init__(self, group_name, tiled_id="", x="0", y="0",
                        width="32", height="32",
                        object_name="", tiled_type="",
                        sprite=""):
        super(Tiled_Object, self).__init__(group_name)

        self.name = object_name
        self.id = tiled_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = tiled_type

        if sprite != "":
            self.sprite = sprite

    def __str__(self):
        print_str = "group_name: %s\n" \
                    "name: %s\n" \
                    "id: %s\n" \
                    "x: %s\n" \
                    "y: %s\n" \
                    "width: %s\n" \
                    "height: %s\n" \
                    "type: %s\n" \
                    "sprite: %s\n" \
                    % (
                        self.group_name,
                        self.name,
                        self.id,
                        self.x,
                        self.y,
                        self.width,
                        self.height,
                        self.type,
                        self.sprite
                        )
        return print_str


def prettify(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_GMS_sprite(tiled_object, output_dir):
    name = tiled_object.name
    if name == "":
        name = tiled_object.group_name

    width = tiled_object.sprite_width
    height = tiled_object.sprite_height
    sprite = tiled_object.sprite

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
        objectgroup_sprite_width = ''
        objectgroup_sprite_height = ''

        # Check tiled custom properties
        if properties is not None:
            for prop in properties:
                name = prop.get('name')
                if name == 'sprite':
                    value = prop.get('value')
                    objectgroup_sprite = value
                elif name == 'sprite_width':
                    value = prop.get('value')
                    objectgroup_sprite_width = value
                elif name == 'sprite_height':
                    value = prop.get('value')
                    objectgroup_sprite_height = value

        tiled_object_list = tiled_objectgroup.findall('object')
        objects = []
        for tiled_object in tiled_object_list:
            tiled_object_dict = {}
            to = Tiled_Object(tiled_objectgroup.get('name'))

            # tiled_object_dict['id'] = tiled_object.get('id')
            to.id = tiled_object.get('id')

            # tiled_object_dict['x'] = tiled_object.get('x')
            to.x = tiled_object.get('x')

            # tiled_object_dict['y'] = tiled_object.get('y')
            to.y = tiled_object.get('y')

            # tiled_object_dict['width'] = tiled_object.get('width')
            to.width = tiled_object.get('width')

            # tiled_object_dict['height'] = tiled_object.get('height')
            to.height = tiled_object.get('height')

            # tiled_object_dict['name'] = tiled_objectgroup.get('name')
            # to.object_name = tiled_object.get('name')
            to.name = tiled_object.get('name')
            if to.name is None:
                to.name = ""

            # tiled_object_dict['type'] = tiled_objectgroup.get('name')
            # to.tiled_type = tiled_object.get('type')
            to.type = tiled_object.get('type')
            if to.type is None:
                to.type = ""

            # Check if there's a sprite set for the object
            # This will override any objectgroup sprite set
            properties = tiled_object.find('properties')

            object_sprite = ''
            object_sprite_width = ''
            object_sprite_height = ''

            # Check tiled custom properties
            if properties is not None:
                for prop in properties:
                    name = prop.get('name')
                    if name == 'sprite':
                        value = prop.get('value')
                        object_sprite = value
                    elif name == 'sprite_width':
                        value = prop.get('value')
                        object_sprite_width = value
                    elif name == 'sprite_height':
                        value = prop.get('value')
                        object_sprite_height = value

            # If there's an object_sprite, use this instead of objectgroup_sprite
            if object_sprite != '':
                # tiled_object_dict['sprite'] = object_sprite
                to.sprite = object_sprite
            else:
                # tiled_object_dict['sprite'] = objectgroup_sprite
                to.sprite = objectgroup_sprite

            if object_sprite_width != '':
                to.sprite_width = object_sprite_width
            else:
                to.sprite_width = objectgroup_sprite_width

            if object_sprite_height != '':
                to.sprite_height = object_sprite_height
            else:
                to.sprite_height = objectgroup_sprite_height

            # objects.append(tiled_object_dict)
            objects.append(to)

        # Add a group to the groups dict
        # groups = {group_name: [{'name': '',},]}
        groups[tiled_objectgroup.get('name')] = objects

    return groups

def create_GMS_object(tiled_object, output_dir):
    name = tiled_object.name
    if name == "":
        name = tiled_object.group_name

    root = Element("object")

    elem = SubElement(root, "spriteName")
    elem.text = "spr_%s" % (name)

    elem = SubElement(root, "solid")
    elem.text = "0"

    elem = SubElement(root, "visible")
    # elem.text = "-1"
    elem.text = "0"

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

def set_room_settings(room_filename):
    tree = ElementTree(file=room_filename)
    root = tree.getroot()
    # print("root.tag: %s" % root.tag)

    element = root.find('speed')
    element.text = "60"

    element = root.find('enableViews')
    element.text = "1"

    views_element = root.find('views')
    view_0 = views_element[0]
    view_0.set("visible", "1")
    view_0.set("wview", "1280")
    view_0.set("hview", "720")
    view_0.set("wport", "1280")
    view_0.set("hport", "720")
    view_0.set("objName", "obj_player")
    view_0.set("hborder", "%s" % (1280/2))
    view_0.set("vborder", "%s" % (720/2))
    view_0.set("hspeed", "20")

    # for e in root:
    #     print e

    write_file = open(room_filename, "w")
    ElementTree(root).write(write_file, encoding="utf-8", xml_declaration=True)
    write_file.close()

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

    # tilewidth, tileheight = get_tile_size(tmx_filename)

    existing_instances_element = root.find('instances')
    if existing_instances_element is None:
        # print("1")
        instances = Element("instances")
    else:
        # print("2")
        instances = existing_instances_element

    room_name = room_filename.split('/')[-1].split(".")[0]

    if tiled_object.name != "":
        object_room_name = tiled_object.name
    else:
        object_room_name = tiled_object.group_name

    elem = Element("instance",
                        objName = "%s" % (object_room_name),
                        x = tiled_object.x,
                        y = tiled_object.y,
                        name = "inst_%s_%04d" % (room_name, int(tiled_object.id)),
                        locked = "0",
                        code = "",
                        scaleX = str(int(tiled_object.width)/int(tiled_object.sprite_width)),
                        scaleY = str(int(tiled_object.height)/int(tiled_object.sprite_height)),
                        colour = "4294967295",
                        rotation = "0")
    instances.append(elem)

    instances = fromstring(prettify(instances))

    if existing_instances_element is None:
        root.append(instances)

    appendfile = room_filename
    ElementTree(root).write(appendfile, encoding="utf-8", xml_declaration=True)

def copy_to_gm_folders(tiled_tileset_path, gms_background_path, gms_room_path,
                        gms_project_path):
    shutil.copyfile(tiled_tileset_path,
        "%s/background/images/%s" % ('/'.join(gms_project_path.split('/')[:-1]), tiled_tileset_path.split('/')[-1]))
    shutil.copyfile(gms_background_path,
        "%s/background/%s" % ('/'.join(gms_project_path.split('/')[:-1]), gms_background_path.split('/')[-1]))

    shutil.copyfile(gms_room_path,
        "%s/rooms/%s" % ('/'.join(gms_project_path.split('/')[:-1]), gms_room_path.split('/')[-1]))

def add_event_to_object(event_template, object_file, event_type, script_name):
    tree = ElementTree(file=event_template)
    event_root = tree.getroot()
    event_root.set('eventtype', event_type)
    # print("event_root.tag: %s" % event_root.tag)

    action = event_root.find('action')
    arguments = action.find('arguments')
    arg_0 = arguments[0]
    script = arg_0.find('script')
    script.text = script_name

    tree = ElementTree(file=object_file)
    object_root = tree.getroot()
    # print("object_root.tag: %s" % root.tag)

    events = object_root.find('events')
    event = events.append(event_root)

    write_file = open(object_file, "w")
    ElementTree(object_root).write(write_file, encoding="utf-8", xml_declaration=True)
    write_file.close()

def get_gm_objects(gm_project_file):
    tree = ElementTree(file=gm_project_file)
    assets_root = tree.getroot()

    objects = assets_root.find('objects')


    gm_object_list = objects.findall('object')
    gm_objects = []
    for gm_object in gm_object_list:
        gm_objects.append(gm_object.text.split("\\")[1])

    return gm_objects

def add_gm_objects_to_tiled(tiled_project_file, gm_objects):
    tree = ElementTree(file=tiled_project_file)
    map_root = tree.getroot()

    # Get existing objects
    existing_objects = map_root.findall('objectgroup')
    existing_objects_names = []
    for ob in existing_objects:
        existing_objects_names.append(ob.get('name'))

    # print(existing_objects_names)
    # return

    for gm_object in gm_objects:
        if gm_object not in existing_objects_names:
            elem = Element("objectgroup",
                                color = "#0000ff",
                                name = gm_object)
            map_root.append(elem)

    # map_root = fromstring(prettify(map_root))

    tmx_file = open(tiled_project_file, "w")
    ElementTree(map_root).write(tmx_file, encoding="utf-8", xml_declaration=True)
    tmx_file.close()

def get_sprite_size(project_filename, tiled_object):
    sprite_filename = "%s/sprites/%s.sprite.gmx" % (project_filename.rsplit("/", 1)[0],
                        tiled_object.group_name.replace("obj", "spr"))

    tree = ElementTree(file=sprite_filename)
    sprite_root = tree.getroot()

    width = sprite_root.find('width').text
    height = sprite_root.find('height').text

    return width, height

def gms_to_tiled(gms_project_path, tiled_project_path):
    gm_objects = get_gm_objects(gms_project_path)
    add_gm_objects_to_tiled(tiled_project_path, gm_objects)

    msgBox = QMessageBox()
    msg = "Finished copying GMS objects to Tiled"
    msgBox.setText(msg)
    msgBox.exec_()

def tiled_to_gms(tiled_project_path, gms_project_path, gms_room_path,
                    tiled_tileset_path, gms_background_path,):
    object_groups = get_tiled_objects(tiled_project_path)

    # if os.path.isfile("C:/Users/dylan/tiled_maps/crate_land/crate_land.room.gmx"):
    clear_instances_from_room(gms_room_path)

    for group in object_groups:
        for tiled_object in object_groups[group]:
            print(str(tiled_object))
            # create_GMS_sprite(tiled_object,
            #         "C:/Users/dylan/tiled_maps")

            # create_GMS_object(tiled_object,
            #                     "C:/Users/dylan/tiled_maps")

            tiled_object.sprite_width, tiled_object.sprite_height = \
                get_sprite_size(gms_project_path,
                                    tiled_object)

            add_instance_to_room(tiled_object,
                                gms_room_path,
                                tiled_project_path)

    # add_event_to_object("C:/Users/dylan/tiled_maps/template_event.xml",
    #     "C:/Users/dylan/tiled_maps/obj_player.object.gmx",
    #     str(event_types.STEP), "obj_player_step")

    set_room_settings(gms_room_path)

    copy_to_gm_folders(tiled_tileset_path, gms_background_path, gms_room_path,
                         gms_project_path)

    msgBox = QMessageBox()
    msg = "Finished copying Tiled objects to GMS.\n"
    msg += "Please import any backgrounds or rooms inside GMS\n"
    msg += "if they don't exist already."
    msgBox.setText(msg)
    msgBox.exec_()

