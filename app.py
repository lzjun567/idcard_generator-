import io
import random
import base64

from flask import Flask, render_template, request, jsonify

from idcard_generator import id_card_utils, name_utils
from idcard_generator.web_generator import generate_id_card

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 最大上传 10MB


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/random', methods=['GET'])
def api_random():
    """随机生成一套身份证信息"""
    random_name_data = name_utils.random_name()
    year = random.randint(1960, 2005)
    month = random.randint(1, 12)
    day = id_card_utils.random_day(year, month)
    start_time = id_card_utils.get_start_time()
    expire_time = id_card_utils.get_expire_time()

    return jsonify({
        'name': random_name_data['name_full'],
        'sex': random_name_data['sex_text'],
        'nation': '汉',
        'year': str(year),
        'month': str(month),
        'day': str(day),
        'addr': '四川省成都市武侯区益州大道中段722号复城国际',
        'idn': id_card_utils.random_card_no(
            year=str(year), month=str(month), day=str(day)
        ),
        'org': '四川省成都市锦江分局',
        'life': f'{start_time}-{expire_time}',
    })


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """接收表单数据和头像，生成身份证图片，返回 base64 编码"""
    avatar_file = request.files.get('avatar')
    if not avatar_file or avatar_file.filename == '':
        return jsonify({'error': '请上传头像图片'}), 400

    data = {
        'name':  request.form.get('name', ''),
        'sex':   request.form.get('sex', ''),
        'nation': request.form.get('nation', ''),
        'year':  request.form.get('year', ''),
        'month': request.form.get('month', ''),
        'day':   request.form.get('day', ''),
        'addr':  request.form.get('addr', ''),
        'idn':   request.form.get('idn', ''),
        'org':   request.form.get('org', ''),
        'life':  request.form.get('life', ''),
    }
    use_matting = request.form.get('use_matting', 'true').lower() == 'true'

    try:
        color_img, bw_img = generate_id_card(data, avatar_file, use_matting=use_matting)
    except Exception as e:
        return jsonify({'error': f'生成失败：{str(e)}'}), 500

    # 转为 base64，直接在浏览器展示
    color_buf = io.BytesIO()
    color_img.save(color_buf, format='PNG')
    color_b64 = base64.b64encode(color_buf.getvalue()).decode()

    bw_buf = io.BytesIO()
    bw_img.save(bw_buf, format='PNG')
    bw_b64 = base64.b64encode(bw_buf.getvalue()).decode()

    return jsonify({
        'color': f'data:image/png;base64,{color_b64}',
        'bw':    f'data:image/png;base64,{bw_b64}',
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
