"""
预测的方法包括了综合增长率（CRG）、产业驱动法、经济测算法和资源承载力法
"""
class PopPredict:
    def __init__(
            self,
            planning_start_year: int,
            planning_end_year: int,
    ) -> None:
        self.planning_start_year = planning_start_year
        self.planning_end_year = planning_end_year

    @staticmethod
    def calculate_cgr(
            start_year: int,
            initial_population: int | float,
            end_year: int,
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
        if end_year <= start_year:
            raise ValueError("结束年份必须大于起始年份")
        
        years = end_year - start_year  # 通过年份差计算年数
        cgr = (final_population / initial_population) ** (1 / years) - 1
        return cgr
    
    def predict_population_by_cgr(
            self,
            initial_population: int | float,
            cgr: int | float,
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
        
        years = self.planning_end_year - self.planning_start_year
        predicted_population = initial_population * (1 + cgr) ** years
        return predicted_population


if __name__ == "__main__":
    pop_2035 = PopPredict(2021, 2035)
    start_year = 2010
    initial_population = 539.62
    end_year = 2020
    final_population = 550.37
    cgr = pop_2035.calculate_cgr(2010, 539.62, 2020, 550.37)
    result = pop_2035.predict_population_by_cgr(550.37, cgr)

    print(f"{start_year}~{end_year}年间的人口综合增长率为{round(cgr * 100, 2)}%")
    print(f"到{pop_2035.planning_end_year}人口预计将达到{int(result)}万人")