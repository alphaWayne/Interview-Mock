import sqlite3,datetime,uuid
# 创建数据库连接
def create_connection(database):
    '''
    : param database: 所要用的数据库
    : return: 返回数据库连接
    目前已有的数据库有:
    - userDatabase 用户数据库
    - fileDatabase 文件数据库
    - chatDatabase 聊天数据库
    '''
    conn = sqlite3.connect('app/Database/{}.db'.format(database))
    cursor = conn.cursor()
    return conn, cursor

def create_dict_cursor(database):
    '''
    : param database: 所要用的数据库
    : return: 返回数据库连接
    目前已有的数据库有:
    - userDatabase 用户数据库
    - fileDatabase 文件数据库
    - chatDatabase 聊天数据库
    '''
    conn = sqlite3.connect('app/Database/{}.db'.format(database))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn, cursor

# 创建表
def create_table(database,SQL_CREATE_TABLE):
    '''
    : param database: 所要用的数据库
    : param SQL_CREATE_TABLE: 创建表的SQL语句
    '''
    conn, cursor = create_connection(database)
    cursor.execute(SQL_CREATE_TABLE)
    conn.commit()
    conn.close()

# 注册用户
def register_user(username, password_hash, email):
    '''
    : param username: 用户名
    : param password_hash: 密码哈希值
    : param email: 电子邮件地址
    该函数用于注册用户
    '''
    user_id = str(uuid.uuid4())  # 生成新的UUID
    conn, cursor = create_connection('userDatabase')
    cursor.execute('''
    INSERT INTO users (_id,username, password_hash, email) VALUES (?,?, ?, ?)
    ''', (user_id,username, password_hash, email))
    conn.commit()
    conn.close()

# 描述表信息
def pragma_table_info(database,table_name):
    '''
    : param database: 所要用的数据库
    : param table_name: 所要查看的表名
    该函数会输出该表的所有列信息
    '''
    conn, cursor = create_connection(database)
    cursor.execute('PRAGMA table_info({})'.format(table_name))
    info = cursor.fetchall()
    for column in info:
        print(column)
    conn.close()

# 查看表行数
def count_table_rows(database,table_name):
    '''
    : param database: 所要用的数据库
    : param table_name: 所要查看的表名
    该函数会返回该表的行数
    '''
    conn, cursor = create_connection(database)
    cursor.execute('SELECT COUNT(*) FROM {}'.format(table_name))
    count = cursor.fetchall()
    conn.close()
    return count

# 查看验证码是否正确
def check_captcha(receiver, captcha_code, purpose):
    '''
    : param receiver: 验证码接收者
    : param captcha_code: 验证码
    : param purpose: 验证码用途
    该函数会返回该验证码是否正确
    '''
    conn, cursor = create_connection('userDatabase')
    cursor.execute('''
    SELECT captcha_code FROM captcha WHERE receiver = ? AND purpose = ?
    ''', (receiver, purpose))
    captcha = cursor.fetchone()
    conn.close()
    if captcha:
        return captcha[0] == captcha_code
    return False

# 查看该用户的验证码是否过期
def check_captcha_expiration(receiver, purpose):
    '''
    : param receiver: 验证码接收者
    : param purpose: 验证码用途
    该函数会返回该验证码是否过期
    '''
    conn, cursor = create_connection('userDatabase')
    cursor.execute('''
    SELECT expiration_time FROM captcha WHERE receiver = ? AND purpose = ?
    ''', (receiver, purpose))
    captcha = cursor.fetchone()
    conn.close()
    if captcha:
        print(captcha[0])
        expiration_time = datetime.datetime.strptime(captcha[0], '%Y-%m-%d %H:%M:%S.%f')  # 确保转换为datetime对象
        return expiration_time > datetime.datetime.now()
    return False

# 插入或更新验证码
def insert_or_update_captcha(receiver, purpose, captcha_code, send_time):
    '''
    :param receiver: 验证码接收者
    :param purpose: 验证码用途
    :param captcha_code: 验证码
    :param send_time: 发送时间
    '''
    expiration_time = send_time + datetime.timedelta(minutes=5)  # 验证码有效期为5分钟
    captcha_id = str(uuid.uuid4())  # 生成新的UUID
    conn = None
    try:
        conn, cursor = create_connection('userDatabase')
        # 使用 ON CONFLICT DO UPDATE 语法来处理冲突
        cursor.execute('''
        INSERT INTO captcha (id, receiver, captcha_code, purpose, send_time, expiration_time)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            receiver=excluded.receiver,
            captcha_code=excluded.captcha_code,
            purpose=excluded.purpose,
            send_time=excluded.send_time,
            expiration_time=excluded.expiration_time
        ''', (captcha_id, receiver, captcha_code, purpose, send_time, expiration_time))
        
        conn.commit()
    finally:
        if conn:
            conn.close()

#查询一条数据
def query_data(database,SQL_QUERY):
    '''
    : param database: 所要用的数据库
    : param SQL_QUERY: 查询数据的SQL语句
    该函数会返回查询的数据
    '''
    conn, cursor = create_connection(database)
    cursor.execute(SQL_QUERY)
    data = cursor.fetchall()
    conn.close()
    return data

# 查询全量数据方法
def query_data_all(database,SQL_QUERY):
    '''
    : param database: 所要用的数据库
    : param SQL_QUERY: 查询数据的SQL语句
    该函数会返回查询的数据
    '''
    conn, cursor = create_connection(database)
    cursor.execute(SQL_QUERY)
    data = cursor.fetchall()
    conn.close()
    return data

# 使用id删除数据
def delete_data_by_id(database,table_name,id):
    '''
    : param database: 所要用的数据库
    : param table_name: 所要删除的表名
    : param id: 所要删除的id
    该函数会删除指定id的数据
    '''
    conn, cursor = create_connection(database)
    cursor.execute('DELETE FROM {} WHERE id = ?'.format(table_name), (id,))
    conn.commit()
    conn.close()

# 使用SQL语句删除数据
def delete_data_by_sql(database,SQL_DELETE):
    '''
    : param database: 所要用的数据库
    : param SQL_DELETE: 删除数据的SQL语句
    该函数会删除指定SQL语句的数据
    '''
    conn, cursor = create_connection(database)
    cursor.execute(SQL_DELETE)
    conn.commit()
    conn.close()

# 添加索引
def alter_table_add_index(database, table_name, column_name):
    '''
    : param database: 所要用的数据库
    : param table_name: 表名
    : param column_name: 列名
    该函数会为指定表的指定列添加索引
    '''
    conn, cursor = create_connection(database)
    cursor.execute(f'CREATE INDEX IF NOT EXISTS {table_name}_{column_name}_idx ON {table_name} ({column_name})')

# 列名重命名
def rename_column(database, table_name, old_column_name, new_column_name):
    '''
    : param database: 所要用的数据库
    : param table_name: 表名
    : param old_column_name: 旧列名
    : param new_column_name: 新列名
    该函数会为指定表的指定列重命名
    '''
    conn, cursor = create_connection(database)
    cursor.execute(f'ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}')

if __name__ == '__main__':
    # 创建users表
    SQL_CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        _id TEXT PRIMARY KEY, -- 用户ID，主键
        username TEXT NOT NULL UNIQUE,         -- 用户名，唯一标识用户
        password_hash TEXT NOT NULL,            -- 密码哈希值，不存储明文密码
        email TEXT NOT NULL UNIQUE,             -- 电子邮件地址，用于登录和通信
        full_name TEXT,                         -- 完整名字
        gender TEXT,                            -- 性别
        date_of_birth DATE,                     -- 出生日期
        phone_number TEXT,                      -- 联系电话
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 创建时间戳，默认为当前时间
        last_login DATETIME,                     -- 最后一次登录时间
        avatar_url TEXT                         -- 头像URL
    );
    '''

    # 创建captcha表
    SQL_CREATE_CAPTCHA_TABLE = '''
    CREATE TABLE IF NOT EXISTS captcha (
        id TEXT PRIMARY KEY, -- 主键
        receiver TEXT NOT NULL,               -- 接收验证码的用户标识（如邮箱）
        captcha_code TEXT NOT NULL,           -- 验证码本身
        purpose TEXT NOT NULL,                -- 验证码的用途，比如 'register', 'reset_password'
        send_time DATETIME DEFAULT CURRENT_TIMESTAMP, -- 发送验证码的时间，默认为当前时间
        expiration_time DATETIME NOT NULL      -- 验证码过期时间，可以由send_time + 5 minutes 计算得出
    );
    '''
    #清空数据库
    # conn, cursor = create_connection('userDatabase')
    # cursor.execute('DROP TABLE IF EXISTS users')
    # cursor.execute('DROP TABLE IF EXISTS captcha')
    # create_table('userDatabase',SQL_CREATE_CAPTCHA_TABLE)
    # create_table('userDatabase',SQL_CREATE_USERS_TABLE)
    # print(count_table_rows('userDatabase','captcha'))
    print(query_data('userDatabase','SELECT * FROM captcha'))
    print(query_data('userDatabase','SELECT * FROM users'))
    # conn.close()
    # delete_data_by_id('userDatabase','captcha','3')
    # pragma_table_info('userDatabase','users')