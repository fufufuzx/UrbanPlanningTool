"""
地理坐标转换算工具
"""
import math
from typing import Any, Literal
import pandas as pd

pi: float = 3.14159265358979324;
a: float = 6378245.0;
ee: float = 0.00669342162296594323;
x_pi: float = 3.14159265358979324 * 3000.0 / 180.0;

def transformLat(x: float, y: float) -> float:
    """
    * 纬度
    """
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * pi) + 320 * math.sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformLon(x: float, y: float) -> Any:
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret

def transform2Mars(wgLat,wgLon):
    '''
     * 地球坐标转换为火星坐标
     *
     * @param wgLat  地球坐标
     * @param wgLon
     *
     * mglat,mglon 火星坐标
    '''
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

def bd_decrypt(bd_lat: float, bd_lon: float) -> tuple[float, float]:
    '''
    * 百度转火星
    * @param bd_lat 百度坐标的纬度
    * @param bd_lon 百度坐标的经度
    '''
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi);
    gg_lon = z * math.cos(theta);
    gg_lat = z * math.sin(theta);
    return gg_lat,gg_lon

def mars_conv_wgs():
    '''
    * 火星转wgs84
    * @param mars_lat 百度坐标的纬度
    * @param mars_lon 百度坐标的经度
    '''
    ...

# 读取Excel并进行转换
def convert_bd_to_gcj(input_excel_path, output_excel_path) -> Any:
    try:
        # 读取Excel文件
        df = pd.read_excel(input_excel_path, engine="xlrd")

        # 检查列名是否存在
        if '纬度' not in df.columns or '经度' not in df.columns:
            raise ValueError("输入的Excel表格中缺少 '纬度' 或 '经度' 列")

        # 批量转换百度坐标为火星坐标
        df[['gcj_lat', 'gcj_lon']] = df.apply(lambda row: pd.Series(bd_decrypt(row['纬度'], row['经度'])), axis=1)

        # 保存转换后的DataFrame为新的Excel文件
        df.to_excel(output_excel_path, index=False)

        print(f"转换完成，结果已保存为: {output_excel_path}")

    except Exception as e:
        print(f"转换过程中出错: {e}")

if __name__ == '__main__':
    # 正确设置路径，避免路径拼接错误
    input_excel_path = r''  # 输入Excel文件的路径
    output_excel_path = r''  # 输出Excel文件的路径

    # 调用函数进行转换
    convert_bd_to_gcj(input_excel_path, output_excel_path)
