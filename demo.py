"""
地理坐标转换算工具
"""
import math
from typing import Any, Literal
import pandas as pd

# 定义椭圆模型
PI: float = 3.14159265358979324
a: float = 6378245.0
ee: float = 0.00669342162296594323
x_pi: float = 3.14159265358979324 * 3000.0 / 180.0

# 检查坐标是否在中国境内
def outOfChina(
        lng: float,
        lat: float
    ) -> str:
    return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)

def transformLat(
        x: float,
        y: float
    ) -> float:
    """
    * 输入纬度
    """
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
    return ret


def transformLon(x: float, y: float) -> Any:
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    return ret

def transform2Mars(wgs84_lat: float, wgs84_lon: float):
    '''
     * 地理坐标转换
     * wgs84坐标转换为火星坐标
     * @param wgs84纬度坐标
     * @param wgs84经度坐标
     *
     * gcj02_lat,gcj02_lon 高德火星地理坐标
    '''
    dLat = transformLat(wgs84_lon - 105.0, wgs84_lat - 35.0)
    dLon = transformLon(wgs84_lon - 105.0, wgs84_lat - 35.0)
    radLat = wgs84_lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI)
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI)
    gcj02_lat = wgs84_lat + dLat
    gcj02_lon = wgs84_lon + dLon
    return gcj02_lat, gcj02_lon

def bd_decrypt(bd_lat: float, bd_lon: float) -> tuple[float, float]:
    '''
    * 百度转火星
    * @param bd_lat 百度坐标的纬度
    * @param bd_lon 百度坐标的经度
    '''
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lon = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
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
    input_path: str = r'any'  # 输入Excel文件的路径
    output_path: str = r'any'  # 输出Excel文件的路径

    # 调用函数进行转换
    convert_bd_to_gcj(input_path, output_path)
