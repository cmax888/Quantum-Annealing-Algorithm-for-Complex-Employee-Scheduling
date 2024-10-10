import os
import numpy as np
import pandas as pd

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

staff_data = pd.read_excel('test.xlsx',header=1,usecols=['组织名称','工号*','姓名','默认技能','人员约束参数*'])
staff_data['组织名称'] = staff_data['组织名称'].map({'米果车间': 0, '点心车间': 1, '卷心酥车间': 2}).fillna(3).astype(int)
staff_data['技能id'] = staff_data['默认技能'].map({'大包段普通作业': 0, '码箱岗': 1, '机包段技术作业': 2, '卧式包装机操作': 3, '机包段普通作业': 4,
                                                  '生产段技术作业': 5, '立式包装机操作': 6, '装箱': 7, '机包段挑选': 8, '烤炉操作': 9,
                                                  '配打料操作': 10, '饼点注馅机开机': 11}).fillna(12).astype(int)
staff_data['班时'] = staff_data['人员约束参数*'].map({'白班': 0, '晚班': 1}).fillna(2).astype(int)

staff_data['员工编号'] = range(len(staff_data))
matrix1 = pd.crosstab(staff_data['员工编号'], staff_data['组织名称'])
binary_matrix1 = (matrix1 > 0).astype(int)
numpy_matrix1 = (1-binary_matrix1).to_numpy()  # 员工与车间的对应矩阵

matrix3 = pd.crosstab(staff_data['员工编号'], staff_data['技能id'])
binary_matrix3 = (matrix3 > 0).astype(int)
numpy_matrix3 = (1-binary_matrix3).to_numpy()  # 员工与拥有技能的对应矩阵

matrix4 = pd.crosstab(staff_data['员工编号'], staff_data['班时'])
crosstab = pd.DataFrame(matrix4)
crosstab.loc[crosstab[2] == 1, [0, 1]] = 1
crosstab = crosstab.drop(columns=[2])
cross_r = pd.concat([crosstab] * 6, axis=1)
cross_r.columns = range(12)
numpy_matrix4 = (1-cross_r).to_numpy()  # 员工与上白班还是夜班的对应矩阵
print(numpy_matrix4[20:25])

w_data = []
filenames = ['米果岗位需求.xlsx', '点心岗位需求.xlsx', '卷心酥岗位需求.xlsx']
for file in filenames:
    df = pd.read_excel(file,usecols=['车间名称','产线名称','岗位名称','技能名称','标准人数'])
    w_data.append(df)
work_data = pd.concat(w_data, ignore_index=True)
work_data['技能id'], unique = pd.factorize(work_data['技能名称'])
work_data['岗位编号'] = range(len(work_data))
# dx_data = pd.read_excel('点心岗位需求.xlsx',header=0,usecols=['车间名称','产线名称','岗位名称','技能名称','标准人数'])
# dx_data['标准人数'] = (dx_data['标准人数']*10)
# jxs_data = pd.read_excel('米果岗位需求.xlsx',header=0,usecols=['车间名称','产线名称','岗位名称','技能名称','标准人数'])
# jxs_data['标准人数'] = (jxs_data['标准人数']*12)
# mg_data = pd.read_excel('卷心酥岗位需求.xlsx',header=0,usecols=['车间名称','产线名称','岗位名称','技能名称','标准人数'])
# mg_data['标准人数'] =(mg_data['标准人数']*12)
# print(work_data.head(51))
matrix2 = pd.crosstab(work_data['岗位编号'], work_data['技能id'])
binary_matrix2 = (matrix2 > 0).astype(int)
binary_matrix2['12'] = 0
numpy_matrix2 = binary_matrix2.to_numpy()   # 岗位与需求技能的对应矩阵
# print(binary_matrix2)
