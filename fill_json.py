def fill(project_content, _db_age_list, _db_gender_list):

    content = project_content

    # age, gender list생성
    age_list = []
    gender_list = []
    img_list = [x for x in content['_via_img_metadata'].keys()]

    # _db_age_list가 비어있을 때=> new project 일 때
    if not _db_age_list:
        # age와 gender list 채우기
        # gender_list print: [['study', 'gender'], ['study', 'gender'], ...]
        for img in img_list:
            study_num = img.split("_")[0]

            if content['_via_img_metadata'][img]['file_attributes']['age']:
                age_list.append([study_num, content['_via_img_metadata'][img]['file_attributes']['age']])
            if content['_via_img_metadata'][img]['file_attributes']['gender'] != 'None':
                gender_list.append([study_num, content['_via_img_metadata'][img]['file_attributes']['gender']])

        # age, gender 비워져있는 것 채우기
        for img in img_list:
            study_num = img.split("_")[0]

            # age가 비워져 있는 것
            if not content['_via_img_metadata'][img]['file_attributes']['age']:
                for idx, dic in enumerate(age_list):
                    if study_num == age_list[idx][0]:
                        content['_via_img_metadata'][img]['file_attributes']['age'] = age_list[idx][1]
                        break
            # gender가 비워져 있는 것, default = 'None'
            if content['_via_img_metadata'][img]['file_attributes']['gender'] == "None":
                for idx, dic in enumerate(gender_list):
                    if study_num == gender_list[idx][0]:
                        content['_via_img_metadata'][img]['file_attributes']['gender'] = gender_list[idx][1]
                        break
    # 기존 project 수정했을 때
    else:
        # age, gender list 만들기
        for img in img_list:
            study_num = img.split("_")[0]
            if content['_via_img_metadata'][img]['file_attributes']['age'] == '':
                content['_via_img_metadata'][img]['file_attributes']['age'] = -1
            age_list.append([int(study_num), int(content['_via_img_metadata'][img]['file_attributes']['age'])])
            gender_list.append([int(study_num), content['_via_img_metadata'][img]['file_attributes']['gender']])

        _real_age_list = []
        _real_gender_list = []

        # 기존 db에 저장된 [study, age] 또는 [study, gender] 와 겹치는 값은 삭제
        for i in age_list:
            if i not in _db_age_list:
                _real_age_list.append(i)
        for i in gender_list:
            if i not in _db_gender_list:
                _real_gender_list.append(i)

        # 반복분 이용 중복 제거된 age, gender list값으로 현재 파일의 age, gender값 치환
        for img in img_list:
            study_num = int(img.split("_")[0])
            for idx, dic in enumerate(_real_age_list):
                if study_num == _real_age_list[idx][0]:
                    content['_via_img_metadata'][img]['file_attributes']['age'] = _real_age_list[idx][1]
            for idx, dic in enumerate(_real_gender_list):
                if study_num == _real_gender_list[idx][0]:
                    content['_via_img_metadata'][img]['file_attributes']['gender'] = _real_gender_list[idx][1]

    return content
