
El proyecto está basado en el paper "FaceNet: A Unified Embedding for Face Recognition and Clustering" y en el modelo prentrenado de David Sandberg, el cual se entrenó con 453453 imágenes con 10575 personas.


### Uso 

Las imágenes de de las personas a reconocer se añaden en la carpeta "train_img" con su respectiva carpeta y nombre. Se necesitan alrededor de 30 fotos para tener un reconocimiento apropiado. 

Luego de eso se corre el archivo "data_preprocesspy". Este archivo detectará y recortará las caras de todas las personas dentro de la carpeta  "train_img" 

Luego se corre el archivo "train_main.py", con este archivo se entrena nuestro modelo usando el modelo prentrenado y las caras recortadas guardadas en la carpeta "pre_img" 

Finalmente se corre el archivo "identify_video.py", el cual lee la entrada de la cámara del pc como input y muestra visualmente en la pantalla el resultado. 

El archivo "Untitled.ipynb" contiene lo mismo que los 3 archivos anteriormente descritos, es un archivo que hicimos para probar el código desde Jupyter y Colaboratory.

También se añadió un archivo "funciones.py" para tomar una ráfaga de 50 fotos de la persona en caso de ser necesario. 
