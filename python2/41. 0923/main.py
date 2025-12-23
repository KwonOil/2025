import tensorflow_hub as hub
import data_reader

dr = data_reader.DataReader(r"python2\41. 0923\img\content.jpg", r"python2\41. 0923\img\content.jpg")

# Hub로부터 style transfer 모듈을 불러옵니다.
hub_module = hub.load(
    'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1'
)

stylized_image = hub_module(dr.content, dr.style)[0]

result = data_reader.tensor_to_image(stylized_image)

result.save(r"python2\41. 0923\img\result2+-.jpg")