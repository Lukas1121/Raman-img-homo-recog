import numpy as np
from bin import image_treatment

path_hery = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Visible"
path_PEA = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\data\PEA\img"
path_hery_tirf = "C:\\Users\lukas\PycharmProjects\Raman-img-homo-recog\Raman\Herys Tirf"

kernel = np.array([[-1,-1,-1],
                  [-1, 9,-1],
                  [-1,-1,-1]])

sharpen_kernel = np.array([[0,-1,0],
                           [-1,5,-1],
                           [0,-1,0]])


obj = image_treatment.Main(path=path_hery_tirf)

# obj.custom_kernel_processing(kernel=sharpen_kernel,
#                              img=3,
#                              save_plot=False)

obj.N_custom_kernal_processing(kernel1=kernel,
                               kernel2=sharpen_kernel,
                               img=7)