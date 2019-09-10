import json
from flask import Flask, render_template, json, request,redirect,session
import codecs
from xml.etree.ElementTree import Element, SubElement, dump, ElementTree
from PIL import Image


def create_xml(content, x, _dic_img, _dic_xml, _first):
    c = content

    # xml 생성 부분
    anote = Element("annotation")

    # 아래부터 anntation 태그 내부
    # folder, path 지정 필요
    folder = Element('folder')
    folder.text = '미정'
    anote.append(folder)
    SubElement(anote, 'filename').text = c['_via_img_metadata'][x]['filename']
    SubElement(anote, 'path').text = c['_via_settings']['core']['default_filepath']
    source = Element('source')
    anote.append(source)

    # 아래는 source 태그 내부 / db는 필요시 조정
    SubElement(source, 'database').text = 'Unknown'
    size = Element('size')
    anote.append(size)

    # img의 width와 heignt삽입, depth=?,
    # 아래는 size태그 내부 / segmented 값을 필요시 조정
    i = Image.open(_dic_img + c['_via_img_metadata'][x]['filename'])
    img_size = i.size
    SubElement(size, 'width').text = str(img_size[0])
    SubElement(size, 'heigth').text = str(img_size[1])
    SubElement(size, 'depth').text = '3'
    SubElement(anote, 'segmented').text = '0'

    # 사각형이 여러개 일때 objec태그도 여러개 생성 -> json의 regions와 대칭
    # 아래는 object 태그 내부 / 0으로 설정한 값은 필요시 조정
    obj_list = [ob for ob in c['_via_img_metadata'][x]['regions']]
    for y in range(len(obj_list)):
        obj = Element('object')
        anote.append(obj)
        if _first < 2:
            SubElement(obj, 'name').text = [ob for ob in c['_via_img_metadata'][x]['regions']][y]['region_attributes'][
                '골절 판독 구분']
        else:
            SubElement(obj, 'name').text = [ob for ob in c['_via_img_metadata'][x]['regions']][y]['region_attributes'][
                'Osteophytes']
        SubElement(obj, 'pose').text = 'Unspecified'
        SubElement(obj, 'truncated').text = '0'
        SubElement(obj, 'difficult').text = '0'
        bndbox = Element('bndbox')
        obj.append(bndbox)

        # via에서 넘겨주는 x,y값을 xml의 형식에 맞춤
        SubElement(bndbox, 'xmin').text = str([ob for ob in c['_via_img_metadata'][x]['regions']][y]['shape_attributes'][
            'x'])
        SubElement(bndbox, 'ymin').text = str([ob for ob in c['_via_img_metadata'][x]['regions']][y]['shape_attributes'][
            'y'])
        SubElement(bndbox, 'xmax').text = str([ob for ob in c['_via_img_metadata'][x]['regions']][y]['shape_attributes'][
            'x']+[ob for ob in c['_via_img_metadata'][x]['regions']][y]['shape_attributes'][
            'width'])
        SubElement(bndbox, 'ymax').text = str([ob for ob in c['_via_img_metadata'][x]['regions']][y]['shape_attributes'][
            'y']+[ob for ob in c['_via_img_metadata'][x]['regions']][y]['shape_attributes'][
            'height'])

    # xml파일 보기좋게 정렬
    def indent(elem, level=0):
        b = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = b + "    "
            if not elem.tail or not elem.tail.strio():
                elem.tail = b
                for elem in elem:
                    indent(elem, level+1)
                if not elem.tail or not elem.tail.strip():
                    elem.tail = b
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = b

    indent(anote)
    # dump(anote)
    # filename이 333.jpg 형식으로 되어있기 때문에 slice해서 333.xml 형식으로 저장되게 함
    ElementTree(anote).write(_dic_xml + c['_via_img_metadata'][x]['filename'].split('.')[0]+'.xml')
