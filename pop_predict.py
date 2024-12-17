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

class PredictByCgr:    
    def calc(self, init_year:int, init_pop:float, cgr:float, final_year:int) -> float:
        """规划期人口预测

        Args:
            init_year (int): 规划始期年份
            init_pop (float): 规划始期人口
            cgr (float): 综合增长率
            final_year (int): 规划末期年份

        Returns:
            float: final_pop规划末期人口
        """
        if init_year > final_year:
            raise ValueError("final_year must bigger than init_year")
        if init_pop <= 0:
            raise ValueError("init_pop must bigger than 0")
        
        years = final_year - init_year
        final_pop = init_pop * (1 + cgr) ** years
        return final_pop

    @staticmethod
    def calc_cgr(init_year:int, init_pop:float, final_year:int, final_pop:float) -> float:
        """
        综合增长率计算

        Args:
            init_year (int): 始期年份
            init_pop (float): 始期人口
            final_year (int): 末期年份
            final_pop (float): 末期人口

        Returns:
            float: cgr综合增长率
        """
        if init_year > final_year:
            raise ValueError("final_year must bigger than init_year")
        if init_pop <= 0 or final_pop <= 0:
            raise ValueError("init_pop and final_pop must bigger than 0")
        
        years = final_year - init_year
        cgr = (final_pop / init_pop) ** (1 / years) - 1
        return cgr

class PredictByResArea:
    def __init__(self) -> None:
        pass

class PopPredict:
    def __init__(self):
        self.method = PredictByCgr()
    
    def calc(self):
        return self.method.calc



if __name__ == "__main__":
    # cgr = PopPredict.calculate_cgr(2010, 539.62, 2020, 550.37)
    # # cgr = 0.008
    # pop_2035 = PopPredict(2020, 2035, cgr)
    # result = pop_2035.predict_by_cgr(550.37)
    
    # print(f"2010~2020年间的人口综合增长率为{round(cgr * 100, 2)}%")
    # print(f"到{pop_2035.end_year}人口预计将达到{int(result)}万人")
    # print(f"需要提供{round(result * GRAIN_NEED_YEAR_PER, 2)}千克的粮食才能养活这个城市")
    # print(f"需要提供{round(result * GRAIN_NEED_YEAR_PER / 600, 2)}亩的耕地才能养活这个城市")

    a = PredictByCgr.calc_cgr(2010, 539.62, 2020, 550.37)
    print(a)

    b = PredictByCgr()
    result = b.calc(2020, 550.37, 0.008, 2035)
    print(result)

