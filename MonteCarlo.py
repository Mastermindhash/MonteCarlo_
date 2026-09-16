import numpy as np 


class Measurment:
    def __init__(self, value: float, uncertainty: float):
        self.value = value
        self.uncertainty = uncertainty



class MeasurementSerie:
    def __init__(self, content: list[Measurment]): 
        self.data = content 

    def mean(self) -> float:
        """return the mean of the Measurement """
        return sum(self.data)/len(self.data)

    def variance(self) -> float:
        """ return the variance of the Measurement """
        m = self.mean()
        return sum((x - m) ** 2 for x in self.data) / (len(self.data) - 1)

    def std_uncertainty(self) -> float:
        """ return the standard uncertainty of the Measurement  """
        return self.variance() ** 0.5

    def uncertainty_on_mean(self) -> float:
        """ return the uncertainty on the mean of the Measurement """
        return self.std_uncertainty() / (len(self.data) ** 0.5) 
        
    def to_measurment(self) -> Measurment :
        """ return a Measurement with mean as value and uncer...mean as uncertainty """
        mean = self.mean() 
        uncertainty_on_mean = self.uncertainty_on_mean() 
        return Measurment(mean, uncertainty_on_mean) 
            
        
class MonteCarloEstimator:
    def __init__(self, f, N: int, measurment_list: list[Measurment]) :
        self.measurments = measurment_list
        self.f = f
        self.N = N

    def estimator(self) -> float:
        """ return an estiamtion of the uncertainty on y based on the measurments """
        samples_by_variables = [np.random.uniform(m.value-m.uncertainty*np.sqrt(3), m.value+m.uncertainty*np.sqrt(3), self.N) for m in self.measurments]
        y_k = self.f(*samples_by_variables) 
        y_mean = np.mean(y_k)
        u_y= np.std(y_k, ddof=1) 
        return u_y  
