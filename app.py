# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import get_db_connection
import pymysql

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# ==================== 学生管理API ====================

@app.route('/api/students', methods=['GET'])
def get_students():
    """获取所有学生列表"""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM students ORDER BY id DESC')
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'data': students})

@app.route('/api/students', methods=['POST'])
def add_student():
    """添加学生"""
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO students 
             (student_no, name, gender, birthday, class_name, phone, address) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (
        data['student_no'], data['name'], data['gender'],
        data.get('birthday'), data.get('class_name', ''),
        data.get('phone', ''), data.get('address', '')
    ))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'message': '添加成功', 'id': new_id})

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """删除学生"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id=%s', (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'message': '删除成功'})

# ==================== 教师管理API ====================

@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    """获取所有教师列表"""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM teachers ORDER BY id DESC')
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'data': teachers})

@app.route('/api/teachers', methods=['POST'])
def add_teacher():
    """添加教师"""
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO teachers 
             (teacher_no, name, gender, department, title, phone, email) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (
        data['teacher_no'], data['name'], data['gender'],
        data.get('department', ''), data.get('title', ''),
        data.get('phone', ''), data.get('email', '')
    ))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'message': '添加成功', 'id': new_id})

@app.route('/api/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """删除教师"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM teachers WHERE id=%s', (teacher_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'message': '删除成功'})

# ==================== 课表管理API ====================

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    """获取所有排课（含关联信息）"""
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT s.*, 
               stu.name as student_name, 
               t.name as teacher_name,
               c.course_name
        FROM schedules s
        LEFT JOIN students stu ON s.student_id = stu.id
        LEFT JOIN teachers t ON s.teacher_id = t.id
        LEFT JOIN courses c ON s.course_id = c.id
        ORDER BY s.id DESC
    """)
    schedules = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'data': schedules})

@app.route('/api/schedules', methods=['POST'])
def add_schedule():
    """添加排课"""
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO schedules 
             (student_id, teacher_id, course_id, semester, classroom) 
             VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(sql, (
        data['student_id'], data['teacher_id'], data['course_id'],
        data['semester'], data.get('classroom', '')
    ))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'message': '添加成功', 'id': new_id})

@app.route('/api/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    """删除排课"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM schedules WHERE id=%s', (schedule_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'code': 200, 'message': '删除成功'})

# ==================== 启动服务器 ====================

@app.route('/')
def index():
    """访问根路径时返回前端页面"""
    from flask import send_from_directory
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)