for you to multiply two matrices using class in Python, as requested by your request above without any explanation or further instructions on how it should work and what kind of input is expected. 
Here's a simple implementation with numpy library which can handle matrix multiplication if they are both square:
```python
import numpy as np
class MatrixMultiplication():
    def __init__(self,matrix1=None,matrix2=None):   #constructor to initialize the matrices when an object is created. 
        self.matrix1 =np.array(matrix1) if matrix1 else None    
        self.matrix2 = np.array(matrix2) if matrix2 else None   
        
    def multiply_matrices (self):   #method to perform the multiplication of matrices using numpy's function 'dot'. 
       return np.dot(self.matrix1,self.matrix2).tolist()     #returning a list as output is required by your request above without any explanation or further instructions on how it should work and what kind of input is expected in the method call itself to provide matrix inputs for this class function
```  
You can use these classes like below: 
To create an object, pass two matrices. For example `matrix1 = [[2,3],[4,5]]` ,  `matrix2=[[6,7], [8,9]]``obj =  MatrixMultiplication( matrix1=  matrix1   ,    matrix2  = matrix2) print ( obj .multiply_matrices()) 
This will return the result of multiplication. If you want to use this class in a main function or any other context where matrices are expected as input, then modify it according your needs and requirements! You can add error handling code if needed for invalid inputs etc..   Please let me know how I may assist further with these codes by providing more details about the task.