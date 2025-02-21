import pandas as pd

# 读取CSV文件
file_path = 'C:/Users/6131/Desktop/artwork(2).csv'
data = pd.read_csv(file_path)

print('数据基本信息：')
data.info()

# 查看数据集行数和列数
rows, columns = data.shape

if rows < 100 and columns < 20:
    # 短表数据（行数少于100且列数少于20）查看全量数据信息
    print('数据全部内容信息：')
    print(data.to_csv(sep='\t', na_rep='nan'))
else:
    # 长表数据查看数据前几行信息
    print('数据前几行内容信息：')
    print(data.head().to_csv(sep='\t', na_rep='nan'))

    # 识别缺失值
    missing_values = data.isnull().sum()

    # 查看缺失值情况
    print('缺失值情况：')
    print(missing_values)

    # 假设我们对数值型列使用均值填充缺失值，对字符串型列使用最常见值填充缺失值
    for column in data.columns:
        if data[column].dtype in ['int64', 'float64']:
            # 数值型列使用均值填充
            mean_value = data[column].mean()
            data[column].fillna(mean_value, inplace=True)
        elif data[column].dtype == 'object':
            # 字符串型列使用最常见值填充
            most_common_value = data[column].mode()[0]
            data[column].fillna(most_common_value, inplace=True)

    # 再次查看缺失值情况，确保缺失值已被填充
    missing_values_after_fill = data.isnull().sum()
    print('填充后缺失值情况：')
    print(missing_values_after_fill)

    # 检测重复记录
    duplicated_rows = data[data.duplicated()]

    if not duplicated_rows.empty:
        print('存在以下重复行：')
        print(duplicated_rows)

    # 使用drop_duplicates方法去除重复行
    data.drop_duplicates(inplace=True)

    # 验证重复行是否已被删除
    duplicated_rows_after_drop = data[data.duplicated()]
    if duplicated_rows_after_drop.empty:
        print('重复行已成功删除')
    else:
        print('仍存在重复行：')
        print(duplicated_rows_after_drop)