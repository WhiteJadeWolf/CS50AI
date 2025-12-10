Hello CS50, Shuvrangshu this side and this is my documentation for "project_traffic" which implements image preprocessing as well as modeling and training a convolutional neural network on a given dataset to categorize 43 different traffic signs.
---

Putting forth the stuff I learnt and implemented in this project :--

1. Using os.path.join() function or os.sep string constant to ensure the functions are platform-independent as different operating systems use different characters to separate path components.
Implemented os.path.join() function for this project.

2. Using OpenCV to read and refine the images so that they are consistent.
Learnt about cv2.imread() function which is used to read images. Its return type is already a numpy ndarray.
Learnt about cv2.resize() function.
Learnt about the cv2.cvtColor(img, cv2.COLOR_BGR2RGB) function to convert BGR channels into RGB channels.
Implemented the same functions in code.

3. Learnt about os.listdir() function which is used to list files and folders in folder given as argument or current dir (implicit). 
Implemented the same function in code.

3. Learnt about os.path.isdir() function to identify folders.

4. Learnt about Data Normalization. Neural Networks train better if inputs are around 0-1.
In almost all common image formats (JPG, PNG, PPM, BMP…), each pixel channel is stored as an 8-bit integer (0-255) in 3 channels (for color image). We need to Normalize this to bring it in the range of 0-1 for ease in processing by neural network. So we use image.astype("float32") / 255.0 , which converts each integer into float and divides by 255.0 to bring it in the range of 0-1. Numpy ndarray helps with this as it broadcasts the process over the entire array so every integer is processed in the same way.

5. Learnt about BatchNormalization which normalizes activation inside the network. It makes the training faster and more stable, improving accuracy but adds very little computation cost. In context of this project, it smoothes out activation flows, reduces overfitting and helps compensate for varied lighting and contrast among traffic sign images.
BatchNorm is usually carried out right after a Conv2D layer and before or after ReLU. Also carried out in fully connected (dense) networks.

6. Researching on what the thought process should be before modeling a neural network, made me learn that we should think in convolution blocks, not random layers. Then stack those blocks to make the model deeper for better accuracy. In these case, its preferable to go with stacks of blocks with the following structure :--
    - Conv2D with some number of filters (starting with 32)
    - BatchNorm
    - another Conv2D with same number of filters
    - BatchNorm again
    - MaxPooling (2x2 pool size)
    - Dropout (0.25 or so)

A good strategy is doubling the no. of filters for Conv2D in following blocks, so :
    - Block 1 : 32 filters
    - Block 2 : 64 filters
    - Block 3 : 128 filters
                ... and so on

Kernel size : 3x3

7. Learnt about padding in Convolution process to compensate for pooling as pooling will make the feature maps smaller in size each time its done.
If padding = "valid" it means there's no padding and feature maps shrink to eventually become too small to learn anything.
If padding = "same" it means padding is added such that the feature map produced is same size as input. This is useful because it helps the network avoid losing information around the edges of the images. Also helps to keep the spatial structure intact allowing us to model deeper networks. The CNN learns better in most cases.

8. The model should be deep enough to capture details but not so deep that it overfits on training dataset or takes "forever" to train.
A rough estimate on the number of nodes we obtain after flattening the output after 3 blocks would be as follows :--
(shape progression)
    - 30 x 30 x 3 image undergoes Conv2D with "same" padding across 32 kernels, resulting in 30 x 30 x 32 image
    - MaxPooling2D with pool_size of 2x2 reduces resolution to give 15 x 15 x 32 image
    - next block introduces Conv2D with 64 kernels, result : 15 x 15 x 64 since padding = "same"
    - again MaxPooling2D, result : 7 x 7 x 64
    - final block introduces Conv2D with 128 kernels, result : 7 x 7 x 128 , padding = "same"
    - again MaxPooling2D, result : 3 x 3 x 128
Before dense layers, we flatten 3x3x128 = 1152 features. So dense layer receives a vector of length 1152as input. 128-512 nodes are sufficient enough for the hidden layer. In this project, 256 nodes were implemented in hidden layer.

9. To avoid overfitting, dropout was implemented in hidden layer.
   Output layer has number of nodes = NUM_CATEGORIES and activation function used is softmax for converting into probability distribution.

---

