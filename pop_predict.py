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
    def __init__(
        self,
        init_year: int,
        end_year: int,
    ) -> None:
        """
        初始化人口预测器

        Args:
            init_year (int): 规划始期年份
            end_year (int): 规划末期年份
        """
        if end_year <= init_year:
                raise ValueError("end_year must bigger than init_year")
        self.init_year = init_year
        self.end_year = end_year

    
    @staticmethod
    def calculate_cgr(
            start_year: int,
            initial_population: int | float,
            final_year: int,
            final_population: int | float
        ) -> float:
        """
        通过年份数据计算人口综合增长率（CGR）
        
        Args:
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
            cgr: float
        ) -> float | int:
        """
        根据综合增长率方法预测规划末期人口

        Args:
        initial_population (int or float): 规划初期人口
        cgr(float): 综合增长率

        Return：
        int or float: 规划末期预测人口
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