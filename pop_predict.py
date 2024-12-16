"""
预测的方法包括了综合增长率（CRG）、产业驱动法、经济测算法和资源承载力法
"""

"""
居住用地相关常量（参考值）
人均居住建筑面积：在中国，不同城市和地区会有不同的差异
一般城市人均居住面积：30-40平方米
定义一下这个常量：RES_AREA_PER = 40

耕地相关常量（参考值）
* 世界人均耕地面积（近似值）：
    * 目前世界人均耕地面积为0.2公顷，这一数据可以作为衡量全球耕地资源紧张的一个宏观常量。
    * 中国的人均耕地面积为0.09公顷
* 主要粮食作物的平均产量（参考）：
    * 水稻：在中国较好的种植条件下，每亩每年产量可达500-700千克
    * 小麦：每亩产量每年一般在300-500千克
    * 按照每人每年消费粮食400千克，一亩水稻田（产量按照600千克计算）产出的粮食理论可以养活1.5人    
工业用地相关常量（参考值）
* 部分产业的单位用地面积就业人数（参考）：
    * 劳动密集型产业：如服装制造业，每公顷工业用地可容纳就业人口在800-1200人
    * 技术密集型产业：电子芯片制造业，每公顷工业用地可容纳就业人口在200-500人
    * 这些数据可以作为规划产业园区时，根据预期就业人口确定工业用地规模的参考常量。
商业用地相关常量（参考值）
* 人均商业建筑面积（参考范围）：
    * 大城市的核心商业区，人均商业建筑面积可以达到1-2平方米
    * 一般城市的普通商业区，人均商业建筑面积可以达到0.8-1.2平方米
水资源消耗相关常量
* 居民生活用水：定额一般在110-180L每人每天，其中南方城市一般在150-180L/（人·d），而北方城市一般在110L-130L/（人·d）
* 工业用水人均耗水量：
* 农业用水人均耗水量：

日照间距
"""


GRAIN_PER_MU = 600 # 主要粮食每亩的年产量，单位：千克
INDUSTRIAL_LAND_PER_HECTARE_EMPLOYMENT_LABOR = 1200 # 劳动密集型每公顷产业用地可容纳就业人口
INDUSTRIAL_LAND_PER_HECTARE_EMPLOYMENT_TECH = 500 # 技术密集型每公顷产业用地可容纳就业人口

R_AREA_PER:int | float = 40 # 人均居住面积推荐常量，单位：平方米
B_AREA_L_PER:int | float = 2 # 大型城市人均商业面积推荐常量，单位：平方米
B_AREA_M_PER:int | float = 1.2 # 一般城市人均商业用地面积推荐常量，单位：平方米
M_LABOR_AREA_PER:int | float = 0.12 # 劳动密集型产业园区人均工业用地推荐常量， 单位：平方米
M_TECH_AREA_PER:int | float = 0.05 # 技术密集型产业园区人均工业用地推荐常量， 单位：平方米
GRAIN_NEED_YEAR_PER:int | float = 400 # 人均每年消耗粮食，单位：千克
WATER_NEED_YEAR_PER:int | float = 180 * 365 #人均每年消耗的居民生活用水，单位：L


class PopPredict:
    def __init__(self, init_year: int, end_year: int, method: str) -> None:
        self.init_year = init_year
        self.end_year = end_year
        self.method = method

    @classmethod
    def by_cgr(cls, ):
        ...
    
    @staticmethod
    def calculate_cgr(
            start_year: int,
            initial_population: int | float,
            final_year: int,
            final_population: int | float
        ) -> float:
        """
        通过年份数据计算人口综合增长率（CGR）
        
        参数：
        initial_population (int or float): 初始人口
        final_population (int or float): 最终人口
        start_year (int): 起始年份
        end_year (int): 结束年份
        
        返回：
        float: 人口综合增长率
        """
        if initial_population <= 0 or final_population <= 0:
            raise ValueError("人口必须大于零")
        if final_year <= start_year:
            raise ValueError("结束年份必须大于起始年份")
        
        years = final_year - start_year  # 通过年份差计算年数
        cgr = (final_population / initial_population) ** (1 / years) - 1
        return cgr
    
    def predict_by_cgr(
            self,
            initial_population: int | float,
        ) -> float | int:
        """
        根据综合增长率方法预测规划末期人口

        参数：
        initial_population (int or float): 规划初期人口

        返回：
        float: 规划末期预测人口
        """
        if initial_population <= 0:
            raise ValueError("初始人口必须大于零")
        
        years = self.end_year - self.init_year
        predicted_population = initial_population * (1 + self.growth_rate) ** years
        return predicted_population


if __name__ == "__main__":
    cgr = PopPredict.calculate_cgr(2010, 539.62, 2020, 550.37)
    # cgr = 0.008
    pop_2035 = PopPredict(2020, 2035, cgr)
    result = pop_2035.predict_by_cgr(550.37)
    
    print(f"2010~2020年间的人口综合增长率为{round(cgr * 100, 2)}%")
    print(f"到{pop_2035.end_year}人口预计将达到{int(result)}万人")
    print(f"需要提供{round(result * GRAIN_NEED_YEAR_PER, 2)}千克的粮食才能养活这个城市")
    print(f"需要提供{round(result * GRAIN_NEED_YEAR_PER / 600, 2)}亩的耕地才能养活这个城市")