#made by Hwang
# import re
# import json_seperator 추가할 것(labelling.py에)
import json
from collections import OrderedDict


# 프로젝트의 json파일 전체를 파라미터로 받을것
# parameter name : project_json
def seperate(project_json, img, user_id, _fname):

    whole_json = project_json
    _dic_sep_json = "./statics/test_json/" + user_id + "/" + _fname + "/"

    # json 생성 위해 OrderedDict 타입 변수 생성
    file_data = OrderedDict()
    img_data = OrderedDict()

    # key 값 분리 : [via att, img_met, set]
    json_keys = [x for x in whole_json.keys()]

    # key별로 value 분리
    json_via_attributes = whole_json['_via_attributes']
    json_via_img_metadata = whole_json['_via_img_metadata']
    json_via_settings = whole_json['_via_settings']

    # 각각 저장하기 위해 file(img) 리스트 생성
    # img_list = [x for x in json_via_img_metadata.keys()]

    # loop 돌려서 각 img별로 json저장
    # for img in img_list:
    file_name = json_via_img_metadata[img]['filename'].split(".")[0]

    # 기존 json과 동일하게 json form 생성
    file_data[json_keys[0]] = json_via_settings
    img_data.clear()
    img_data[img] = json_via_img_metadata[img]
    file_data[json_keys[1]] = img_data
    file_data[json_keys[2]] = json_via_attributes

        # json file save
        # 필요시 경로 수정할 것
    with open(_dic_sep_json + file_name + ".json", "w", encoding="utf-8") as make_file:
        json.dump(file_data, make_file)

