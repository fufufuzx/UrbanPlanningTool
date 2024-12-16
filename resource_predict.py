
class ResourcePredict:
    # 规划中一些常用的常量参考值
    R_AREA_PER:int | float = 40 # 人均居住面积推荐常量，单位：平方米
    B_AREA_L_PER:int | float = 2 # 大型城市人均商业面积推荐常量，单位：平方米
    B_AREA_M_PER:int | float = 1.2 # 一般城市人均商业用地面积推荐常量，单位：平方米
    M_LABOR_AREA_PER:int | float = 0.12 # 劳动密集型产业园区人均工业用地推荐常量， 单位：平方米
    M_TECH_AREA_PER:int | float = 0.05 # 技术密集型产业园区人均工业用地推荐常量， 单位：平方米
    GRAIN_NEED_YEAR_PER:int | float = 400 # 人均每年消耗粮食，单位：千克
    WATER_NEED_YEAR_PER:int | float = 180 * 365 #人均每年消耗的居民生活用水，单位：L
    
    def __init__(self, predit_population: float) -> None:
        if predit_population <= 0:
            raise ValueError("predit_population must bigger than 0")
        self.predit_population = predit_population
    
    def water_per_y(self):
        result = self.predit_population * ResourcePredict.WATER_NEED_YEAR_PER
        return f"每年消耗的水资源为{result}L"
    
    def grain_per_y(self):
        result = self.predit_population * ResourcePredict.GRAIN_NEED_YEAR_PER
        return f"每年消耗的粮食为{result}千克"
    
    def r_area(self):
        result = self.predit_population * ResourcePredict.R_AREA_PER
        return f"规划居住用地面积推荐为{round(result / 10000, 2)}公顷"

if __name__ == "__main__":
    a = ResourcePredict(5560000)
    print(a.water_per_y())
    print(a.grain_per_y())
    print(a.r_area())
