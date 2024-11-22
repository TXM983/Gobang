import pandas as pd
import re


def oracle_to_mysql_data_type(oracle_type):
    # 简单的 Oracle 到 MySQL 字段类型映射
    mapping = {
        'VARCHAR2': 'VARCHAR',
        'NUMBER': 'DECIMAL',
        'DATE': 'DATE',
        'CHAR': 'CHAR',
        'FLOAT': 'FLOAT',
        'BLOB': 'BLOB',
        'INTEGER': 'INT(11)'
        # 添加其他类型映射
    }
    # 匹配带有长度和标度的类型
    match = re.match(r'(\w+)(?:\s*\((\d+)(?:,\s*(\d+))?\))?', oracle_type.strip())
    if match:
        base_type = match.group(1).upper()
        length = match.group(2)  # 可选长度
        scale = match.group(3)  # 可选标度

        if base_type == 'NUMBER':
            if scale:  # 如果有标度
                return f"DECIMAL({length}, {scale})"
            elif length:  # 如果有长度但没有标度
                return f"DECIMAL({length})"  # 或者根据实际需要返回
            else:  # 如果没有长度和标度
                return "INT(11)"  # 转换为 INT

        mysql_type = mapping.get(base_type, base_type)  # 查找基础类型
        if scale:
            return f"{mysql_type}({length},{scale})"
        elif length:
            return f"{mysql_type}({length})"  # 返回带长度的类型
        return mysql_type  # 如果没有长度，返回基础类型

    # 对于没有长度的类型直接返回
    if oracle_type.upper() == 'NUMBER':
        return "INT"  # 没有长度和标度的 NUMBER 转为 INT

    return mapping.get(oracle_type.upper(), oracle_type)


def generate_create_table_sql_with_comments(file_path, sheet_name=None):
    # 读取Excel文件，表头在第二行
    xls = pd.ExcelFile(file_path)
    sheets = xls.sheet_names if not sheet_name else [sheet_name]

    sql_statements = []

    # 处理每个sheet
    for sheet in sheets:
        df = pd.read_excel(xls, sheet, header=1)  # 指定 header=1

        # 去除列名空格
        df.columns = df.columns.str.strip()

        # 打印列名以调试
        print(df.columns.tolist())
        print(df.head())  # 打印前几行以确认读取内容

        # 遍历不同的表名
        for table_name in df['表名称'].unique():
            table_df = df[df['表名称'] == table_name]
            table_description = table_df['表描述'].iloc[0]

            # 添加DROP TABLE语句
            drop_statement = f"DROP TABLE IF EXISTS `{table_name}`;"
            sql_statements.append(drop_statement)

            # SQL创建表的初始部分
            sql = f"CREATE TABLE {table_name} (\n"

            # 遍历字段
            for _, row in table_df.iterrows():
                column_name = row['字段英文名']  # 使用字段英文名
                oracle_data_type = row['字段类型']
                mysql_data_type = oracle_to_mysql_data_type(oracle_data_type)  # 转换类型
                column_comment = row['字段中文名']  # 使用字段中文名作为注释
                if any(keyword in column_comment for keyword in ["保额", "保费", "金额", "加费", "费用"]):
                    mysql_data_type = 'DECIMAL(16,2)'
                elif any(keyword in column_comment for keyword in ["比例"]):
                    mysql_data_type = 'DECIMAL(16,4)'
                if oracle_data_type == "TIMESTAMP" or column_name.upper() == "ID":
                    nullable = "NOT NULL"
                else:
                    nullable = "NULL" if row['能否为空'] == '' else "DEFAULT NULL"  # 假设空值为可空


                # 添加字段行
                sql += f"    {column_name} {mysql_data_type} {nullable} COMMENT '{column_comment}',\n"

            # 移除最后一个逗号，添加表注释
            sql = sql.rstrip(',\n') + f"\n) COMMENT '{table_description}';\n"
            sql_statements.append(sql)

    # 将所有表的SQL语句组合起来
    return "\n".join(sql_statements)


def save_sql_to_file(sql_output, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(sql_output)


# 示例使用
file_path = "D:\\DevelopSoftware\\svn\\i17doc\\04_项目实施_SS\\04_DSP咨询设计_ZX\\03_交付物_JF\\01-接口规范\\SS-MB-011_GF-I17_国富人寿_DSP组_数据平台接口规范设计_V0.7_20241025.xlsx"
sheet_name = "GRP_CALC_RESULT"  # 如果想处理指定sheet，填写sheet名称；不指定则处理所有sheet
output_file = "GRP_CALC_RESULT.sql"  # 输出文件名
sql_output_with_comments = generate_create_table_sql_with_comments(file_path, sheet_name)
save_sql_to_file(sql_output_with_comments, output_file)
# 输出或保存SQL
print(sql_output_with_comments)
# 如果要保存到文件中，可以使用下面这行
# with open
