"""
요청 정보로 랜딩 페이지 소스코드를 구성하는 작업을 담당
"""
import base64
import json

from bs4 import BeautifulSoup


def _convert_to_html(tag_string):
    return BeautifulSoup(tag_string, 'html.parser')


class Default:
    """랜딩 페이지의 기본 HTML, CSS, JS"""

    def __init__(self, landing_config):
        """
        2019/09/03

        :param landing_config:
        """
        self.default_html = f"""
                        <!DOCTYPE html>
                <html lang="ko-kr">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="x-ua-compatible" content="ie=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
                    <title>{landing_config['title']}</title>

                    <meta name="robots" content="index,follow">
                    <link rel="shortcut icon" href="https://landings.infomagazine.xyz/favicon.ico" type="image/x-icon">
                    <link rel="icon" href="https://landings.infomagazine.xyz/favicon.ico" type="image/x-icon">
                </head>
                <body>
                </body>
                </html>
                """
        self.default_stylesheets = """
                <link rel="stylesheet" href="https://assets.infomagazine.xyz/css/normalize.css">
                <style>
                *, ::after, ::before {
                    box-sizing: border-box;
                }

                body {
                    font-size: 3vw;
                }

                a {
                    text-decoration: none;
                    color: #000;
                }

                img {
                    width: 100%;
                    display: block;
                }

                input {
                    border: 1px solid #808080;
                }

                .section-container {
                    max-width: 1000px;
                    margin: 0 auto;
                }

                .landing-section {
                    position: relative;
                    width: 100%;
                    min-height: 1px;
                }

                .landing-object-block {
                    position: absolute;
                }

                .object-type-image {
                    overflow: hidden;
                    height: 0;
                }

                .object-type-form {
                    width: 100%;
                    position: relative;
                    background: transparent;
                    overflow: auto;
                }

                .object-type-form::before {
                    content: "";
                    width: 1px;
                    margin-left: -1px;
                    float: left;
                    height: 0;
                }

                .object-type-form::after {
                    content: "";
                    display: table;
                    clear: both;
                }

                .form-group {
                    position: absolute;
                    display: flex;
                    align-items: center;
                }
                
                .form-group.terms{
                    font-size: 1.7vw;
                }
                
                .form-group.terms a{
                    color: #007bff;
                    cursor: pointer;
                }

                .form-group-prepend {
                    display: flex;
                }

                .form-group-label {
                    display: flex;
                    align-items: center;
                }

                .form-control {
                    width: 1%;
                    display: flex;
                    align-items: center;
                    flex: 1 1 auto;
                    height: 5vw;
                    border-radius: 0.5vw;
                }

                .form-button {
                    width: 100%;
                    border: 1px solid;
                    background-color: #fff;
                    cursor: pointer;
                    padding: 0.5vw;
                    border-radius: 0.5vw;
                }
                
                input.form-button {
                    border: none;
                    border-radius: unset;
                    background-repeat: no-repeat;
                    background-position: center;
                    background-size: 100%;
                }
                
                .video-box {
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    top: 0;
                    left: 0;
                }

                @media (min-width: 1000px) {
                    body {
                        font-size: 1.9rem;
                    }

                    .form-control {
                        height: 50px;
                        border-radius: 5px
                    }
                    
                    .form-group.terms{
                        font-size: 1.3rem;
                    }

                    .form-button {
                        height: 50px;
                        padding: 5px;
                        border-radius: 5px
                    }
                }
                
                .dim-layer {
                  display: none;
                  position: fixed;
                  top: 0;
                  left: 0;
                  width: 100%;
                  height: 100%;
                  z-index: 100;
                }
                
                .dim-layer .dim-background {
                  position: absolute;
                  top: 0;
                  left: 0;
                  width: 100%;
                  height: 100%;
                  background: #000;
                  opacity: .5;
                  filter: alpha(opacity=50);
                }
                
                .pop-layer .pop-container {
                  padding: 10px;
                }
                
                .pop-layer {
                  position: absolute;
                  top: 5%;
                  left: 5%;
                  right: 5%;
                  bottom: 5%;
                  width: 90%;
                  overflow: scroll;
                  background-color: #fff;
                  border: 5px solid #3571B5;
                  z-index: 10;
                }
            </style>
                """
        self.default_scripts = """
                <script src="https://assets.infomagazine.xyz/vendor/js/jquery-3.4.1.min.js"></script>
                <script src="https://assets.infomagazine.xyz/vendor/js/lazyload.min.js"></script>
                <script>
                (function ($) {{
                    var isIE = /*@cc_on!@*/false || !!document.documentMode;
                    
                    if(!sessionStorage.getItem('current_epoch_time')){
                        sessionStorage.setItem('current_epoch_time', Date.now());    
                    }

                    if(isIE){
                        $('body').attr('class','ie-check');
                    }else{
                        $('.lazyload').lazyload();
                    }
                }})(jQuery)
                </script>
                """
        self.layout_stylesheets = ""
        self.landing_scripts = ""


class StyleSheet(Default):
    """랜딩페이지의 스타일시트 생성"""

    def __init__(self, landing_config):
        self.landing_config = landing_config
        super(StyleSheet, self).__init__(landing_config)

    def _css_section_height(self, section_id=None, section_h=None):
        """
        2019/09/03

        섹션의 전체 높이를 설정한다.
        margin을 이용하여 다이나믹한 높이를 설정.

        :param section_id: 섹션 번호
        :param section_h: 섹션 전체 높이
        """
        height = section_h / 10
        result = f"""
        section[data-section-id="{section_id}"] {{
            margin-bottom: calc({height}% - 1px);
        }}
        """
        self.layout_stylesheets += result

    def _css_object_block_size(self, section_id=None, object_id=None, layout_info=None):
        """
        2019/09/03

        섹션안의 객체 블록 사이즈를 설정.
        객체 블록은 이미지, DB폼, 동영상을 감싸고 있다.

        :param section_id: 섹션 번호
        :param object_id: 객체 번호
        :param layout_info: 객체의 사이즈 정보 딕셔너리
        """
        object_x = layout_info['position']['x']
        object_y = layout_info['position']['y']
        object_w = layout_info['position']['w']

        ob_x_ratio = object_x / 10
        ob_y_ratio = object_y / 10
        ob_width_ratio = object_w / 10
        result = f"""
        section[data-section-id="{section_id}"] > div[data-object-id="{object_id}"] {{
            margin-left: {ob_x_ratio}%;
            margin-top: {ob_y_ratio}%;
            width: {ob_width_ratio}%;
        }}
        """
        self.layout_stylesheets += result

    def _css_object_by_type_size(self, object_type=None, section_id=None, object_id=None, layout_info=None):
        """
        2019/09/03

        객체의 타입별 사이즈 설정.

        :param object_type: 객체 타입
        :param section_id: 섹션 번호
        :param object_id: 객체 번호
        :param layout_info: 객체 정보 딕셔너리

        object_type == 1 : 이미지 객체
        object_type == 2 : 폼 객체
        object_type == 3 : 비디오 객체
        """
        object_w = layout_info['position']['w']
        object_h = layout_info['position']['h']

        object_image_url = ""
        if layout_info['image_data']:
            object_image_url = layout_info['image_data']

        result = f""""""
        if object_type == 1:
            result += f"""
            section[data-section-id="{section_id}"] > div[data-object-id="{object_id}"] > .object-type-image {{
                padding-top: calc({object_h} / {object_w} * 100%);
                background-position : center;
                background-size: 100%;
                background-repeat: no-repeat;
            }}
            .ie-check section[data-section-id="{section_id}"] > div[data-object-id="{object_id}"] > .object-type-image {{
                padding-top: calc({object_h} / {object_w} * 100%);
                background: url('{object_image_url}') center / 100% no-repeat;
            }}
            """
        elif object_type == 2:
            result += f"""
            section[data-section-id="{section_id}"] > div[data-object-id="{object_id}"] > .object-type-form {{
                padding-top: calc({object_h} / {object_w} * 100%);
            }}
            """

        elif object_type == 3:
            result += f"""
            section[data-section-id="{section_id}"] > div[data-object-id="{object_id}"] > .object-type-video {{
                position: relative; 
                padding-top: calc({object_h} / {object_w} * 100%);
            }}
            """
        self.layout_stylesheets += result

    def _css_field_position(self, section_id=None, object_id=None, object_w=None, object_h=None, field_id=None,
                            field_info=None, field_position_set=None):
        """
        2019/09/03

        DB폼 내의 각 필드의 블록 사이즈와 위치를 설정.

        :param section_id: 섹션 번호
        :param object_id: 객체 번호
        :param object_w: 객체 가로 길이
        :param object_h: 객체 높이
        :param field_id: 필드 번호
        :param field_info: 필드 인포
        :param field_position_set: 필드 위치 정보
        """
        field_x = field_position_set['x']
        field_y = field_position_set['y']
        field_w = field_position_set['w']
        field_h = field_position_set['h']

        field_x_ratio = round((field_x * 100) / object_w, 6)
        field_y_ratio = round((field_y * 100) / object_h, 6)
        field_w_ratio = round((field_w * 100) / object_w, 6)

        result = f"""
        section[data-section-id="{section_id}"] > div[data-object-id="{object_id}"] > form > div[data-form-filed-id="{field_id}"] {{
            top: {field_y_ratio}%;
            left: {field_x_ratio}%;
            width: {field_w_ratio}%;
        }}
        """
        self.layout_stylesheets += result

    def _css_field_label_size(self, section_id=None, object_id=None, field_info_list=None, form_group_id=None):
        """
        2019/09/03

        필드의 라벨 가로 길이를 설정.

        :param section_id: 섹션 번호
        :param object_id: 객체 번호
        :param field_info_list: 필드 정보 리스트
        :param form_group_id: 폼 그룹 번호
        :return:
        """
        field_name_list = [len(field['name'])
                           for field_index, field
                           in enumerate(field_info_list)
                           if int(field['form_group_id']) == int(form_group_id)]
        label_len_list = list(set(field_name_list))
        label_len_list.sort()

        # 적정 라벨 넓이 계산
        is_long_spacing = False
        standard_len = label_len_list[0]
        diff_tmp = standard_len
        for index in range(1, len(label_len_list)):
            diff = label_len_list[index] - label_len_list[index - 1]

            if diff == diff_tmp or (diff < diff_tmp and not is_long_spacing):
                standard_len = label_len_list[index]

            if diff > diff_tmp:
                standard_len = label_len_list[index - 1]
                is_long_spacing = True
            diff_tmp = diff

        result = f"""
        section[data-section-id="{section_id}"] > div[data-object-id="{object_id}"] .form-group-prepend {{
            width: {standard_len * 3}vw;
        }}
        @media (min-width: 1000px) {{
            section[data-section-id="{section_id}"] > div[data-object-id="{object_id}"] .form-group-prepend {{
                width: {standard_len * 30}px;
            }}
        }}
        """
        self.layout_stylesheets += result

    def _stylesheets_generate(self):
        """
        2019/09/03

        생성된 모든 스타일시트를 반환

        :return: 모든 스타일시트
        """
        result = self.default_stylesheets
        result += f"""<style>{self.layout_stylesheets}</style>"""
        return result


class Script(Default):
    """랜딩페이지의 스크립트 작성"""

    def __init__(self, landing_config):
        self.landing_config = landing_config
        super(Script, self).__init__(landing_config)

        self.tnk_script_check = False
        if landing_config['tracking_info']['tnk']:
            self.tnk_script_check = True
        self.facebook_pixel_check = False
        if landing_config['tracking_info']['fb']:
            self.facebook_pixel_check = True
        self.kakao_pixel_check = False
        if landing_config['tracking_info']['ka']:
            self.kakao_pixel_check = True
        self.google_analytics = False
        if landing_config['tracking_info']['ga']:
            self.google_analytics = True
        self.google_tag_manager = False
        if landing_config['tracking_info']['gtm']:
            self.google_tag_manager = True
        self.google_display_network = False
        if landing_config['tracking_info']['gdn']:
            self.google_display_network = True

    def _js_init_datepicker(self, field_id=None):
        """
        2019/09/03

        캘린더 설정 초기화

        :param field_id: 필드 번호
        """
        result = f"""
        $('#{field_id}').datepicker({{
            format: 'yyyy-mm-dd',
            date: new Date(1989, 6, 20),
            yearFirst: true,
            language: 'ko-KR',
            autoHide: true
        }});
        """
        self.landing_scripts += result

    def _js_submit_event(self, section_id=None, item_group=None):
        """
        2019/09/03

        DB등록 이벤트 생성

        :param section_id: 섹션 번호
        :param item_group: 보낼 DB들의 정보 묶음
        """
        converted_item_group = {}
        for item in item_group:
            if item['type'] == 9 and 'required' in item['validation']:
                item['validation'].append('checked')
            converted_item_group[item['name']] = {'target': item['target'], 'validation': item['validation']}

        result = f"""
        $("#form_{section_id}_submit_button").click(function () {{
            var $this = $(this);
            $this.attr("disabled",true);
            var item_group = {json.dumps(converted_item_group)};
            form_{section_id}_validation($this,item_group);
            call_form_{section_id}_ajax($this,item_group)
        }});
        """
        self.landing_scripts += result

    def _js_validation(self, section_id=None):
        """
        2019/09/03

        DB폼 벨리데이션 생성

        :param section_id: 섹션 번호
        """
        result = f"""
        function form_{section_id}_validation($this, item_group) {{
            // required
            // korean_only
            // english_only
            // number_only
            // email
            // phone_only
            // age_limit

            var required_list = [];
            var only_korean_list = [];
            var only_english_list = [];
            var only_num_list = [];
            var email_list = [];
            var tel_num_list = [];
            var age_limit_list = [];
            var checked_list = [];
            $.each(item_group,function(key,value){{
                var _target = eval(value['target']);
                if (value['validation'].indexOf('required') !== -1) {{
                    if (value['validation'].indexOf('checked') !== -1){{
                        if(!_target.is(":checked")){{
                            checked_list.push(_target.attr('data-label-name'))
                        }}
                    }}
                    if (!_target.val()) {{
                        required_list.push(_target.attr('data-label-name'));
                    }}
                }}
                if (value['validation'].indexOf('korean_only') !== -1) {{
                    var only_korean_regex = /[^가-힣]/;
                    if (only_korean_regex.test(_target.val())) {{
                        only_korean_list.push(_target.attr('data-label-name'));
                    }}
                }}
                if (value['validation'].indexOf('english_only') !== -1) {{
                    var only_english_regex = /[^a-zA-Z]/;
                    if (only_english_regex.test(_target.val())) {{
                        only_english_list.push(_target.attr('data-label-name'));
                    }}
                }}
                if (value['validation'].indexOf('number_only') !== -1) {{
                    var only_num_regex = /[^0-9]/;
                    if (only_num_regex.test(_target.val())) {{
                        only_num_list.push(_target.attr('data-label-name'));
                    }}
                }}
                if (value['validation'].indexOf('email') !== -1) {{
                    var email_regex = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{{2,3}}$/i;
                    if (!email_regex.test(_target.val())) {{
                        email_list.push(_target.attr('data-label-name'));
                    }}
                }}
                if (value['validation'].indexOf('phone_only') !== -1) {{
                    var tel_num_regex = /^(010)\d{{3,4}}\d{{4}}$/;
                    if (!tel_num_regex.test(_target.val())) {{
                        tel_num_list.push(_target.attr('data-label-name'));
                    }}
                }}
                if (value['validation'].indexOf('age_limit') !== -1) {{
                    var now_date = new Date();
                    var birthday_date = new Date(_target.val());
                    var new_now_date = new Date(now_date.getUTCFullYear() + "-" + (now_date.getUTCMonth() + 1) + "-" + now_date.getUTCDate());
                    var american_age_date = new Date((now_date.getUTCFullYear() - 19) + "-" + (now_date.getUTCMonth() + 1) + "-" + now_date.getUTCDate());
                    if (((now_date.getTime() + 32400000) - birthday_date.getTime()) < (new_now_date.getTime() - american_age_date.getTime())) {{
                        age_limit_list.push(_target.attr('data-label-name'));
                    }}
                }}
            }});
            validate_generator(required_list, "을(를) 입력해주세요.");
            validate_generator(only_korean_list, "은(는) 유효한 한글이 아닙니다.");
            validate_generator(only_english_list, "은(는) 유효한 영어가 아닙니다.");
            validate_generator(only_num_list, "은(는) 유효한 숫자가 아닙니다.");
            validate_generator(email_list, "은(는) 유효한 이메일이 아닙니다.");
            validate_generator(tel_num_list, "은(는) 유효한 전화번호가 아닙니다.");
            validate_generator(age_limit_list, "이(가) 만 19세 이하 제한에 걸립니다.");
            validate_generator(checked_list, "를 체크해주시기 바랍니다.");
            function validate_generator(list, message) {{
                if (list.length !== 0) {{
                    var list_total = "";
                    for (var i = 0; i < list.length; i++) {{
                        if (i === 0) {{
                            list_total += (list[i])
                        }} else {{
                            list_total += (", " + list[i])
                        }}
                    }}
                    $this.removeAttr('disabled')
                    alert(list_total + message);
                    throw list_total + message;
                }}
            }}
        }}
        """
        self.landing_scripts += result

    def _js_call_ajax(self, section_id=None):
        """
        2019/09/03

        DB입력 AJAX

        :param section_id: 섹션 번호
        """
        tnk_script_callback = ""
        if self.tnk_script_check:
            tnk_script_callback = "TnkSession.actionCompleted();"

        facebook_pixel_callback = ""
        if self.facebook_pixel_check:
            facebook_pixel_callback = "fbq('track', 'CompleteRegistration');"

        kakao_pixel_callback = ""
        if self.kakao_pixel_check:
            kakao_pixel_callback = f"kakaoPixel('{self.landing_config['tracking_info']['ka']}').completeRegistration();"

        callback_script = self.landing_config['callback_script'] or ""

        result = f"""
        function call_form_{section_id}_ajax($this,item_group) {{
            var body = {{
                'data': {{}},
                'schema': {{}}
            }};
            var stay_time = Math.round((Date.now() - sessionStorage.getItem('current_epoch_time'))/1000);
            $.each(item_group,function(key,value){{
                var _target = eval(value['target']);
                body['data'][key] = _target.val();
                body['schema'][key] = _target.attr('data-label-name');
            }});
            body['landing_id'] = window.location.pathname.split('/')[1];
            body['registered_date'] = String(Date.now());
            body['stay_time'] = stay_time;
            $.ajax({{
                method: 'POST',
                contentType: "application/json;", // MIME type to request
                url: 'https://serverlessapi.infomagazine.xyz/db/',
                data: JSON.stringify(body),
                success: function (data) {{
                    if (data['state'] === true) {{
                        {tnk_script_callback}
                        {facebook_pixel_callback}
                        {kakao_pixel_callback}
                        {callback_script}
                    }}
                    alert(data['message']);
                    sessionStorage.setItem('current_epoch_time', Date.now());
                }},
                error: function (data) {{
                    var response = data.responseText;
                    var parsed_response = $.parseJSON(response)
                    alert(parsed_response['message']);
                }}
            }}).always(function () {{
                $this.removeAttr('disabled')
            }})
        }}
        """
        self.landing_scripts += result

    def _js_call_ajax_by_phone_auth(self, section_id=None):
        """
        2019/09/03

        번호 인증이 추가된 DB입력 AJAX

        :param section_id: 섹션 번호
        """
        result = f"""
                function call_form_{section_id}_ajax(item_group) {{
                    var IMP = window.IMP;
                    IMP.init("imp77156252");
                    IMP.certification({{ // param
                        merchant_uid: "axa_img_tnk",
                        phone: $("#first_user_phone_1").val() + $("#first_user_phone_2").val() + $("#first_user_phone_3").val()
                    }}, function (rsp) {{ // callback
                        if (rsp.success) {{
                            $.ajax({{
                                type: 'get',
                                url: '',
                                data: {{imp_uid: rsp.imp_uid}},
                                dataType: 'json',
                                success: function (data) {{
                                    if (data) {{
                                        first_db_reg_ajax(data.data['name'], data.data['birth'], data.data['gender'])
                                        var body = {{
                                            'data': {{
                                                'form_{section_id}_name': data.data['name'],
                                                'form_{section_id}_birth': data.data['birth'],
                                                'form_{section_id}_gender': data.data['gender'],
                                            }},
                                            'schema': {{
                                                'form_{section_id}_name': '이름',
                                                'form_{section_id}_birth': '생년월일',
                                                'form_{section_id}_gender': '성별',
                                            }}
                                        }};
                                        Object.entries(item_group).forEach(function (item) {{
                                            var _target = eval(item[1]['target']);
                                            body['data'][item[0]] = _target.val();
                                            body['schema'][item[0]] = _target.attr('data-label-name');
                                        }});
                                        $.ajax({{
                                            type: 'post',
                                            url: 'https://api.infomagazine.xyz/db/',
                                            data: body,
                                            dataType: 'json',
                                            success: function (data) {{
                                                if (data) {{
                                                    alert('신청이 완료되었습니다.');
                                                }} else {{
                                                    alert("이미 신청하셨습니다.");
                                                }}
                                            }},
                                            error: function (data) {{
                                                alert('에러');
                                            }}
                                        }})
                                    }} else {{
                                        alert("인증 정보를 얻는데 실패하였습니다.");
                                    }}
                                }},
                                error: function (data) {{
                                    alert('일시적인 오류로 신청이 안 되었습니다.');
                                }}
                            }})
                            // first_db_reg_ajax()
                        }} else if (rsp.error_code === "F0000") {{
                            alert("인증 취소");
                        }} else {{
                            alert("인증에 실패하였습니다. 에러 내용: " + rsp.error_msg);
                        }}
                    }});
                }}
                """
        self.landing_scripts += result

    # TODO 업그레이드 필요
    def _js_terms_trigger(self):
        """
        2019/09/03

        :return: 약관 트리거 이벤트
        """
        result = """
        $('.terms-button').click(function(){
            $('#popup-layer').fadeIn();
            $('.dim-background, .terms-close-button').click(function(){
                $('#popup-layer').fadeOut();
            })
        })
        """
        self.landing_scripts += result

    def _scripts_generate(self):
        """
        2019/09/03

        생성된 모든 스크립트 반환

        :return: 모든 스크립트
        """

        result = self.default_scripts
        result += f"""
        <script>
        (function ($) {{
            {self.landing_scripts}
        }})(jQuery)
        </script>
        """

        return result

    def _facebook_pixel_head(self):
        """
        2019/08/23

        :return: 페이스북 픽셀 공통 스크립트
        """

        return f"""
        <!-- Facebook Pixel Code -->
        <script>
          !function(f,b,e,v,n,t,s)
          {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
          n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
          if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
          n.queue=[];t=b.createElement(e);t.async=!0;
          t.src=v;s=b.getElementsByTagName(e)[0];
          s.parentNode.insertBefore(t,s)}}(window, document,'script',
          'https://connect.facebook.net/en_US/fbevents.js');
          fbq('init', '{self.landing_config['tracking_info']['fb']}');
          fbq('track', 'PageView');
        </script>
        <!-- End Facebook Pixel Code -->
        """

    def _tnk_script(self):
        """
        2019/09/05

        :return: tnk script 공통 스크립트
        """
        return """
        <script src="//api3.tnkfactory.com/tnk/js/tnk-webapi-cpatrack.1.3.js"></script>
        """

    def _facebook_pixel_body(self):
        """
        2019/08/23

        :return: 페이스북 픽셀 노스크립트
        """

        return f"""
        <!-- Facebook Pixel Code -->
        <noscript><img height="1" width="1" style="display:none"
          src="https://www.facebook.com/tr?id={self.landing_config['tracking_info']['fb']}&ev=PageView&noscript=1"
        /></noscript>
        <!-- End Facebook Pixel Code -->
        """

    def _kakao_pixel(self):
        """
        2019/08/23

        :return: 카카오 픽셀 공통 스크립트
        """

        return f"""
        <script type="text/javascript" charset="UTF-8" src="//t1.daumcdn.net/adfit/static/kp.js"></script>
        <script type="text/javascript">
              kakaoPixel('{self.landing_config['tracking_info']['ka']}').pageView();
        </script>
        """

    def _google_display_network(self):
        """
        2019/08/23

        :return: GDN 공통 스크립트
        """

        return f"""
        <!-- Global site tag (gtag.js) - Google Ads: {self.landing_config['tracking_info']['gdn']} -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={self.landing_config['tracking_info']['gdn']}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', '{self.landing_config['tracking_info']['gdn']}');
        </script>
        """

    def _hijack(self):
        """
        2019/09/03

        :return: 후팝업 스크립트
        """
        return f"""
        <!--Backward catch that called 후팝업 -->
        <script>
        history.replaceState(null, document.title, location.pathname+"#!/stealingyourhistory");
        history.pushState(null, document.title, location.pathname);

        window.addEventListener("popstate", function() {{
            if(location.hash === "#!/stealingyourhistory") {{
                history.replaceState(null, document.title, location.pathname);
                setTimeout(function(){{
                    location.replace('{self.landing_config['hijack_url']}');
                }},0);
            }}
        }}, false);
        </script>
        """


class LandingPage(StyleSheet, Script):
    """주어진 랜딩 정보로 랜딩 페이지를 생성"""

    def __init__(self, landing_info, is_generate=False):
        self.landing_config = landing_info['landing']
        super(LandingPage, self).__init__(landing_config=self.landing_config)
        self.term_config = landing_info['term']
        self.form_config_list = landing_info['form']
        self.field_info_list = landing_info['field']
        self.section_info_list = landing_info['sections']
        self.is_generate = is_generate

        self.is_datepicker_to_add = False
        self.is_phone_auth_to_add = False
        self.is_terms_to_add = False

    def _db_form_field_generator(self, base_html, section_id=None,
                                 object_id=None, object_w=None,
                                 object_h=None, field_id=None,
                                 field_info=None, field_position_set=None):
        """
        2019/09/03

        DB폼 필드 생성

        1: 텍스트 - input text
        2: 숫자 - input number
        3: 전화번호 - input number
        4: 선택 스크롤 - select, opt
        5: 선택 버튼 - radio
        6: 체크 박스 - chk
        7: 날짜 - date
        8: 완료버튼 - script
        9: 약관동의 - chk

        :return: 필드 번호, 필드 타입, jQuery객체, 벨리데이션
        """
        self._css_field_position(section_id=section_id,
                                 object_id=object_id,
                                 object_w=object_w,
                                 object_h=object_h,
                                 field_id=field_id,
                                 field_info=field_info,
                                 field_position_set=field_position_set[
                                     'position'])
        form_group = base_html.new_tag('div', attrs={'class': 'form-group', 'data-form-filed-id': field_id})

        field_id = 'form_' + str(section_id) + '_' + base64.b64encode(field_info['name'].encode('utf-8')).decode(
            'utf-8')

        equal_check = "=" in field_id
        while equal_check:
            field_id = field_id.replace('=', '')
            if "=" not in field_id:
                break

        field_type = int(field_info['type'])

        if field_type == 1:
            label_wrap_tag = base_html.new_tag('div', attrs={'class': 'form-group-prepend'})
            label_tag = base_html.new_tag('label', attrs={'for': field_id,
                                                          'class': 'form-group-label'})
            label_tag.string = field_info['name']
            label_wrap_tag.append(label_tag)
            input_tag = base_html.new_tag('input', attrs={'type': 'text',
                                                          'id': field_id,
                                                          'class': 'form-control',
                                                          'placeholder': field_info['holder'],
                                                          'data-label-name': field_info['name']})
            form_group.append(label_wrap_tag)
            form_group.append(input_tag)
        elif field_type == 2:
            label_wrap_tag = base_html.new_tag('div', attrs={'class': 'form-group-prepend'})
            label_tag = base_html.new_tag('label', attrs={'for': field_id,
                                                          'class': 'form-group-label'})
            label_tag.string = field_info['name']
            label_wrap_tag.append(label_tag)
            input_tag = base_html.new_tag('input', attrs={'type': 'number',
                                                          'id': field_id,
                                                          'class': 'form-control',
                                                          'placeholder': field_info['holder'],
                                                          'data-label-name': field_info['name']})
            form_group.append(label_wrap_tag)
            form_group.append(input_tag)
        elif field_type == 3:
            label_wrap_tag = base_html.new_tag('div', attrs={'class': 'form-group-prepend'})
            label_tag = base_html.new_tag('label', attrs={'for': field_id,
                                                          'class': 'form-group-label'})
            label_tag.string = field_info['name']
            label_wrap_tag.append(label_tag)
            input_tag = base_html.new_tag('input', attrs={'type': 'tel',
                                                          'id': field_id,
                                                          'class': 'form-control',
                                                          'placeholder': field_info['holder'],
                                                          'data-label-name': field_info['name']})
            form_group.append(label_wrap_tag)
            form_group.append(input_tag)
        elif field_type == 4:
            input_tag = base_html.new_tag('input', attrs={'type': 'select'})
            form_group.append(input_tag)
        elif field_type == 5:
            label_wrap_tag = base_html.new_tag('div', attrs={'class': 'form-group-prepend'})
            label_tag = base_html.new_tag('span', attrs={'class': 'form-group-label'})
            label_tag.string = field_info['name']
            label_wrap_tag.append(label_tag)
            form_group.append(label_wrap_tag)
            for index, radio_value in enumerate(field_info['list']):
                radio_attrs = {
                    'type': 'radio',
                    'id': field_id + "_" + str(index),
                    'name': field_id,
                    'value': radio_value,
                    'data-label-name': field_info['name']
                }
                if field_info['default'] == radio_value:
                    radio_attrs['checked'] = ""
                radio_wrap_tag = base_html.new_tag('div', attrs={'class': 'form-control'})
                input_tag = base_html.new_tag('input', attrs=radio_attrs)
                label_tag = base_html.new_tag('label', attrs={'for': field_id + "_" + str(index),
                                                              'class': 'form-group-label'})
                label_tag.string = radio_value
                radio_wrap_tag.append(input_tag)
                radio_wrap_tag.append(label_tag)
                form_group.append(radio_wrap_tag)
        elif field_type == 6:
            input_tag = base_html.new_tag('input', attrs={'type': 'checkbox'})
            form_group.append(input_tag)
        elif field_type == 7:
            label_wrap_tag = base_html.new_tag('div',
                                               attrs={'class': 'form-group-prepend'})
            label_tag = base_html.new_tag('label', attrs={'for': field_id,
                                                          'class': 'form-group-label'})
            label_tag.string = field_info['name']
            label_wrap_tag.append(label_tag)
            input_tag = base_html.new_tag('input', attrs={'type': 'text',
                                                          'id': field_id,
                                                          'class': 'form-control',
                                                          'placeholder': field_info['holder'],
                                                          'data-label-name': field_info['name'],
                                                          'data-toggle': 'datepicker',
                                                          'readonly': ''})
            form_group.append(label_wrap_tag)
            form_group.append(input_tag)
            self._js_init_datepicker(field_id=field_id)
            if not self.is_datepicker_to_add:
                self.default_stylesheets += """
                    <link rel="stylesheet" href="https://assets.infomagazine.xyz/vendor/css/datepicker.min.css">
                    """
                self.default_scripts += """
                    <script src="https://assets.infomagazine.xyz/vendor/js/datepicker.min.js"></script>
                    <script src="https://assets.infomagazine.xyz/vendor/js/datepicker.ko-KR.js"></script>
                    """
                self.is_datepicker_to_add = True
        elif field_type == 8:
            if not field_info['image_data']:
                button_tag = base_html.new_tag('button', attrs={'type': 'button',
                                                                'class': 'form-button',
                                                                'id': "form_" + str(section_id) + "_submit_button"})
                button_tag.string = field_info['name']
            else:
                button_tag = base_html.new_tag('input', attrs={'type': 'button',
                                                               'class': 'form-button',
                                                               'id': "form_" + str(section_id) + "_submit_button",
                                                               'style': 'background-image: url(' + field_info[
                                                                   'image_data'] + ')'})
            form_group.append(button_tag)
        elif field_type == 9:
            form_group.attrs.update({'class': 'form-group terms'})
            label_tag = base_html.new_tag('label', attrs={'for': field_id,
                                                          'class': 'form-group-label'})
            label_tag.string = field_info['holder']

            checkbox_option = {'type': 'checkbox',
                               'id': field_id,
                               'data-label-name': field_info['name']}
            if field_info['default']:
                checkbox_option.update({'checked': 'checked'})
            input_tag = base_html.new_tag('input', attrs=checkbox_option)
            form_group.append(input_tag)
            form_group.append(label_tag)
            if self.landing_config['is_term']:
                a_tag_to_terms_attr_option = {'class': 'terms-button'}

                if self.term_config['url']:
                    a_tag_to_terms_attr_option.update({'href': self.term_config['url'], 'target': '_blank'})
                else:
                    if not self.is_terms_to_add:
                        div_to_dim_layer = base_html.new_tag('div', attrs={'id': 'popup-layer', 'class': 'dim-layer'})
                        div_to_dim_background = base_html.new_tag('div', attrs={'class': 'dim-background'})
                        div_to_popup_layer = base_html.new_tag('div', attrs={'class': 'pop-layer'})
                        div_to_popup_container = base_html.new_tag('div', attrs={'class': 'pop-container'})
                        div_to_popup_contents = base_html.new_tag('div', attrs={'class': 'pop-contents'})
                        div_to_terms_title = base_html.new_tag('h4', attrs={'class': 'terms-title'})
                        div_to_terms_title.string = self.term_config['title']
                        div_to_terms_contents = base_html.new_tag('div', attrs={'class': 'terms-contents'})
                        div_to_terms_contents.append(
                            _convert_to_html('<br/>'.join(self.term_config['content'].splitlines())))
                        div_to_close_button = base_html.new_tag('button', attrs={'class': 'terms-close-button'})
                        div_to_close_button.string = "닫기"
                        div_to_popup_contents.append(div_to_close_button)
                        div_to_popup_contents.append(div_to_terms_title)
                        div_to_popup_contents.append(div_to_terms_contents)
                        div_to_popup_container.append(div_to_popup_contents)
                        div_to_popup_layer.append(div_to_popup_container)
                        div_to_dim_layer.append(div_to_dim_background)
                        div_to_dim_layer.append(div_to_popup_layer)
                        base_html.append(div_to_dim_layer)

                        self._js_terms_trigger()

                        self.is_terms_to_add = True

                a_tag_to_terms_detail = base_html.new_tag('a', attrs=a_tag_to_terms_attr_option)
                a_tag_to_terms_detail.string = "[보기]"
                form_group.append(a_tag_to_terms_detail)

        if field_type in [8, 9]:
            return form_group, None
        elif field_type in [5]:
            return form_group, {
                'name': field_id,
                'type': field_info['type'],
                'target': f"""$('input[name="{field_id}"]:checked')""",
                'validation': list(field_info['validation'].keys())
            }
        else:
            return form_group, {
                'name': field_id,
                'type': field_info['type'],
                'target': f"""$('#{field_id}')""",
                'validation': list(field_info['validation'].keys())
            }

    def _video_box_generator(self, base_html, layout_info=None):
        """
        2019/08/25

        :param base_html:
        :param layout_info:

        autoplay: 자동 재생
        mute: 음소거
        loop: 영상 반복
        fs: 풀스크린
        disablekb: 키보드 컨트롤

        :return: iframe 태그
        """
        # TODO 비메오 추후 추가
        video_url = layout_info['video_url']
        iframe_tag = base_html.new_tag('iframe', attrs={
            'class': 'video-box',
            'src': f'https://www.youtube.com/embed/{video_url}',
            'allowfullscreen': 'allowfullscreen',
            'frameBorder': '0'})
        return iframe_tag

    def _body_generator(self, base_html):
        """
        2019/08/23
        :param base_html:

        object_type == 1 : 이미지 객체
        object_type == 2 : 폼 객체
        object_type == 3 : 비디오 객체
        """
        main_container = base_html.new_tag('main', attrs={'class': 'section-container'})
        base_html.body.append(main_container)

        for section_index, section in enumerate(self.section_info_list):  # 섹션 생성
            section_h = section[0]['section_h']
            self._css_section_height(section_id=section_index,
                                     section_h=section_h)
            landing_section = base_html.new_tag('section',
                                                attrs={'class': 'landing-section',
                                                       'data-section-id': section_index})
            main_container.append(landing_section)

            for object_index, section_object_info in enumerate(section):  # 객체 생성
                self._css_object_block_size(section_id=section_index,
                                            object_id=object_index,
                                            layout_info=section_object_info)
                section_object_block = base_html.new_tag('div', attrs={'class': 'landing-object-block',
                                                                       'data-object-id': object_index})
                landing_section.append(section_object_block)
                object_type = section_object_info['type']
                self._css_object_by_type_size(object_type=object_type,
                                              section_id=section_index,
                                              object_id=object_index,
                                              layout_info=section_object_info)
                if object_type == 1:
                    object_image_url = section_object_info['image_data']
                    section_object_by_type = base_html.new_tag('div', attrs={'class': 'object-type-image lazyload',
                                                                             'data-src': object_image_url})
                    section_object_block.append(section_object_by_type)

                elif object_type == 2:
                    form_group_id = section_object_info['form_group_id']
                    self._css_field_label_size(section_id=section_index,
                                               object_id=object_index,
                                               field_info_list=self.field_info_list,
                                               form_group_id=form_group_id)
                    section_object_by_type = base_html.new_tag('form', attrs={'class': 'object-type-form'})
                    section_object_block.append(section_object_by_type)
                    generated_field_list = [self._db_form_field_generator(base_html,
                                                                          section_id=section_index,
                                                                          object_id=object_index,
                                                                          object_w=section_object_info['position'][
                                                                              'w'],
                                                                          object_h=section_object_info['position'][
                                                                              'h'],
                                                                          field_id=field_index,
                                                                          field_info=field,
                                                                          field_position_set=next(
                                                                              item for item in
                                                                              section_object_info['fields']
                                                                              if item["sign"] == field['sign']))
                                            for field_index, field
                                            in enumerate(self.field_info_list)
                                            if int(field['form_group_id']) == int(form_group_id)]
                    item_group = []
                    for generated_field, item in generated_field_list:
                        section_object_by_type.append(generated_field)
                        if item is not None:
                            item_group.append(item)

                    self._js_submit_event(section_id=section_index,
                                          item_group=item_group)
                    self._js_validation(section_id=section_index)
                    self._js_call_ajax(section_id=section_index)

                elif object_type == 3:
                    section_object_by_type = base_html.new_tag('div', attrs={'class': 'object-type-video'})
                    iframe_tag = self._video_box_generator(base_html, layout_info=section_object_info)
                    section_object_by_type.append(iframe_tag)
                    section_object_block.append(section_object_by_type)

    def generate(self):
        base_html = _convert_to_html(self.default_html)
        try:
            self._body_generator(base_html)

            stylesheets = _convert_to_html(self._stylesheets_generate())
            base_html.head.append(stylesheets)

            header_script = _convert_to_html(
                self.landing_config['header_script'] if self.landing_config['header_script'] else "")
            base_html.head.append(header_script)

            if self.tnk_script_check:
                base_html.head.append(_convert_to_html(self._tnk_script()))

            if self.facebook_pixel_check:
                base_html.head.append(_convert_to_html(self._facebook_pixel_head()))
                base_html.body.append(_convert_to_html(self._facebook_pixel_body()))

            if self.kakao_pixel_check:
                base_html.head.append(_convert_to_html(self._kakao_pixel()))

            if self.google_display_network:
                base_html.head.append(_convert_to_html(self._google_display_network()))

            scripts = _convert_to_html(self._scripts_generate())
            base_html.body.append(scripts)

            body_script = _convert_to_html(
                self.landing_config['body_script'] if self.landing_config['body_script'] else "")
            base_html.body.append(body_script)

            if self.landing_config['is_hijack']:
                base_html.body.append(_convert_to_html(self._hijack()))

            return {'state': True, 'data': base_html.prettify(), 'message': 'Succeed.'}
        except Exception as e:
            return {'state': False, 'data': '', 'message': str(e)}
