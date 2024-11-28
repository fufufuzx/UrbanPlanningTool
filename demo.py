import math
import pandas as pd
import xlrd

pi = 3.14159265358979324;
a = 6378245.0;
ee = 0.00669342162296594323;
x_pi = 3.14159265358979324 * 3000.0 / 180.0;

def transformLat(x,y):

    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * pi) + 320 * math.sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret

 
def transformLon(x,y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret
 
'''
     * 地球坐标转换为火星坐标
     *
     * @param wgLat  地球坐标
     * @param wgLon
     *
     * mglat,mglon 火星坐标
'''
def transform2Mars(wgLat,wgLon):
        dLat = transformLat(wgLon - 105.0, wgLat - 35.0);
        dLon = transformLon(wgLon - 105.0, wgLat - 35.0);
        radLat = wgLat / 180.0 * pi;
        magic = math.sin(radLat);
        magic = 1 - ee * magic * magic;
        sqrtMagic = math.sqrt(magic);
        dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi);
        dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * pi);
        mgLat = wgLat + dLat;
        mgLon = wgLon + dLon;
        return mgLat,mgLon

'''
     * 百度转火星
     * @param bd_lat
     * @param bd_lon
'''     
def bd_decrypt(bd_lat,bd_lon):
    
        x = bd_lon - 0.0065
        y = bd_lat - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi);
        gg_lon = z * math.cos(theta);
        gg_lat = z * math.sin(theta);
        return gg_lat,gg_lon
    

# 读取Excel并进行转换
def convert_bd_to_gcj(input_excel_path, output_excel_path):
    try:
        # 读取Excel文件
        df = pd.read_excel(input_excel_path, engine="xlrd")

        print('成功')

        # 检查列名是否存在
        if '纬度' not in df.columns or '经度' not in df.columns:
            raise ValueError("输入的Excel表格中缺少 '纬度' 或 '经度' 列")
            print("成功")

        # 批量转换百度坐标为火星坐标
        df[['gcj_lat', 'gcj_lon']] = df.apply(lambda row: pd.Series(bd_decrypt(row['纬度'], row['经度'])), axis=1)

        print(df[['gcj_lat', 'gcj_lon']])

        # 保存转换后的DataFrame为新的Excel文件
        df.to_excel(output_excel_path, index=False)

        print(f"转换完成，结果已保存为: {output_excel_path}")

    except Exception as e:
        print(f"转换过程中出错: {e}")

if __name__ == '__main__':
    # 正确设置路径，避免路径拼接错误
    input_excel_path = r'\xx\xx\xxxx.xlsx'  # 输入Excel文件的路径
    output_excel_path = r'\xx\xx\xxxx2.xlsx.xlsx'  # 输出Excel文件的路径

    # 调用函数进行转换
    convert_bd_to_gcj(input_excel_path, output_excel_path)
    

